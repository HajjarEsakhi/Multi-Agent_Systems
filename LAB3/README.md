# TP03 — Automatic License Plate Recognition with SPADE (Python)

> **Course:** Multi-Agent Systems | UEMF / EIDIA  
> **Author:** Esakhi Hajjar | AI Engineering – 2nd Year  
> **Professor:** Pr. Abderrahim Waga  
> **Date:** March 3, 2026

---

## Overview

This project implements an **Automatic Number Plate Recognition (ANPR)** pipeline as a **Multi-Agent System** using SPADE. Each stage of the recognition pipeline is handled by a dedicated autonomous agent — from image input to final validated plate text — integrating **YOLO** for detection and **EasyOCR** for text extraction.

---

## System Architecture

Five agents communicate sequentially over XMPP:

```
[ClientAgent]
     │  image path
     ▼
[DetectorAgent]  ── YOLO ──►  crops plate  ──► cropped/plate_0_0.jpg
     │
     ▼
[PreprocessorAgent]  ── contrast + sharpness + resize ──► enhanced image
     │
     ▼
[OCRAgent]  ── EasyOCR ──►  raw text  (e.g. "LR33 TEE")
     │
     ▼
[ValidatorAgent]  ── regex cleanup ──►  "LR33TEE"
     │
     ▼
[ClientAgent]  ◄── final plate result
```

| Agent | Role |
|-------|------|
| `ClientAgent` | Sends the input image path, waits for the final result |
| `DetectorAgent` | Runs YOLO on the image, crops the detected plate region |
| `PreprocessorAgent` | Resizes (×2), boosts contrast and sharpness with Pillow |
| `OCRAgent` | Reads text from the enhanced plate using EasyOCR |
| `ValidatorAgent` | Strips non-alphanumeric characters, returns clean plate string |

---

## Project Structure

```
TP3_ANPR/
├── agents/
│   ├── client_agent.py         # Sends image, receives final result
│   ├── detector_agent.py       # YOLO-based plate detection & cropping
│   ├── preprocessor_agent.py   # Image enhancement (contrast, sharpness)
│   ├── ocr_agent.py            # EasyOCR text extraction
│   └── validator_agent.py      # Text cleaning and validation
├── models/
│   └── real_detector.pt        # YOLO checkpoint (license plate detector)
├── images/
│   └── car.jpg                 # Input image(s)
├── cropped/                    # Auto-generated: cropped plate images
├── main.py                     # Entry point — starts all agents
└── README.md
```

---

## Prerequisites

- Python 3.8+
- A running SPADE XMPP server on `localhost`
- YOLO checkpoint file: `models/real_detector.pt`

---

## Installation & Usage

### 1. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install spade ultralytics opencv-python Pillow easyocr
```

> EasyOCR will download its language models (~100MB) on first run.

### 3. Start the SPADE XMPP server

Open a **separate terminal** and run:

```bash
spade run
```

Keep this terminal open.

### 4. Add your YOLO model

Place your trained license plate detector checkpoint at:

```
models/real_detector.pt
```

### 5. Add an input image

Place a car image at:

```
images/car.jpg
```

### 6. Run the system

```bash
python main.py
```

---

## Expected Console Output

```
[OCR] Loading EasyOCR model...
[Detector] Agent started.
[Preprocessor] Agent started.
[Validator] Agent started.
[OCR] Agent started.
[Client] Agent started.
[Client] Sent image: images/car.jpg
[Detector] Detecting plates in: images/car.jpg
[Detector] Cropped -> cropped/plate_0_0.jpg
[Detector] Sent to Preprocessor
[Preprocessor] Enhancing: cropped/plate_0_0.jpg
[Preprocessor] Sent to OCR Agent
[OCR] Reading plate from: cropped/enhanced_plate_0_0.jpg
[OCR] Extracted: 'LR33 TEE'
[Validator] Received: 'LR33 TEE'
[Validator] Cleaned plate: 'LR33TEE'
[Validator] Sent result to Client
[Client] Final plate: LR33TEE
```

---

## Agent Details

### DetectorAgent
- Loads `models/real_detector.pt` via Ultralytics YOLO
- Iterates over detected bounding boxes and saves each crop to `cropped/`
- Forwards the first detected crop to the Preprocessor via XMPP message

### PreprocessorAgent
- Opens the cropped image with Pillow
- Upscales 2× using `LANCZOS` resampling
- Applies contrast enhancement (×2.0) and sharpness enhancement (×2.0)
- Saves result as `enhanced_plate_*.jpg` and forwards to OCR

### OCRAgent
- Initializes `easyocr.Reader(['en'], gpu=False)` **once** at agent level (not per message)
- Reads the enhanced image and joins all detected text segments
- Forwards raw text to Validator

### ValidatorAgent
- Applies `re.sub(r"[^A-Z0-9]", "", raw.upper())` to strip spaces and special characters
- Sends the cleaned plate string back to the Client

---

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `Error during connection with the server` | SPADE XMPP server not running | Run `spade run` in a separate terminal first |
| `pin_memory` UserWarning from EasyOCR | No GPU found (expected on CPU) | Safe to ignore — CPU mode works fine |
| Empty OCR result | Poor image quality or wrong crop | Check `cropped/` folder; try adjusting contrast/sharpness values |
| `FileNotFoundError: models/real_detector.pt` | YOLO checkpoint missing | Add your trained `.pt` file to the `models/` folder |

---

## Key Concepts

- **SPADE** — Python MAS framework using asynchronous XMPP messaging
- **YOLO (Ultralytics)** — object detection model used to localize the license plate bounding box
- **EasyOCR** — deep learning OCR engine used to extract text from the cropped plate
- **Pipeline architecture** — each agent handles exactly one stage; loosely coupled via messages
- **`CyclicBehaviour`** — agents listen indefinitely for incoming messages
- **`OneShotBehaviour`** — the Client uses this to send the image exactly once
