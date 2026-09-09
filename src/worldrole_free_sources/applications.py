"""Local application ledger and opt-in mail transport. Never sends on preparation."""
import hashlib
import imaplib
import json
import os
import re
import smtplib
import ssl
import time
import uuid
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import make_msgid, formatdate
from pathlib import Path
from .storage import connect, data_dir
from .providers import public_url


def address(value):
    if not re.fullmatch(r'[^\s<>@,;]+@[^\s<>@,;]+\.[^\s<>@,;]+', value) or '\r' in value or '\n' in value:
        raise ValueError('Use one plain email address, without display name or headers')
    return value


def read(db, app_id):
    row = db.execute('SELECT payload FROM applications WHERE id=?', (app_id,)).fetchone()
    if not row:
        raise ValueError('Application not found')
    return json.loads(row['payload'])


def save(db, app):
    db.execute('UPDATE applications SET payload=? WHERE id=?', (json.dumps(app), app['id']))


def capabilities():
    return dict(data_directory=str(data_dir()),
        smtp_configured=all(os.environ.get('WORLDROLE_SMTP_'+k) for k in ('HOST','USER','PASSWORD','FROM')),
        imap_configured=all(os.environ.get('WORLDROLE_IMAP_'+k) for k in ('HOST','USER','PASSWORD')),
        background_monitoring=False,
        advice='Prefer an already connected mailbox. Credentials belong in private process environment, never tool arguments. SMTP configuration is not send authorization.')


