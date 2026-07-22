import asyncio

from dotenv import load_dotenv

# Load .env FIRST
load_dotenv()

from app.agents.agent_manager import AgentManager


async def main():

    manager = AgentManager()

    print("Supermarket AI Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            break

        response = await manager.chat(message)

        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())