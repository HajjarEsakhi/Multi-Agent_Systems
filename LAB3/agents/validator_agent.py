import re
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ValidatorAgent(Agent):
    class ValidateBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=30)
            if msg:
                raw = msg.body
                print(f"[Validator]  Validating: '{raw}'")

                cleaned = re.sub(r'[^A-Z0-9]', '', raw.upper())

                if len(cleaned) >= 4:
                    result = f" Plate detected: {cleaned}"
                else:
                    result = f" Unreadable — raw: '{raw}'"

                reply = Message(to="client@localhost")
                reply.set_metadata("performative", "inform")
                reply.set_metadata("ontology", "plate-result")
                reply.body = result
                await self.send(reply)
                print(f"[Validator]  Sent result to Client")

    async def setup(self):
        print("[Validator] Agent started.")
        self.add_behaviour(self.ValidateBehaviour())