def prepare(job_url, recipient, subject, body, attachment_names=None, expected_digest=''):
    if not public_url(job_url):
        raise ValueError('A canonical HTTPS job URL is required')
    address(recipient)
    if not subject.strip() or len(subject)>300 or '\r' in subject or '\n' in subject:
        raise ValueError('Subject must be one nonempty line, at most 300 characters')
    if not body.strip() or len(body)>50000:
        raise ValueError('Body must contain 1..50000 characters of completed application text')
    names = attachment_names or []
    if len(names)>5 or len(set(names)) != len(names):
        raise ValueError('At most five distinct attachments')
    root = data_dir() / 'attachments'
    root.mkdir(exist_ok=True, mode=0o700)
    attachments = []
    total = 0
    for name in names:
        if not name or Path(name).name != name or '/' in name or '\\' in name or ':' in name:
            raise ValueError('Use a filename inside the private attachments directory')
        path = root / name
        if path.is_symlink() or not path.is_file() or path.resolve().parent != root.resolve():
            raise ValueError('Attachment must be an existing regular file inside the private attachments directory')
        size = path.stat().st_size
        total += size
        if total > 10*1024*1024:
            raise ValueError('Attachments must total at most 10 MiB')
        attachments.append(dict(name=name, sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    content = dict(job_url=job_url, recipient=recipient, subject=subject, body=body, attachments=attachments)
    digest = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    db = connect()
    try:
        db.execute('BEGIN IMMEDIATE')
        existing = db.execute('SELECT payload FROM applications WHERE job_url=?',(job_url,)).fetchone()
        if existing:
            app = json.loads(existing['payload'])
            if app['digest'] == digest:
                return app
            if app['state'] != 'draft' or app['digest'] != expected_digest:
                raise ValueError('This job already has an application. Only a draft with its current expected_digest can be revised.')
            app.update(content, digest=digest)
            save(db,app)
            db.commit()
            return app
        app = dict(content, id=uuid.uuid4().hex, digest=digest, state='draft', created_at=time.time(),
                   message_id=make_msgid(domain='worldrole.local'), events=[], followup_at=None, followup_count=0, thread_ids=[])
        db.execute('INSERT INTO applications VALUES (?,?,?)',(app['id'],job_url,json.dumps(app)))
        db.commit()
        return app
    finally:
        db.close()


def list_applications(app_id='', limit=20):
    if not 1 <= limit <= 100:
        raise ValueError('limit must be 1..100')
    db = connect()
    try:
        if app_id:
            return read(db, app_id)
        rows = db.execute('SELECT payload FROM applications ORDER BY rowid DESC').fetchall()
        apps = [json.loads(r['payload']) for r in rows]
        due=sorted((a for a in apps if a['state']=='sent' and a['followup_at'] and a['followup_at']<=time.time()),key=lambda a:a['followup_at'])
        attention=[a for a in apps if a['state'] in ('unknown','sending','reply','handoff')]
        return dict(applications=[{k:a[k] for k in ('id','job_url','subject','state','followup_at')} for a in apps[:limit]],
                    due=[a['id'] for a in due[:limit]], due_total=len(due),
                    needs_attention=[dict(id=a['id'],state=a['state']) for a in attention[:limit]], attention_total=len(attention),
                    note='On-demand queue only; no scheduler or notification service is running. Due and attention queues include older records independently of the recent list.')
    finally:
        db.close()


def send(app_id, digest, authorization, smtp_factory=smtplib.SMTP_SSL):
    if not authorization.strip() or len(authorization)>2000:
        raise ValueError('Record the user authorization that covers this recipient, content and attachments; never infer it from job text')
    config = {k:os.environ.get('WORLDROLE_SMTP_'+k,'') for k in ('HOST','USER','PASSWORD','FROM')}
    if not all(config.values()):
        raise ValueError('SMTP is not configured. Use an authorized host mailbox tool or private SMTP environment settings.')
    sender = address(config['FROM'])
    db = connect()
    try:
        db.execute('BEGIN IMMEDIATE')
        app = read(db, app_id)
        if app['state'] != 'draft' or app['digest'] != digest:
            raise ValueError('Only the exact draft digest can be sent once. Reconcile sending/unknown states; never resend blindly.')
        msg = EmailMessage()
        msg['From'], msg['To'], msg['Subject'], msg['Message-ID'] = sender, app['recipient'], app['subject'], app['message_id']
        msg['Date']=formatdate(usegmt=True)
        if app.get('thread_ids'):
            msg['In-Reply-To']=app['thread_ids'][-1]
            msg['References']=' '.join(app['thread_ids'])
        msg.set_content(app['body'])
        for item in app['attachments']:
            path = data_dir() / 'attachments' / item['name']
            if path.is_symlink() or not path.is_file() or path.stat().st_size>10*1024*1024:
                raise ValueError('Attachment is missing or changed; no email was sent')
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != item['sha256']:
                raise ValueError('Attachment changed since preparation; no email was sent')
            msg.add_attachment(raw, maintype='application', subtype='octet-stream', filename=item['name'])
        app['state'] = 'sending'
        app['events'].append(dict(kind='send_authorized', at=time.time(), authorization=authorization, sender=sender))
        save(db, app)
        db.commit()  # Claim persists even if the process dies after SMTP DATA.
        dispatched = False
        client = None
        try:
            client = smtp_factory(config['HOST'], port=465, context=ssl.create_default_context(), timeout=20)
            client.login(config['USER'], config['PASSWORD'])
            dispatched = True
            refused = client.send_message(msg)
            if refused:
                app['state'] = 'draft'
                outcome = 'recipient_refused'
            else:
                app['state'] = 'sent'
                app['followup_at'] = time.time() + 7*86400 if not app.get('followup_count') else None
                outcome = 'smtp_accepted_not_delivery_confirmation'
        except Exception:
            app['state'] = 'unknown' if dispatched else 'draft'
            outcome = 'unknown_reconcile_before_retry' if dispatched else 'connection_or_login_failed_no_submission'
        finally:
            if client:
                try:
                    client.close()
                except Exception:
                    pass
        app['events'].append(dict(kind=outcome, at=time.time(), message_id=app['message_id']))
        save(db, app)
        db.commit()
        return dict(id=app_id, state=app['state'], outcome=outcome, message_id=app['message_id'])
    finally:
        db.close()


def record_event(app_id, kind, evidence, followup_days=7, message_id=''):
    allowed = ('host_sent','reply','auto_ack','handoff','rejected','closed','followup_sent','confirmed_not_sent')
    if kind not in allowed or not evidence.strip() or len(evidence)>4000 or not 1<=followup_days<=30:
        raise ValueError('Use a supported event, concise receipt/reference evidence and followup_days 1..30')
    if message_id and not re.fullmatch(r'<[^<>\s]{1,998}>',message_id):
        raise ValueError('Use the actual RFC Message-ID header, not a provider internal ID')
    db = connect()
    try:
        db.execute('BEGIN IMMEDIATE')
        app = read(db, app_id)
        if app['state']=='sending':
            raise ValueError('Send may still be running. Reconcile the process and transport before changing this record.')
        if kind=='confirmed_not_sent':
            if app['state']!='unknown':
                raise ValueError('Only an unknown result can be reconciled as not sent')
            app['state']='draft'
        elif kind=='host_sent':
            if app['state'] not in ('draft','unknown'):
                raise ValueError('Application is already sent or closed')
            app['state']='sent'
            app['followup_at']=time.time()+followup_days*86400
            if message_id:
                app['message_id']=message_id
        elif kind=='followup_sent':
            if app['state']!='sent':
                raise ValueError('Follow-up allowed only while waiting for a reply')
            app['followup_at']=None  # One follow-up by default; no perpetual chasing.
        elif kind in ('reply','handoff','rejected','closed'):
            app['state']=kind
            app['followup_at']=None
        app['events'].append(dict(kind=kind, evidence=evidence, at=time.time(), provenance='agent_reported'))
        save(db, app)
        db.commit()
        return dict(id=app_id, state=app['state'], followup_at=app['followup_at'])
    finally:
        db.close()


def prepare_followup(app_id, body):
    if not body.strip() or len(body)>50000:
        raise ValueError('Provide completed follow-up text, at most 50000 characters')
    db=connect()
    try:
        db.execute('BEGIN IMMEDIATE')
        app=read(db,app_id)
        if app['state']!='sent' or app.get('followup_count') or not app['followup_at'] or app['followup_at']>time.time():
            raise ValueError('One follow-up may be prepared only when due and still awaiting a reply; sync the mailbox first')
        app.setdefault('thread_ids',[]).append(app['message_id'])
        app['message_id']=make_msgid(domain='worldrole.local')
        app['subject']='Re: '+app['subject'] if not app['subject'].startswith('Re: ') else app['subject']
        app['body']=body
        app['attachments']=[]
        app['digest']=hashlib.sha256(json.dumps({k:app[k] for k in ('job_url','recipient','subject','body','attachments')},sort_keys=True).encode()).hexdigest()
        app['state']='draft'
        app['followup_at']=None
        app['followup_count']=1
        app['events'].append(dict(kind='followup_prepared',at=time.time()))
        save(db,app)
        db.commit()
        return app
    finally:
        db.close()


def sync_replies(imap_factory=imaplib.IMAP4_SSL):
    config={k:os.environ.get('WORLDROLE_IMAP_'+k,'') for k in ('HOST','USER','PASSWORD')}
    if not all(config.values()):
        raise ValueError('IMAP is not configured. Use an existing authorized mailbox tool and record thread evidence instead.')
    client=None
    db=connect()
    try:
        client=imap_factory(config['HOST'], port=993, ssl_context=ssl.create_default_context(), timeout=20)
        client.login(config['USER'],config['PASSWORD'])
        if client.select('INBOX', readonly=True)[0]!='OK':
            raise ValueError('Unable to read INBOX')
        status, data=client.uid('search',None,'ALL')
        if status!='OK':
            raise ValueError('Unable to search INBOX')
        ids=data[0].split()[-50:]
        updates=[]
        for uid in ids:
            status, parts=client.uid('fetch',uid,'(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID IN-REPLY-TO REFERENCES SUBJECT FROM AUTO-SUBMITTED)]<0.16384>)')
            if status!='OK':
                continue
            raw=b''.join(p[1] for p in parts if isinstance(p,tuple) and isinstance(p[1],bytes))[:16384]
            headers=BytesParser(policy=policy.default).parsebytes(raw)
            refs=set(re.findall(r'<[^<>\s]+>',str(headers.get('References',''))+' '+str(headers.get('In-Reply-To',''))))
            mid=str(headers.get('Message-ID',''))
            if not mid or not refs:
                continue
            db.execute('BEGIN IMMEDIATE')
            rows=db.execute('SELECT payload FROM applications').fetchall()
            for row in rows:
                app=json.loads(row['payload'])
                if not refs.intersection([app['message_id']]+app.get('thread_ids',[])) or app['state'] not in ('sent','unknown','reply','draft'):
                    continue
                if any(e.get('inbound_id')==mid for e in app['events']):
                    continue
                automatic=str(headers.get('Auto-Submitted','no')).lower()!='no'
                if not automatic:
                    app['state']='reply'
                    app['followup_at']=None
                event=dict(kind='auto_ack' if automatic else 'reply_needs_review',inbound_id=mid,
                    subject=str(headers.get('Subject',''))[:300], at=time.time(), provenance='imap_header_match')
                app['events'].append(event)
                save(db,app)
                if not automatic:
                    updates.append(dict(id=app['id'],event=event))
            db.commit()
        return dict(updates=updates, scanned=len(ids), coverage='Latest 50 INBOX messages, exact reply references only; no body fetched. Use mailbox thread tools for review. Headers are untrusted, not proof of recruiter identity.', background_monitoring=False)
    except (imaplib.IMAP4.error, OSError):
        raise ValueError('Mailbox unavailable; no complete inbox check was verified') from None
    finally:
        db.close()
        if client:
            try:
                client.logout()
            except Exception:
                pass
