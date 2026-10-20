"""Magic Hour component for Langflow.

Thin wrapper around Langflow's canonical MCP component. It points the
component at Magic Hour's hosted MCP server and supplies the user's API key
as a Bearer token, so every tool the server exposes (image, video and audio
generation and editing) shows up in the "Tool" dropdown and in Tool Mode for
agents. There is no REST wrapper: tool discovery and execution are done by
the MCP component itself.
"""

from __future__ import annotations

import copy
from typing import ClassVar

from lfx.components.models_and_agents.mcp_component import MCPToolsComponent
from lfx.io import SecretStrInput

MAGIC_HOUR_MCP_URL = "https://mcp.magichour.ai/"
MAGIC_HOUR_SERVER_NAME = "Magic Hour"


def _inputs() -> list:
    api_key = SecretStrInput(
        name="api_key",
        display_name="Magic Hour API Key",
        info="Create a key at https://magichour.ai/developer. Stored as a secret, never saved in the flow JSON.",
        required=True,
    )
    inherited = []
    for field in MCPToolsComponent.inputs:
        field = copy.deepcopy(field)
        if field.name == "mcp_server":
            # The parent's UI logic reads this field, so it must exist. The server is fixed, so hide it.
            field.show = False
        inherited.append(field)
    return [api_key, *inherited]


class MagicHourComponent(MCPToolsComponent):
    display_name = "Magic Hour"
    description = "Generate and edit images, video and audio with Magic Hour (via its hosted MCP server)."
    documentation = "https://docs.magichour.ai"
    icon = "Video"
    name = "MagicHour"

    inputs: ClassVar[list] = _inputs()

    def _server_value(self) -> dict:
        key = self.api_key
        key = key.get_secret_value() if hasattr(key, "get_secret_value") else key
        key = (key or "").strip()
        if not key:
            msg = "Magic Hour API key is required. Create one at https://magichour.ai/developer."
            raise ValueError(msg)
        return {
            "name": MAGIC_HOUR_SERVER_NAME,
            "config": {
                "url": MAGIC_HOUR_MCP_URL,
                "headers": {"Authorization": f"Bearer {key}"},
            },
        }

    async def update_tool_list(self, mcp_server_value=None):  # noqa: ARG002
        # Every caller (build, tool dropdown refresh, agent tool mode) funnels through here,
        # so always use the fixed Magic Hour server regardless of what the caller passes.
        value = self._server_value()
        self.mcp_server = value
        return await super().update_tool_list(value)
