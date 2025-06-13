"""Agent that interacts with github."""

from flock.core import FlockFactory

from mcp_servers.github_mcp_server import github_mcp_server
from settings import APP_SETTINGS


AGENT_NAME="github_agent"
AGENT_DESCRIPTION="""An Agent that can interact with the GitHub APIs.
This agent uses the available tools to accomplish the given task and
provides feedback about it's actions.

Commits code, Creates Issues, manages repositories and merges PullRequests.
"""

AGENT_INPUT="""overall_goal: str | Overall goal to achieve,
tasks: list[dict[str, Any]] | A set of tasks to accomplish or actions to perform,"""
AGENT_OUTPUT="""action_report: list[dict[str, Any]] | Detailed report listing the actions performed and a summary of the results as well as the completed tasks and links to created repos issues pull-requests etc,
all_tasks_completed: bool | set to True to stop execution,"""


github_agent = FlockFactory.create_default_agent(
    name=AGENT_NAME,
    description=AGENT_DESCRIPTION,
    servers=[github_mcp_server],
    model=APP_SETTINGS.default_model,
    include_reasoning=True,
    stream=True,
    max_tokens=8192,
    max_tool_calls=1000,
    input=AGENT_INPUT,
    output=AGENT_OUTPUT,
)