"""RAG agent"""

from flock.core import FlockFactory

from local_tools.memory_tools import ask_knowledge_base, check_knowledge_base_health, get_indexes, search_knowledge_base
from settings import APP_SETTINGS

AGENT_NAME="project_manager_agent"
AGENT_DESCRIPTION="""Project Manager
This Agent has access to a knowledge-base,
allowing it to leverage its Tools to 
retrieve the requirements, information about
the tech stack, and project-definitions for a given project.

It then produces concrete task-items for other agents to 
tackle.
When producing tasks, it searches through the knowledge-base
and asks the integrated LLM of the knowledge-base for information
in order to make informed decisions.
It creates the tasks with the provided action_report in mind.
"""

AGENT_INPUT="""overall_goal: str | information about the project and additional instructions,
action_report: list[dict[str, Any]] | An (optional) action report of steps already performed by the other agents in the team."""
AGENT_OUTPUT="""tasks: list[dict[str, Any]] | A list of individual tasks that detail the steps to implement the project,
"""


TOOLS = [
    ask_knowledge_base,
    get_indexes,
    search_knowledge_base,
    check_knowledge_base_health,
]


rag_agent = FlockFactory.create_default_agent(
    name=AGENT_NAME,
    description=AGENT_DESCRIPTION,
    input=AGENT_INPUT,
    output=AGENT_OUTPUT,
    include_thought_process=True,
    stream=True,
    enable_rich_tables=True,
    model=APP_SETTINGS.default_model,
    max_tokens=8192,
    max_tool_calls=1000,
    temperature=1.0,
    print_context=True,
    tools=TOOLS,
)