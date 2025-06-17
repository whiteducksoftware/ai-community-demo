import asyncio
import os
import uuid
from agents.github_agent import github_agent
from agents.rag_agent import rag_agent
from mcp_servers.github_mcp_server import github_mcp_server
from routers.limit_router import LimitRouter, LimitRouterConfig
from settings import APP_SETTINGS
from utils.upload_file_function import upload_files
from flock.core import Flock
from flock.routers.agent.agent_router import AgentRouter, AgentRouterConfig
from flock.core.logging.logging import configure_logging


async def upload(
    paths: list[str],
    index: str,
) -> None:
    """Upload the files to the memory."""
    await upload_files(document_id=str(uuid.uuid4()), index=index, files=paths)


async def saturate() -> None:
    cwd = os.getcwd()
    folder = "/files_for_memory"

    files_to_upload = [
        f"{cwd}{folder}/project_definition.md",
        f"{cwd}{folder}/requirments.md",
        f"{cwd}{folder}/tech_stack.md",
        f"{cwd}{folder}/github_rules.md",
        f"{cwd}{folder}/roadmap.md",
    ]

    await upload(
        paths=files_to_upload,
        index="default",
    )


async def run_agents(task: str) -> None:
    agent_router = AgentRouter(
        name="agent_router",
        config=AgentRouterConfig(
            enabled=True, with_output=True, confidence_threshold=0.75,
        )
    )
    
    limit_router = LimitRouter(
        name="limit_router",
        config=LimitRouterConfig(
            enabled=True,
            max_iterations=10,
            orchestrator=agent_router,
        )
    )

    rag_agent.handoff_router = limit_router
    github_agent.handoff_router = limit_router

    flock = Flock(
        name="demo_swarm",
        model=APP_SETTINGS.default_model,
        show_flock_banner=True,
        agents=[
            rag_agent,
            github_agent,
        ],
        servers=[
            github_mcp_server,
        ],
    )

    configure_logging(flock_level="ERROR", external_level="ERROR")

    result = await flock.run_async(
        start_agent=rag_agent,
        input={
            "overall_goal": task,
        },
    )

    if result.get("action_report", None):
        print(result["action_report"])
    else:
        print("faulty code.")


async def main():
    await saturate()
    task = input("Please provide a task: ")
    await run_agents(task=task)


if __name__ == "__main__":
    asyncio.run(main())
