# 🧠 BrowserMind — Agentic AI Research Platform

**A multi-agent AI research application powered by LangGraph, Playwright, Ollama, and FastAPI.**

BrowserMind transforms research questions into structured research workflows. It uses specialized agents to plan investigations, collect website evidence, generate comparative analyses, and assess whether conclusions are supported by retrieved sources.

## ✨ Features

- **AI Research Planner:** Generates question-specific research tasks using Llama 3.2.
- **Browser Research Agent:** Collects webpage information using Playwright.
- **Research Analyst:** Synthesizes evidence into research summaries.
- **Verification Agent:** Evaluates whether generated conclusions are supported by collected evidence.
- **LangGraph Orchestration:** Coordinates the research workflow across specialized nodes.
- **Real-Time Agent Tracking:** Streams agent completion events using Server-Sent Events.
- **Interactive Dashboard:** Provides a web interface for research questions, results, and source links.
- **Session Tracking:** Assigns unique identifiers to research requests.
- **Health Monitoring:** Checks FastAPI and Ollama availability.
- **Retry Handling:** Retries selected temporary model connection failures.

## 🏗️ System Architecture

```text
             User Research Question
                       |
                       v
              LangGraph Workflow
                       |
                       v
                Planner Agent
                       |
                       v
              Browser Research Agent
                  (Playwright)
                       |
                       v
                Research Analyst
                 (Llama 3.2)
                       |
                       v
               Verification Agent
                       |
                       v
               FastAPI Backend
                       |
                       v
                Web Dashboard
```

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Agent Orchestration | LangGraph |
| LLM | Llama 3.2 via Ollama |
| LLM Integration | LangChain, LangChain-Ollama |
| Browser Automation | Playwright, Chromium |
| Backend | FastAPI, Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Live Updates | Server-Sent Events |
| Validation | Pydantic |
| Data Storage | Local JSON files (prototype) |
| Version Control | Git, GitHub |

## 📁 Project Structure

```text
browsermind/
├── api.py
├── browser_agent.py
├── research_extractor.py
├── multi_research.py
├── planner_agent.py
├── research_workflow.py
├── research_analyst.py
├── verification_agent.py
├── multi_agent_system.py
├── frontend/
│   └── index.html
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or newer
- Ollama
- Git
- Playwright-compatible Chromium

### 1. Clone the repository

```bash
git clone https://github.com/jp1109/BrowserMind.git
cd BrowserMind
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install langgraph langchain-core langchain-ollama pydantic playwright python-dotenv fastapi "uvicorn[standard]" httpx
python -m playwright install chromium
```

### 4. Set up Ollama

Install Ollama, then download the model:

```bash
ollama pull llama3.2:3b
```

Ensure Ollama is running. If the Ollama service is not already active:

```bash
ollama serve
```

### 5. Start BrowserMind

In a separate terminal:

```bash
source .venv/bin/activate
python -m uvicorn api:app --reload
```

Open the application:

**Dashboard:** http://127.0.0.1:8000/dashboard

**API Documentation:** http://127.0.0.1:8000/docs

**Health Check:** http://127.0.0.1:8000/health

## 🔬 Example Research Question

> How do LangGraph and CrewAI differ in multi-agent orchestration, memory management, fault tolerance, and production scalability?

BrowserMind generates a research plan, collects information from configured documentation websites, produces a comparative analysis, and evaluates the supporting evidence.

## 🔐 Current Limitations

BrowserMind is an active development project, not yet a fully production-hardened service.

- Research currently uses a predefined list of approved websites.
- Verification is LLM-based and does not independently guarantee factual accuracy.
- Reports are currently exchanged through local JSON files.
- Session IDs support tracking but do not yet provide isolated persistent storage.
- Local Ollama inference can be slow depending on hardware.
- Authentication, rate limiting, comprehensive tests, and deployment security are planned.

## 🗺️ Roadmap

- [x] Browser automation with Playwright
- [x] AI-powered research planning
- [x] LangGraph multi-agent workflow
- [x] Evidence-based research analysis
- [x] Initial verification agent
- [x] FastAPI backend
- [x] Interactive research dashboard
- [x] Agent progress streaming
- [x] Health checks
- [ ] Per-session report storage
- [ ] Dynamic source discovery
- [ ] Claim-level citation verification
- [ ] Automated integration tests
- [ ] Docker containerization
- [ ] Authentication and rate limiting
- [ ] Production deployment

## 👩‍💻 Author

**Janhavi Patil**

Data Science | AI Engineering | Agentic AI

- [GitHub](https://github.com/jp1109)
- [Portfolio](https://jp1109.github.io/personal-portfolio/)

---

*BrowserMind — Research with AI agents, grounded in evidence.*
