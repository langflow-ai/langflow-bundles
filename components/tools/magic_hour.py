from typing import ClassVar

from lfx.components.models_and_agents.mcp_component import MCPToolsComponent
from lfx.io import SecretStrInput


class MagicHourMCPComponent(MCPToolsComponent):
    display_name = "Magic Hour MCP"
    description = "Generate and edit images, videos, and audio with Magic Hour."
    documentation = "https://magichour.ai/mcp"
    icon = "Video"
    name = "MagicHourMCP"

    inputs: ClassVar[list] = [
        SecretStrInput(
            name="api_key",
            display_name="Magic Hour API Key",
            info="Create an API key at https://magichour.ai/developer",
            required=True,
        ),
        *[
            component_input
            for component_input in MCPToolsComponent.inputs
            if component_input.name not in {"mcp_server", "headers"}
        ],
    ]

    def _configure_server(self) -> None:
        api_key = self.api_key.get_secret_value() if hasattr(self.api_key, "get_secret_value") else self.api_key
        if not api_key:
            msg = "Magic Hour API key is required."
            raise ValueError(msg)

        self.mcp_server = {
            "name": "Magic Hour",
            "config": {
                "url": "https://mcp.magichour.ai/",
                "headers": {"Authorization": f"Bearer {api_key}"},
            },
        }
        self.headers = []

    async def update_tool_list(self, mcp_server_value=None):
        self._configure_server()
        return await super().update_tool_list(self.mcp_server)
