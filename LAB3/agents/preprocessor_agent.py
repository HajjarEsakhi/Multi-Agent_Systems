from PIL import Image, ImageEnhance
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class PreprocessorAgent(Agent):
    class PreprocessBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=30)
            if msg:
                path = msg.body
                print(f"[Preprocessor]   Enhancing: {path}")

                img = Image.open(path).convert("RGB")
                """
                img = img.resize(
                    (img.width * 2, img.height * 2),
                    Image.LANCZOS
                )
                """
                img = ImageEnhance.Contrast(img).enhance(2.0)
                img = ImageEnhance.Sharpness(img).enhance(2.0)

                out_path = path.replace("plate_", "enhanced_plate_")
                img.save(out_path)
                print(img.size)
                
                reply = Message(to="ocr@localhost")
                reply.set_metadata("performative", "inform")
                reply.set_metadata("ontology", "plate-ocr")
                reply.body = out_path
                await self.send(reply)
                print("[Preprocessor]  Sent to OCR Agent")

    async def setup(self):
        print("[Preprocessor] Agent started.")
        self.add_behaviour(self.PreprocessBehaviour())
