# Magic Hour MCP tools

`magic_hour.py` provides a reusable Magic Hour component on top of Langflow's canonical `MCPToolsComponent`. It connects to `https://mcp.magichour.ai/` over Streamable HTTP and discovers the current image, video, and audio tools and their schemas. It does not add a parallel REST implementation.

Install using Langflow's Custom Component code editor, or load this directory as a custom-component category with `--components-path`. Requires lfx 1.12.7 for the tested compatibility version.

Create a Magic Hour API key at https://magichour.ai/developer and store it as a Langflow global secret named `MAGIC_HOUR_API_KEY`. Select it in the component's secret input. This refreshes tool discovery and exposes the tool dropdown. Select a tool and fill its dynamically generated fields, or enable Tool Mode and connect its Toolset to an Agent.

The importable example at `flows/magic-hour-retrieve-image.json` retrieves an existing image project. Enter your own project's ID before running; it never submits a paid generation. The example embeds component source and uses a secret-variable reference, without an API credential or output download URL.

Generations consume Magic Hour credits. Save an accepted project ID before waiting and retrieve that same project after an interruption instead of generating again.

The component returns a credential-free editor configuration and hashes runtime headers into the parent tool-cache key, including before Tool Mode lookup, to isolate credential-bound tools when a key rotates.

Verification: 11 tests with the real lfx runtime; full Langflow 1.12.7 editor loading, secret-variable selection, discovery of 46 tools, dynamic field selection, and an actual completed-project retrieval shown in the output inspector. An imported portable copy of the flow also executed successfully through the authenticated Langflow run API. Previous live generation through the discovered MCP creation tool was verified separately. Editor retrieval reused the same completed project without another credit charge.

```sh
python3 -m pip install -r components/tools/requirements-dev.txt
python3 -m pytest -q components/tools/tests
python3 -m ruff check components/tools/magic_hour.py components/tools/tests
```

Documentation: https://docs.magichour.ai/integration/langflow
