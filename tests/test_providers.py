import io
import unittest
from unittest.mock import patch
from worldrole_free_sources.providers import SourceError, NoRedirect, fetch_json, search_himalayas, list_board


class ProvidersTest(unittest.TestCase):
    def test_search_preserves_attribution_and_unknown_eligibility(self):
        seen=[]
        def fetch(url):
            seen.append(url)
            return {'jobs':[{'title':'Python Engineer','companyName':'Example','locationRestrictions':['US'],
                'applicationLink':'https://himalayas.app/jobs/example','excerpt':'<b>Build</b> tools'}]}
        r=search_himalayas('python & data',country='US',fetch=fetch)
        self.assertIn('q=python+%26+data',seen[0])
        self.assertEqual(r['jobs'][0]['location_restrictions'],['US'])
        self.assertEqual(r['applicant_eligibility'],'not_checked')
        self.assertIn('Himalayas',r['attribution'])

    def test_search_truncation_does_not_invent_next_page(self):
        r=search_himalayas('python',limit=1,fetch=lambda _:dict(jobs=[{},{}]))
        self.assertTrue(r['truncated'])
        self.assertIsNone(r['next_page'])
        self.assertEqual(r['more_pages'],'unknown')

    def test_greenhouse_offset_and_url(self):
        seen=[]
        def fetch(url):
            seen.append(url)
            return {'jobs':[dict(id=i,title='Engineer',absolute_url='https://example.org/jobs/'+str(i),location={'name':'Remote'}) for i in range(3)]}
        r=list_board('greenhouse','example',offset=1,limit=1,fetch=fetch)
        self.assertEqual(r['jobs'][0]['id'],1)
        self.assertEqual(r['next_page'],{'offset':2})
        self.assertEqual(r['jobs'][0]['location'],'Remote')

    def test_ashby_compensation_and_html(self):
        r=list_board('ashby','example',fetch=lambda _:dict(jobs=[dict(title='Build',descriptionPlain='Work',compensation={'currency':'USD'},jobUrl='https://example.org/job')]))
        self.assertEqual(r['jobs'][0]['compensation']['currency'],'USD')
        self.assertIsNone(r['next_page'])

    def test_lever_eu_pagination_and_spaces(self):
        seen=[]
        def fetch(url):
            seen.append(url);return [dict(id='a',text='Engineer',categories={'location':'Paris'})]
        r=list_board('lever','Flock Safety',offset=4,limit=1,region='eu',fetch=fetch)
        self.assertIn('api.eu.lever.co/v0/postings/Flock%20Safety',seen[0])
        self.assertIn('skip=4&limit=1',seen[0])
        self.assertEqual(r['next_page'],{'offset':5})

    def test_bad_board_and_regions_never_fetch(self):
        def fetch(_):raise AssertionError('Network should not be used')
        for board in ['https://localhost','../secret','foo?x=1','foo/bar','']:
            with self.assertRaises(ValueError):list_board('lever',board,fetch=fetch)
        with self.assertRaises(ValueError):list_board('ashby','example',region='eu',fetch=fetch)

    def test_malformed_upstream_is_not_empty_success(self):
        with self.assertRaises(SourceError):search_himalayas('python',fetch=lambda _:dict(error='bad'))
        with self.assertRaises(SourceError):list_board('lever','example',fetch=lambda _:dict(error='bad'))

    def test_outbound_allowlist_and_redirect(self):
        for url in ['http://himalayas.app/jobs/api','https://localhost/','https://himalayas.app.evil.example/','https://user:secret@himalayas.app/']:
            with self.assertRaises(SourceError):fetch_json(url)
        with self.assertRaises(SourceError):NoRedirect().redirect_request(None,None,302,'',{},'http://localhost')

    def test_response_limit(self):
        class Response(io.BytesIO):
            pass
        class Opener:
            def open(self,*args,**kwargs):return Response(b'12345')
        with patch('urllib.request.build_opener',return_value=Opener()),patch('worldrole_free_sources.providers.MAX_BYTES',4):
            with self.assertRaises(SourceError):fetch_json('https://himalayas.app/jobs/api')


if __name__=='__main__':unittest.main()
