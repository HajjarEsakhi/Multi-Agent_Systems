# TP02 : ACL Communication in JADE (Java)

> **Course:** Multi-Agent Systems | UEMF / EIDIA  
> **Author:** Esakhi Hajjar | AI Engineering – 2nd Year  
> **Professor:** Pr. Abderrahim Waga  
> **Date:** February 17, 2026

---

## Overview

This lab implements **Agent Communication Language (ACL)** messaging in JADE (Java Agent DEvelopment Framework), covering four progressive communication patterns — from simple one-way messaging to a full negotiation protocol with decision making.

---

## Project Structure

```
TP2_ACL_Communication/
├── src/
│   └── eu/uemf/agents/
│       ├── AgentA.java               # Ex1 — Sender (unidirectional)
│       ├── AgentB.java               # Ex1 — Receiver (unidirectional)
│       ├── AgentA_Ex2.java           # Ex2 — Requester (bidirectional)
│       ├── AgentB_Ex2.java           # Ex2 — Responder (bidirectional)
│       ├── CoordinatorAgent.java     # Ex3 — Coordinates two experts
│       ├── Expert1.java              # Ex3 — Expert agent 1
│       ├── Expert2.java              # Ex3 — Expert agent 2
│       ├── BuyerAgent.java           # Ex4 — Negotiation buyer
│       ├── Seller1.java              # Ex4 — Seller with price 500
│       └── Seller2.java              # Ex4 — Seller with price 450
└── README.md
```

---

## Prerequisites

- Java JDK 8+ (Java 9+ module system must be disabled — see troubleshooting)
- Eclipse IDE
- JADE 4.6.0 (`jade.jar` added to build path)

---

## Setup

### 1. Add JADE to the project

In Eclipse: `Right-click project → Build Path → Add External JARs → select jade.jar`

### 2. Disable Java module system (if on Java 9+)

Delete `module-info.java` from the `src` folder if it was auto-generated. JADE is incompatible with the Java module system.

### 3. Configure run arguments

For each exercise, go to: `Run → Run Configurations → Arguments → Program arguments` and paste the command from the exercise below.

---

## Exercises

---

### Exercise 1 — Unidirectional Communication

Agent A sends a single `INFORM` message to Agent B. No reply is expected.

**Pattern:** `OneShotBehaviour` (Sender) + `CyclicBehaviour` (Listener)

**Run arguments:**
```
-gui agentB:eu.uemf.agents.AgentB;agentA:eu.uemf.agents.AgentA
```

**Expected output:**
```
Agent A is starting...
Agent B is ready and listening...
Agent A sent: Hello B!
Agent B received: Hello B!
From: agentA
```

---

### Exercise 2 — Bidirectional Communication

Agent A sends a `REQUEST`, Agent B processes it and replies with an `INFORM`. Agent A waits for the reply using a step-based `Behaviour`.

**Pattern:** `REQUEST` → `INFORM` reply using `createReply()`

**Run arguments:**
```
-gui -local-port 1100 agentB:eu.uemf.agents.AgentB_Ex2;agentA:eu.uemf.agents.AgentA_Ex2
```

**Expected output:**
```
Agent A (Ex2) is starting...
Agent B (Ex2) is ready and listening...
Agent A sent REQUEST: What is the temperature?
Agent B received: What is the temperature?
Agent B sent reply: It is 25°C.
Agent A received reply: It is 25°C.
```

---

### Exercise 3 — Coordination of 3 Agents

A Coordinator sends tasks to two Expert agents and waits for both replies before concluding. Uses a reply counter to track completion.

**Pattern:** `OneShotBehaviour` (dispatch) + `CyclicBehaviour` (collect replies)

**Run arguments:**
```
-gui -local-port 1101 coordinator:eu.uemf.agents.CoordinatorAgent;expert1:eu.uemf.agents.Expert1;expert2:eu.uemf.agents.Expert2
```

**Expected output:**
```
Coordinator is starting...
Expert 1 is ready...
Expert 2 is ready...
Coordinator sent task to Expert 1
Coordinator sent task to Expert 2
Expert 1 received: Task for Expert 1
Expert 2 received: Task for Expert 2
Expert 1 sent reply
Expert 2 sent reply
Coordinator received reply 1: Expert 2 completed the task
Coordinator received reply 2: Expert 1 completed the task
✓ All replies received!
```

---

### Exercise 4 — Decision Making & Negotiation

A Buyer sends a `CFP` (Call For Proposal) to two Sellers, collects their price proposals, picks the cheapest, and sends `ACCEPT_PROPOSAL` to the winner and `REJECT_PROPOSAL` to the loser.

**Pattern:** Contract Net Protocol — `CFP` → `PROPOSE` → `ACCEPT/REJECT`

**Run arguments:**
```
-gui -local-port 1102 buyer:eu.uemf.agents.BuyerAgent;seller1:eu.uemf.agents.Seller1;seller2:eu.uemf.agents.Seller2
```

**Expected output:**
```
Buyer is starting negotiation...
Seller 1 is ready (Price: 500)
Seller 2 is ready (Price: 450)
Buyer sent CFP to both sellers
Seller 1 received CFP
Seller 2 received CFP
Seller 1 proposed: 500
Seller 2 proposed: 450
Buyer received proposal from seller1: 500
Buyer received proposal from seller2: 450

Buyer compared prices. Best price: 450
Winner: seller2

✗ Seller 1: My proposal was rejected.
✓ Seller 2: Hooray, I won the deal!
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot bind server socket to port 1099` / `No ICP active` | Previous JADE instance still running on port 1099 | Stop previous run in Eclipse console, kill `java.exe` in Task Manager, or add `-local-port [number]` to use a different port |
| `Could not find or load main class jade.Boot` | Eclipse auto-generated `module-info.java` incompatible with JADE | Delete `module-info.java` from `src/` folder |

---

## ACL Performatives Used

| Performative | Used In | Meaning |
|---|---|---|
| `INFORM` | Ex1, Ex2 | Share information |
| `REQUEST` | Ex2, Ex3 | Ask another agent to perform an action |
| `CFP` | Ex4 | Call For Proposal — open a negotiation |
| `PROPOSE` | Ex4 | Submit a proposal (price) |
| `ACCEPT_PROPOSAL` | Ex4 | Accept the best offer |
| `REJECT_PROPOSAL` | Ex4 | Decline a losing offer |

---

## Key Concepts

- **ACL (Agent Communication Language)** — FIPA-standard language for inter-agent messaging, built around *performatives* that express the intent of a message
- **OneShotBehaviour** — executes once then terminates
- **CyclicBehaviour** — loops indefinitely, listening for new messages
- **`block()`** — suspends a behaviour until a new message arrives (avoids busy-waiting)
- **`createReply()`** — automatically addresses a reply to the original sender
- **`MessageTemplate`** — filters incoming messages by performative, sender, or content
- **Contract Net Protocol** — standard negotiation pattern: CFP → proposals → accept/reject
