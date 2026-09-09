# WorldRole MCP

A free-to-access hosted job-search MCP plus an optional local companion for public job sources. [中文说明](README.md).

Connect `https://mcp.worldrole.work/mcp` using Streamable HTTP. Guests need no API key. Follow [INSTALL.md](INSTALL.md) or https://worldrole.work/install.md. Account access and career summaries are also free subject to the service's current limits; your AI host/model may have separate costs.

The included [skill](skills/worldrole/SKILL.md) tells the agent to reuse known facts, do useful work first, and collect genuinely necessary missing information in one concise request. It does not grant email, upload or application permissions.

## Optional free-source MCP

Python 3.11+ is required only for this companion:

```sh
python -m venv .venv
# Windows: .venv\Scripts\python.exe -m pip install .
.venv/bin/python -m pip install .
```

Use the absolute path to `.venv/bin/worldrole-free-sources` (Windows: `.venv\Scripts\worldrole-free-sources.exe`) as a stdio MCP command. See [the two-connection example](examples/with-free-sources.json). The package is installed from this repository; no PyPI publication is implied.

Tools: `search_free_jobs` searches Himalayas; `list_free_company_jobs` reads known Greenhouse, Ashby and Lever boards. All are public read-only GET requests without keys. Preserve provider attribution; remote does not mean worldwide eligibility. [Sources, pagination and usage limits](docs/SOURCES.md).

This repository does not include the hosted backend, production databases, account service, email sending, application submission or background notifications. Private keys and resumes must never enter this repository.

Tests: `python -m unittest discover -s tests -v`. MIT license covers our original code/skill, not third-party job data.
