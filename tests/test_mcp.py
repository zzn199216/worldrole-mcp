import asyncio
import sys
from pathlib import Path
import unittest
import tempfile
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class ProtocolTest(unittest.TestCase):
    def test_real_stdio_session_and_invalid_input(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        async def check():
            params=StdioServerParameters(command=sys.executable,args=['-m','worldrole_free_sources.server'],env={'PYTHONPATH':str(Path(__file__).resolve().parents[1]/'src'),'WORLDROLE_DATA_DIR':temp.name})
            async with stdio_client(params) as (read,write):
                async with ClientSession(read,write) as session:
                    await session.initialize()
                    listed=await session.list_tools()
                    names={t.name for t in listed.tools}
                    self.assertEqual(names,{'search_free_jobs','list_free_company_jobs','get_application_capabilities',
                        'prepare_application','prepare_application_followup','get_applications','send_application',
                        'record_application_event','sync_application_replies'})
                    indexed={t.name:t for t in listed.tools}
                    self.assertTrue(indexed['search_free_jobs'].annotations.read_only_hint)
                    self.assertFalse(indexed['send_application'].annotations.read_only_hint)
                    self.assertFalse(indexed['send_application'].annotations.idempotent_hint)
                    result=await session.call_tool('list_free_company_jobs',{'provider':'lever','board':'https://localhost'})
                    self.assertTrue(result.is_error)
                    self.assertIn('board identifier', result.content[0].text)
                    draft=await session.call_tool('prepare_application',{'job_url':'https://example.test/job',
                        'recipient':'jobs@example.test','subject':'Application','body':'Known test facts.'})
                    self.assertFalse(draft.is_error)
                    self.assertEqual(draft.structured_content['state'],'draft')
                    app_id=draft.structured_content['id']
                    saved=await session.call_tool('get_applications',{'app_id':app_id})
                    self.assertEqual(saved.structured_content['digest'],draft.structured_content['digest'])
                    blocked=await session.call_tool('send_application',{'app_id':app_id,
                        'digest':draft.structured_content['digest'],'authorization':''})
                    self.assertTrue(blocked.is_error)
        asyncio.run(check())


if __name__=='__main__':unittest.main()
