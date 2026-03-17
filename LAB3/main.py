import asyncio
import spade
from agents.client_agent import ClientAgent
from agents.detector_agent import DetectorAgent
from agents.preprocessor_agent import PreprocessorAgent
from agents.ocr_agent import OCRAgent
from agents.validator_agent import ValidatorAgent

async def main():
    validator    = ValidatorAgent("validator@localhost",       "pass1")
    ocr          = OCRAgent("ocr@localhost",                  "pass2")
    preprocessor = PreprocessorAgent("preprocessor@localhost","pass3")
    detector     = DetectorAgent("detector@localhost",        "pass4")
    client       = ClientAgent("client@localhost",            "pass5",
                               image_path="images/car.jpg")

    await validator.start(auto_register=True)
    await ocr.start(auto_register=True)
    await preprocessor.start(auto_register=True)
    await detector.start(auto_register=True)

    await asyncio.sleep(2)  # wait for all agents to be ready

    await client.start(auto_register=True)

    while client.is_alive():
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break

    await client.stop()
    await detector.stop()
    await preprocessor.stop()
    await ocr.stop()
    await validator.stop()
    print("\n All agents stopped.")

if __name__ == "__main__":
    spade.run(main())
