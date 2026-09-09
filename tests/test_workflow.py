import json
import os
import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import Mock, patch
from worldrole_free_sources import applications as a, discovery as d
from worldrole_free_sources.providers import SourceError
from worldrole_free_sources.storage import connect


class PrivateTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.env=patch.dict(os.environ, {'WORLDROLE_DATA_DIR':self.temp.name,
            'WORLDROLE_SMTP_HOST':'smtp.example.test','WORLDROLE_SMTP_USER':'user',
            'WORLDROLE_SMTP_PASSWORD':'private-test-password','WORLDROLE_SMTP_FROM':'me@example.test',
            'WORLDROLE_IMAP_HOST':'imap.example.test','WORLDROLE_IMAP_USER':'user','WORLDROLE_IMAP_PASSWORD':'private-test-password'})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def draft(self, **kwargs):
        return a.prepare('https://example.test/jobs/1','jobs@example.test','Application','Supported experience.',**kwargs)

    def smtp(self):
        client=Mock()
        client.send_message.return_value={}
        return client,Mock(return_value=client)

    def test_draft_idempotency_revision_and_send_exactly_once(self):
        app=self.draft()
        self.assertEqual(app['id'],self.draft()['id'])
        revised=a.prepare(app['job_url'],app['recipient'],app['subject'],'Corrected facts.',expected_digest=app['digest'])
        client,factory=self.smtp()
        with self.assertRaises(ValueError):
            a.send(app['id'],app['digest'],'User authorized this application',factory)
        self.assertFalse(factory.called)
        sent=a.send(app['id'],revised['digest'],'User authorized this application',factory)
        self.assertEqual(sent['state'],'sent')
        self.assertIn('not_delivery',sent['outcome'])
        with self.assertRaises(ValueError):
            a.send(app['id'],revised['digest'],'same authorization',factory)
        self.assertEqual(client.send_message.call_count,1)

    def test_unknown_send_never_retried_and_error_secrets_hidden(self):
        app=self.draft()
        client,factory=self.smtp()
        client.send_message.side_effect=TimeoutError('private-test-password')
        result=a.send(app['id'],app['digest'],'User delegated sending',factory)
        self.assertEqual(result['state'],'unknown')
        self.assertNotIn('private-test-password',json.dumps(a.list_applications(app['id'])))
        with self.assertRaises(ValueError):
            a.send(app['id'],app['digest'],'retry',factory)

    def test_login_failure_no_submission(self):
        app=self.draft()
        client,factory=self.smtp()
        client.login.side_effect=OSError('private-test-password')
        result=a.send(app['id'],app['digest'],'User delegated sending',factory)
        self.assertEqual(result['state'],'draft')
        self.assertFalse(client.send_message.called)

    def test_concurrent_calls_submit_once(self):
        app=self.draft()
        client,factory=self.smtp()
        def call():
            try:
                return a.send(app['id'],app['digest'],'User delegated sending',factory)['state']
            except ValueError:
                return 'blocked'
        with ThreadPoolExecutor(max_workers=2) as executor:
            states=list(executor.map(lambda _:call(),range(2)))
        self.assertEqual(sorted(states),['blocked','sent'])
        self.assertEqual(client.send_message.call_count,1)

    def test_changed_attachment_and_header_injection_blocked(self):
        folder=Path(self.temp.name)/'attachments';folder.mkdir()
        (folder/'cv.txt').write_text('original',encoding='utf-8')
        app=self.draft(attachment_names=['cv.txt'])
        (folder/'cv.txt').write_text('changed',encoding='utf-8')
        _,factory=self.smtp()
        with self.assertRaises(ValueError):
            a.send(app['id'],app['digest'],'Authorized',factory)
        self.assertFalse(factory.called)
        with self.assertRaises(ValueError):
            self.draft(attachment_names=['../cv.txt'])
        with self.assertRaises(ValueError):
            a.prepare('https://example.test/job','jobs@example.test','Hi\r\nBcc: x@example.test','Body')

    def test_due_followup_threads_and_reply_stops_further_sending(self):
        app=self.draft()
        a.record_event(app['id'],'host_sent','Actual provider receipt',message_id='<actual@example.test>')
        db=connect()
        with db:
            stored=a.read(db,app['id']);stored['followup_at']=time.time()-1;a.save(db,stored)
        db.close()
        self.assertEqual(a.list_applications()['due'],[app['id']])
        follow=a.prepare_followup(app['id'],'A concise follow-up.')
        self.assertEqual(follow['thread_ids'],['<actual@example.test>'])
        client,factory=self.smtp()
        a.send(app['id'],follow['digest'],'User authorized one follow-up',factory)
        msg=client.send_message.call_args.args[0]
        self.assertEqual(msg['In-Reply-To'],'<actual@example.test>')
        self.assertIsNone(a.list_applications(app['id'])['followup_at'])
        a.record_event(app['id'],'reply','Actual thread receipt')
        with self.assertRaises(ValueError):
            a.prepare_followup(app['id'],'Again')

    def test_imap_readonly_exact_thread_dedup_and_auto_ack(self):
        app=self.draft()
        a.record_event(app['id'],'host_sent','Actual receipt')
        client=Mock()
        client.select.return_value=('OK',[b'3'])
        def uid(command,*args):
            if command=='search':return ('OK',[b'1 2 3'])
            n=args[0].decode()
            reference='<unrelated@test>' if n=='1' else app['message_id']
            raw=f'Message-ID: <reply{n}@test>\r\nIn-Reply-To: {reference}\r\nSubject: Reply {n}\r\n'.encode()
            if n=='2':raw+=b'Auto-Submitted: auto-replied\r\n'
            return ('OK',[(b'header',raw),b')'])
        client.uid.side_effect=uid
        first=a.sync_replies(Mock(return_value=client))
        self.assertEqual(len(first['updates']),1)
        self.assertEqual(a.list_applications(app['id'])['state'],'reply')
        self.assertEqual(a.sync_replies(Mock(return_value=client))['updates'],[])
        client.select.assert_called_with('INBOX',readonly=True)
        self.assertTrue(all('BODY.PEEK' in c.args[2] for c in client.uid.call_args_list if c.args[0]=='fetch'))

    def test_partial_sources_dedup_exclusions_and_country_disclosure(self):
        def fetch(url):
            if 'himalayas' in url:raise SourceError('Unavailable')
            if 'jobicy' in url:return {'jobs':[{'id':1,'jobTitle':'Python','url':'https://example.test/one'}]}
            return {'data':[{'slug':'one','title':'Python','url':'https://example.test/one'},
                            {'slug':'two','title':'Python','url':'https://example.test/two'}],'links':{'next':'untrusted'}}
        result=d.search_sources('Python','DE',sources=['himalayas','jobicy','arbeitnow'],fetch=fetch)
        self.assertEqual(len(result['jobs']),2)
        self.assertEqual(result['sources'][0]['status'],'unavailable')
        self.assertFalse(result['sources'][1]['country_filter_applied'])
        result=d.search_sources('Python',sources=['arbeitnow'],exclude_urls=['https://example.test/one'],fetch=fetch)
        self.assertEqual([j['id'] for j in result['jobs']],['two'])

    def test_cache_shared_across_queries_and_failed_feed_cooldown(self):
        with patch.object(d.providers,'fetch_json',return_value={'jobs':[]}) as fetch:
            d.search_sources('Python',sources=['jobicy'])
            d.search_sources('Engineer',sources=['jobicy'])
            self.assertEqual(fetch.call_count,1)
        with patch.object(d.providers,'fetch_json',side_effect=SourceError('Rate limited')) as fetch:
            d.search_sources('Python',sources=['arbeitnow'])
            d.search_sources('Engineer',sources=['arbeitnow'])
            self.assertEqual(fetch.call_count,1)

    def test_old_due_items_survive_recent_list_limit(self):
        first=self.draft()
        a.record_event(first['id'],'host_sent','Actual receipt')
        db=connect()
        with db:
            stored=a.read(db,first['id']);stored['followup_at']=time.time()-1;a.save(db,stored)
        db.close()
        a.prepare('https://example.test/jobs/2','jobs@example.test','Second','Supported facts')
        result=a.list_applications(limit=1)
        self.assertNotEqual(result['applications'][0]['id'],first['id'])
        self.assertEqual(result['due'],[first['id']])

    def test_no_authorization_or_mail_config_means_no_send(self):
        app=self.draft()
        _,factory=self.smtp()
        with self.assertRaises(ValueError):
            a.send(app['id'],app['digest'],'',factory)
        with patch.dict(os.environ,{'WORLDROLE_SMTP_PASSWORD':''}):
            with self.assertRaises(ValueError):
                a.send(app['id'],app['digest'],'Actual delegation',factory)
        self.assertFalse(factory.called)


if __name__=='__main__':unittest.main()
