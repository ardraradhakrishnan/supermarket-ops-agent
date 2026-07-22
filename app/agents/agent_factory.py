from google.adk.agents import Agent

from app.agents.root_agent import root_agent


class AgentFactory:
    """
    Factory responsible for returning agents.
    """

    @staticmethod
    def get_agent() -> Agent:
        return root_agent