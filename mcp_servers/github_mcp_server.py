"""GitHub MCP Server."""

from flock.core import FlockFactory

from settings import APP_SETTINGS



github_mcp_server = FlockFactory.create_mcp_server(
    name="github_mcp_server",
    connection_params=FlockFactory.StdioParams(
        command="docker",
        args=[
            "run",
            "-i",
            "--init",
            "--rm",
            "-e",
            f"GITHUB_PERSONAL_ACCESS_TOKEN={APP_SETTINGS.github_pat}",
            "ghcr.io/github/github-mcp-server:latest"
        ],
    ),
    enable_tools_feature=True,
)