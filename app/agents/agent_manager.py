from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from app.agents import AgentFactory


class AgentManager:
    """
    Handles Google ADK execution with multi-session support.
    """

    APP_NAME = "supermarket-ai"
    USER_ID = "supermarket-user"

    def __init__(self):
        self.session_service = InMemorySessionService()
        self.agent = AgentFactory.get_agent()
        self.runner = Runner(
            agent=self.agent,
            app_name=self.APP_NAME,
            session_service=self.session_service,
        )
        self._initialized_sessions = set()

    async def _initialize_session(self, session_id: str):
        """
        Creates the ADK session for a specific session ID if not already created.
        """
        if session_id in self._initialized_sessions:
            return

        await self.session_service.create_session(
            app_name=self.APP_NAME,
            user_id=self.USER_ID,
            session_id=session_id,
        )
        self._initialized_sessions.add(session_id)

    async def chat(
        self,
        message: str,
        session_id: str = "default",
    ) -> str:
        """
        Sends a message to the ADK agent for the given session_id
        and returns the final response.
        """
        await self._initialize_session(session_id)

        user_message = Content(
            role="user",
            parts=[
                Part(text=message)
            ],
        )

        final_response = "No response generated."

        async for event in self.runner.run_async(
            user_id=self.USER_ID,
            session_id=session_id,
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