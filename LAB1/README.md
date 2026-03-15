# TP01 — Hello Agent with SPADE (Python)

> **Course:** Multi-Agent Systems | UEMF / EIDIA  
> **Author:** Esakhi Hajjar | AI Engineering – 2nd Year  
> **Professor:** Pr. Abderrahim Waga  
> **Date:** February 16, 2026

---

## Overview

This is the Python implementation of a basic "Hello World" agent using the **SPADE** (Smart Python Agent Development Environment) framework. The agent starts up, prints its identity information, and shuts down gracefully — demonstrating the core agent lifecycle in SPADE.

---

## File

```
TP1_SPADE/
├── hello_agent.py      # Main agent implementation
└── README.md           # This file
```

---

## Prerequisites

- Python 3.8+
- SPADE library

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

### 2. Install SPADE

```bash
pip install spade
```

### 3. Start the SPADE XMPP server

SPADE agents require a running XMPP server. Open a **separate terminal** and run:

```bash
spade run
```

Leave this terminal open — the server must stay running.

### 4. Run the agent

In your main terminal:

```bash
python hello_agent.py
```

---

## Expected Output

```
Program starting...

Creating agent...
Starting agent...
Agent starting up...
Agent started. Waiting for completion...

=== AGENT OUTPUT ===
Hello World! I am a SPADE Agent.
My JID (identifier) is: myagent@localhost
Agent is running: True
===================

Stopping agent...
Agent stopped successfully!

Program finished.
```

---

## How It Works

The agent uses a `OneShotBehaviour` , a behaviour that runs **exactly once** then stops:

```
Agent starts (setup())
    └── HelloBehaviour.run()
            ├── Print identity info
            └── Call agent.stop()
Agent shuts down
```

| Component | Role |
|-----------|------|
| `HelloAgent` | The agent class, inherits from SPADE's `Agent` |
| `HelloBehaviour` | A `OneShotBehaviour` that prints info and stops the agent |
| `setup()` | Entry point called on agent start — registers the behaviour |
| `spade.run()` | Starts the asyncio event loop and launches the agent |

---

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `Exception in the event loop: Error during the connection with the server` | No XMPP server running | Run `spade run` in a separate terminal first |
| `asyncio` event loop errors on Windows | Windows default event loop policy | Already handled in code with `WindowsSelectorEventLoopPolicy` |

---

## Key Concepts

- **SPADE Agent** — autonomous entity identified by a JID (Jabber ID)
- **OneShotBehaviour** — runs once and terminates (vs. `CyclicBehaviour` which loops forever)
- **asyncio** — SPADE is fully asynchronous; all agent methods use `async/await`
- **XMPP** — the communication protocol SPADE uses for agent messaging
