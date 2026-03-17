from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message

class ClientAgent(Agent):
    def __init__(self, jid, password, image_path):
        super().__init__(jid, password)
        self.image_path = image_path

    class SendImageBehaviour(OneShotBehaviour):
        async def run(self):
            msg = Message(to="detector@localhost")
            msg.set_metadata("performative", "request")
            msg.set_metadata("ontology", "plate-detection")
            msg.body = self.agent.image_path
            await self.send(msg)
            print(f"[Client] Sent image: {self.agent.image_path}")

    class WaitResultBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=60)
            if msg:
                print(f"\n[Client]  FINAL PLATE RESULT: {msg.body}\n")
                await self.agent.stop()

    async def setup(self):
        print("[Client] Agent started.")
        self.add_behaviour(self.SendImageBehaviour())
        self.add_behaviour(self.WaitResultBehaviour())