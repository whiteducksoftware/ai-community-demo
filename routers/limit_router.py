"""Limiting Router."""


from flock.core.flock_router import FlockRouter, FlockRouterConfig, HandOffRequest
from flock.routers.agent.agent_router import AgentRouter
from pydantic import ConfigDict, Field


class LimitRouterConfig(FlockRouterConfig):
    """Config."""
    
    max_iterations: int = Field(
        default=10,
        description="Max number of iterations."
    )
    
    orchestrator: AgentRouter = Field(
        ...,
        description="Orchestrator agent."
    )
    
    model_config: ConfigDict = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
    )
    
class LimitRouter(FlockRouter):
    """Limiting Router. Stops after self.config.max_iterations"""
    
    config: LimitRouterConfig = Field(
        ...,
        description="Internal Config"
    )
    
    current_iteration: int = Field(
        default=0,
        description="Current Iteration."
    )
    
    async def route(self, current_agent, result, context) -> HandOffRequest:
        self.current_iteration += 1
        
        if self.current_iteration > self.config.max_iterations:
            self.current_iteration = 0
            return HandOffRequest(
                next_agent=""
            )
        else:
            return await self.config.orchestrator.route(
                current_agent=current_agent,
                result=result,
                context=context
            )