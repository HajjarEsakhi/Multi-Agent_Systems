from PIL import Image, ImageEnhance
import easyocr
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class OCRAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        print("[OCR] Loading EasyOCR model...")
        # Create the reader once at agent level
        self.ocr_engine = easyocr.Reader(['en'], gpu=False)

    class OCRBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=30)
            if msg:
                path = msg.body
                print(f"[OCR]  Reading plate from: {path}")
                img = Image.open(path)
                # Access the engine via self.agent, not self
                result = self.agent.ocr_engine.readtext(img, detail=0)
                text = " ".join(result).strip()

                print(f"[OCR]  Extracted: '{text}'")

                reply = Message(to="validator@localhost")
                reply.set_metadata("performative", "inform")
                reply.set_metadata("ontology", "plate-validation")
                reply.body = text
                await self.send(reply)

    async def setup(self):
        print("[OCR] Agent started.")
        self.add_behaviour(self.OCRBehaviour())
