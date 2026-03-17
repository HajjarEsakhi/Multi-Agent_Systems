import os
import cv2
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from ultralytics import YOLO

class DetectorAgent(Agent):
    class DetectBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=30)
            if msg:
                image_path = msg.body
                print(f"[Detector]  Detecting plates in: {image_path}")

                model = YOLO("models/real_detector.pt")

                results = model(image_path)
                image = cv2.imread(image_path)
                os.makedirs("cropped", exist_ok=True)

                cropped_paths = []
                for i, result in enumerate(results):
                    for j, box in enumerate(result.boxes.xyxy):
                        x1, y1, x2, y2 = map(int, box)
                        crop = image[y1:y2, x1:x2]
                        path = f"cropped/plate_{i}_{j}.jpg"
                        cv2.imwrite(path, crop)
                        cropped_paths.append(path)
                        print(f"[Detector]  Cropped → {path}")
            

                if cropped_paths:
                    reply = Message(to="preprocessor@localhost")
                    reply.set_metadata("performative", "inform")
                    reply.set_metadata("ontology", "plate-preprocessing")
                    reply.body = cropped_paths[0]
                    await self.send(reply)
                    print("[Detector]  Sent to Preprocessor")
                else:
                    print("[Detector]  No plates detected.")

    async def setup(self):
        print("[Detector] Agent started.")
        self.add_behaviour(self.DetectBehaviour())
