import asyncio
import sys
from pathlib import Path
import unittest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class ProtocolTest(unittest.TestCase):
    def test_real_stdio_session_and_invalid_input(self):
        async def check():
            params=StdioServerParameters(command=sys.executable,args=['-m','worldrole_free_sources.server'],env={'PYTHONPATH':str(Path(__file__).resolve().parents[1]/'src')})
            async with stdio_client(params) as (read,write):
                async with ClientSession(read,write) as session:
                    await session.initialize()
                    listed=await session.list_tools()
                    self.assertEqual({t.name for t in listed.tools},{'search_free_jobs','list_free_company_jobs'})
                    self.assertTrue(all(t.annotations.read_only_hint for t in listed.tools))
                    result=await session.call_tool('list_free_company_jobs',{'provider':'lever','board':'https://localhost'})
                    self.assertTrue(result.is_error)
                    self.assertIn('board identifier', result.content[0].text)
        asyncio.run(check())


if __name__=='__main__':unittest.main()
