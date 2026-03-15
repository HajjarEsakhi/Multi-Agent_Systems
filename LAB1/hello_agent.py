import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour


class HelloAgent(Agent):
    """
    A simple agent that prints Hello World and its identification
    """
    
    class HelloBehaviour(OneShotBehaviour):
        """
        Behaviour that runs once when the agent starts
        """
        async def run(self):
            print("\n=== AGENT OUTPUT ===")
            print("Hello World! I am a SPADE Agent.")
            print(f"My JID (identifier) is: {self.agent.jid}")
            print(f"Agent is running: {self.agent.is_alive()}")
            print("===================\n")
            
            # Stop the agent after printing
            await self.agent.stop()
    
    async def setup(self):
        """
        Setup method - called when agent starts
        """
        print("Agent starting up...")
        behaviour = self.HelloBehaviour()
        self.add_behaviour(behaviour)


async def main():
    """
    Main function to create and start the agent
    """
    print("Creating agent...")
    agent = HelloAgent("myagent@localhost", "password123")
    
    print("Starting agent...")
    await agent.start()
    
    print("Agent started. Waiting for completion...")
    
    # Wait a bit for the behaviour to execute
    await asyncio.sleep(2)
    
    print("Stopping agent...")
    await agent.stop()
    print("Agent stopped successfully!")


if __name__ == "__main__":
    print("Program starting...\n")
    
    # Windows event loop fix
    if asyncio.sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Run the main coroutine
    spade.run(main())
    
    print("\nProgram finished.")
