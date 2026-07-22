from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from app.agents import AgentFactory


class AgentManager:
    """
    Handles Google ADK execution.
    """

    APP_NAME = "supermarket-ai"
    USER_ID = "supermarket-user"
    SESSION_ID = "default"

    def __init__(self):

        self.session_service = InMemorySessionService()

        self.agent = AgentFactory.get_agent()

        self.runner = Runner(
            agent=self.agent,
            app_name=self.APP_NAME,
            session_service=self.session_service,
        )

        self._initialized = False

    async def _initialize(self):
        """
        Creates the ADK session once.
        """

        if self._initialized:
            return

        await self.session_service.create_session(
            app_name=self.APP_NAME,
            user_id=self.USER_ID,
            session_id=self.SESSION_ID,
        )

        self._initialized = True

    async def chat(
        self,
        message: str,
    ) -> str:
        """
        Sends a message to the ADK agent and returns
        the final response.
        """

        await self._initialize()

        user_message = Content(
            role="user",
            parts=[
                Part(text=message)
            ],
        )

        final_response = "No response generated."

        async for event in self.runner.run_async(
            user_id=self.USER_ID,
            session_id=self.SESSION_ID,
            new_message=user_message,
        ):

            # Skip events that don't contain content
            if not getattr(event, "content", None):
                continue

            content = event.content

            if not content.parts:
                continue

            texts = []

            for part in content.parts:
                if getattr(part, "text", None):
                    texts.append(part.text)

            if texts:
                final_response = "\n".join(texts)

        return final_response