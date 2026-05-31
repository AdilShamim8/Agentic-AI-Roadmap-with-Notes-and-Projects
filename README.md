<div align="center">

# Agentic AI Roadmap with Notes & Projects

### A production-grade, hands-on curriculum for mastering Agentic AI development using LangGraph

[![GitHub Stars](https://img.shields.io/github/stars/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects?style=for-the-badge&logo=github&color=FFD700)](https://github.com/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects?style=for-the-badge&logo=github&color=4B9CD3)](https://github.com/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects/forks)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects?style=for-the-badge&color=F97316)](https://github.com/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects/commits/main)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3B82F6?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-8B5CF6?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)

<br/>

> **📅 Updated: May 2026** — Now covers MCP, A2A Protocol, LangGraph Platform, Functional API & Multi-Agent Systems at scale

<br/>

[🚀 Quick Start](#-quick-start) · [📅 Daily Curriculum](#-daily-curriculum) · [🗺️ Full Roadmap](#%EF%B8%8F-end-to-end-roadmap) · [💻 Code Samples](#-sample-code) · [📚 Resources](#-resources) · [🤝 Contribute](#-contributing)

</div>

---

## 📌 What Is This Repository?

This is a **structured, production-grade curriculum** for building sophisticated **Agentic AI systems** — from first principles to enterprise-scale deployment.

It takes you from LLM fundamentals all the way to deploying resilient, observable, multi-agent pipelines in production using **LangGraph** as the primary orchestration layer.

Unlike scattered tutorials, this roadmap gives you:

| What You Get | Why It Matters |
|---|---|
| 🗺️ **A clear 6-phase learning path** (~22–25 weeks) | Zero guesswork — you always know what's next |
| 📓 **Daily hands-on Jupyter notebooks** | Learn by building, not by reading slides |
| 🏗️ **Production-ready patterns** | Not toy demos — actual enterprise-grade architectures |
| 🔧 **2026-current content** | MCP, A2A, functional API, multi-agent systems |
| ✅ **Runnable code today** | Tested, annotated, copy-paste ready |

---

## 🎯 Who Is This For?

| Your Background | You'll Use This To |
|---|---|
| 🧑‍💻 **ML / AI Engineer** | Transition from prompting to production agents |
| 🔧 **Backend / Full-Stack Developer** | Add autonomous reasoning to your existing stack |
| 📊 **Data Scientist** | Build agents that automate complex analysis pipelines |
| 🎓 **CS Student** | Follow a structured path to AI agent development |
| 🏗️ **Tech Lead / Architect** | Understand modern agentic system design trade-offs |

**Prerequisites:**
- Python 3.10+ (comfortable with type hints and `async/await`)
- Basic familiarity with LLMs and API calls
- Optional but helpful: LangChain basics, Docker

---

## 🏆 What You'll Be Able to Build

After completing this roadmap, you'll have the skills to architect and ship:

```
├── 🤖 Single Agents         — ReAct, Plan-and-Execute, Reflexion agents
├── 🏢 Multi-Agent Systems   — Supervisor, swarm, and hierarchical orchestration
├── 🧠 Memory-Augmented AI   — Persistent memory graphs and long-term recall
├── 🔧 MCP-Powered Tools     — Standardized tool servers via Model Context Protocol
├── 🌐 Interoperable Agents  — A2A protocol for cross-framework communication
├── 🔄 Human-in-the-Loop     — Interrupt/resume patterns and approval workflows
├── 📊 Observable Systems    — LangSmith tracing, evaluation, and production monitoring
└── 🚀 Production Systems    — LangGraph Platform, Docker, auto-scaling infrastructure
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects.git
cd Agentic-AI-Roadmap-with-Notes-and-Projects

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install core dependencies
pip install langgraph langchain langchain-openai langchain-anthropic langsmith

# 4. Configure your environment
cp .env.example .env             # Edit .env with your API keys

# 5. Open Day 0 and begin
jupyter lab "Day 0 Generative AI vs Agentic AI/"
```

**Required API Keys** — add these to your `.env` file:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LANGCHAIN_API_KEY=ls__...            # Free at smith.langchain.com
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=agentic-ai-roadmap
```

> 💡 **Tip:** You can swap OpenAI models for Anthropic Claude or local Ollama models at any point — all examples use the standard LangChain interface.

---

## 📅 Daily Curriculum

Hands-on notes organized day by day. Click any folder to dive straight in.

### 🟢 Foundation Track — Getting Started

| Day | Topic | What You'll Learn |
|:---:|-------|-------------------|
| **Day 0** | [Generative AI vs Agentic AI](./Day%200%20Generative%20AI%20vs%20Agentic%20AI/) | Core distinctions, mental models, side-by-side comparison |
| **Day 1** | [What is Agentic AI?](./Day%2001%20What%20is%20Agentic%20AI/) | Definitions, key characteristics, anatomy of an agent |
| **Day 2** | [LangChain vs LangGraph](./Day%2002%20LangChain%20vs%20LangGraph/) | When to use which, architectural differences, migration guide |

### 🔵 Core Track — LangGraph Mastery

| Day | Topic | What You'll Learn |
|:---:|-------|-------------------|
| **Day 3** | [LangGraph Core Concepts](./Day%2003%20LangGraph%20Core%20Concepts/) | Nodes, edges, state, graph compilation |
| **Day 4** | [Sequential Workflows](./Day%2004%20Sequential%20Workflows%20in%20LangGraph/) | Step-by-step agent execution, linear pipelines |
| **Day 5** | [Parallel Workflows](./Day%2005%20Parallel%20Workflows%20in%20LangGraph/) | Fan-out / fan-in patterns, concurrent node execution |
| **Day 6** | [Conditional Workflows](./Day%2006%20Conditional%20Workflows%20in%20LangGraph/) | Dynamic routing, conditional edges, decision logic |
| **Day 7** | [Iterative Workflows](./Day%2007%20Iterative%20Workflows%20in%20LangGraph/) | Loops, cycles, self-correction patterns |

### 🟠 Builder Track — Real Agents

| Day | Topic | What You'll Learn |
|:---:|-------|-------------------|
| **Day 8** | [Build a Chatbot with LangGraph](./Day%2008%20How%20to%20build%20a%20Chatbot%20using%20LangGraph/) | Full conversational agent from scratch |
| **Day 9** | [Persistence in LangGraph](./Day%2009%20Persistence%20in%20LangGraph/) | Checkpointing, thread IDs, memory across sessions |

> 🔜 **Days 10–30 Coming Soon** — Multi-agent systems, MCP integration, reflexion loops, production deployment, and more.

---

## 🗺️ End-to-End Roadmap

### Roadmap Overview

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   AGENTIC AI MASTERY PATH — 22 to 25 Weeks                  ║
╠══════════════╦═════════════════╦══════════════════════╦═══════════════════════╣
║  Phase 1     ║  Phase 2        ║  Phase 3             ║  Phase 4             ║
║  Weeks 1–3   ║  Weeks 4–7      ║  Weeks 8–12          ║  Weeks 13–18         ║
║              ║                 ║                      ║                      ║
║  LLM &       ║  LangGraph      ║  Agentic Workflows   ║  Advanced Patterns   ║
║  LangChain   ║  Core Mastery   ║  Multi-Agent Systems ║  Eval & Safety       ║
║  Basics      ║                 ║                      ║                      ║
╠══════════════╩═════════╦═══════╩══════════╦═══════════╩═══════════════════════╣
║                         ║  Phase 5         ║  Phase 6                         ║
║                         ║  Weeks 19–21     ║  Weeks 22–25                     ║
║                         ║                 ║                                  ║
║                         ║  Protocols &    ║  Production & Scaling            ║
║                         ║  Interop        ║  LangGraph Platform              ║
║                         ║  MCP, A2A       ║                                  ║
╚═════════════════════════╩═════════════════╩══════════════════════════════════╝
```

---

### Phase 1: Foundations `Weeks 1–3`

**Goal:** Build a rock-solid base in LLMs, prompt engineering, and LangChain. 📚

| Topic | Key Concepts | Est. Time |
|-------|-------------|:---------:|
| **LLM Fundamentals** | Tokenization, inference, temperature, structured outputs | 3 days |
| **Prompt Engineering** | Zero/few-shot, Chain-of-Thought, Self-consistency, ReAct | 2 days |
| **LangChain Basics** | LCEL, chains, memory, tools, chat models | 4 days |
| **Python Async & State** | `asyncio`, state machines, event-driven programming | 2 days |
| **Modern LLM Landscape** | GPT-4o, Claude 3.5+, Gemini 2.0 Pro, Llama 3, Mistral | 2 days |
| **Function & Tool Calling** | JSON mode, structured outputs, tool schemas | 2 days |

**✅ Phase 1 Mini-Projects:**
- Structured Q&A chatbot with memory using LangChain
- RAG pipeline with structured JSON output
- Function-calling agent using both OpenAI and Anthropic APIs

---

### Phase 2: LangGraph Core Mastery `Weeks 4–7`

**Goal:** Deep mastery of LangGraph's architecture and both API surfaces. 🏗️

| Topic | Key Concepts | Est. Time |
|-------|-------------|:---------:|
| **Graph Architecture** | Nodes, edges, state, transitions, conditional logic | 3 days |
| **StateGraph API** | `TypedDict`/`Pydantic` state, reducers, graph compilation | 3 days |
| **Functional API** *(2026)* | `@entrypoint`, `@task` decorators, Pythonic workflows | 2 days |
| **Memory & Checkpointing** | `MemorySaver`, Postgres, episodic memory, `Store` API | 3 days |
| **Tool Integration** | `ToolNode`, connecting APIs/DBs, dynamic tool loading | 2 days |
| **Human-in-the-Loop** | `interrupt()`, `Command(resume=...)`, approval workflows | 2 days |
| **Prebuilt Agents** | `create_react_agent()` for rapid prototyping | 1 day |
| **LangGraph Studio** | Visual debugging, graph inspection, step-through execution | 2 days |
| **Streaming** | Token streaming, event streaming, production patterns | 2 days |

**✅ Phase 2 Mini-Projects:**
- Customer support agent with `StateGraph`
- Rebuild the same agent using functional API (`@entrypoint`/`@task`)
- Add persistent memory + human approval checkpoints
- Debug and visualize agent execution in LangGraph Studio

---

### Phase 3: Building Agentic Workflows `Weeks 8–12`

**Goal:** Design, build, and test advanced agentic systems. 🤖

| Topic | Key Concepts | Est. Time |
|-------|-------------|:---------:|
| **Multi-Agent Orchestration** | Supervisor, swarm, hierarchical team patterns | 4 days |
| **ReAct Agents** | Reasoning + Acting loops, self-correction | 2 days |
| **Plan-and-Execute Pattern** | Task decomposition, dynamic replanning | 3 days |
| **Reflexion Loops** | Self-review, introspection, iterative improvement, scoring | 3 days |
| **Agentic Memory Graphs** | Zettelkasten-style linking, semantic memory, retrieval | 3 days |
| **Map-Reduce Agents** | Fan-out/fan-in, parallel processing patterns | 2 days |
| **Agent Handoffs** | Transferring control between specialized agents | 2 days |
| **Subgraph Composition** | Nesting graphs, modularity, reusable components | 2 days |

**✅ Phase 3 Mini-Projects:**
- Plan-and-execute document analyst with reflexion
- Multi-agent workflow: supervisor → researcher → analyst → writer
- Map-reduce agent for parallel document processing
- Long-term memory agent using the LangGraph `Store` API

---

### Phase 4: Advanced Agentic Patterns `Weeks 13–18`

**Goal:** Master enterprise-grade and cutting-edge agent architectures. 🚀

| Topic | Key Concepts | Est. Time |
|-------|-------------|:---------:|
| **Adaptive Deliberation** | Fast/slow reasoning, thinking budgets, context switching | 3 days |
| **Self-Improving Agents** | Error learning, experience replay, memory-enhanced iteration | 3 days |
| **Governed Tool Use** | Permissions, audit logs, safety constraints, guardrails | 3 days |
| **Complex Branching & Cycles** | Non-linear graphs, parallel/sequential, dynamic routing | 3 days |
| **Multimodal Agents** | Text + images + audio + video in agent workflows | 3 days |
| **Enterprise Compliance** | Audit trails, PII handling, data privacy, compliance layers | 2 days |
| **Agent Evaluation** | LangSmith evals, benchmarking, regression testing suites | 3 days |
| **Background & Cron Agents** | Long-running tasks, scheduled agent execution | 2 days |

**✅ Phase 4 Mini-Projects:**
- Self-improving code review agent with reflexion + persistent learning
- Governed multi-tool workflow for regulated domains (healthcare/finance)
- Multimodal document processor (text + embedded images)
- Full evaluation suite using LangSmith datasets and evaluators

---

### Phase 5: Agent Protocols & Interoperability `Weeks 19–21`

**Goal:** Master MCP and A2A — the open protocols powering the next generation of agents. 🌐

> 🆕 **Critical Phase (2026):** The industry has converged on these two protocols as the standard connective tissue of the agentic ecosystem.

| Topic | Key Concepts | Est. Time |
|-------|-------------|:---------:|
| **Model Context Protocol (MCP)** | MCP servers/clients, tool discovery, resource access | 3 days |
| **MCP with LangGraph** | `@tool` + MCP servers, dynamic tool loading, registries | 2 days |
| **Agent-to-Agent (A2A) Protocol** | Agent Cards, task lifecycle, inter-agent messaging | 3 days |
| **A2A with LangGraph** | Exposing + consuming agents via A2A | 2 days |
| **Cross-Framework Interop** | LangGraph ↔ OpenAI Agents SDK ↔ CrewAI bridges | 2 days |
| **Tool Registries & Discovery** | Dynamic registration, capability catalogs, versioning | 1 day |

**✅ Phase 5 Mini-Projects:**
- MCP tool server + LangGraph agent integration from scratch
- LangGraph agent exposing itself via an A2A Agent Card
- Multi-framework pipeline: LangGraph supervising OpenAI Agents SDK agents
- Dynamic tool discovery agent that finds and uses MCP tools at runtime

---

### Phase 6: Production & Scaling `Weeks 22–25`

**Goal:** Deploy, monitor, and scale agentic AI systems that never sleep. ⚙️

| Topic | Key Concepts | Est. Time |
|-------|-------------|:---------:|
| **LangGraph Platform** | Managed deployment, Assistants API, cron, store management | 3 days |
| **Checkpointing & Reliability** | Save/restore state, error handling, retries, durable execution | 2 days |
| **LangSmith Monitoring** | Tracing, dashboards, alerting, production observability | 2 days |
| **Deployment Options** | LangGraph Cloud, self-hosted Docker, FastAPI, Kubernetes | 3 days |
| **Scaling Multi-Agent Systems** | Distributed agents, load balancing, async execution | 3 days |
| **Continuous Improvement** | Feedback loops, A/B testing, online eval, agent versioning | 2 days |
| **Security & Access Control** | API key management, RBAC, secrets management | 1 day |
| **Cost Optimization** | Token budgeting, model routing, intelligent caching | 2 days |

**✅ Phase 6 Mini-Projects:**
- Production agent API on LangGraph Platform with full LangSmith monitoring
- Automated feedback pipeline for continuous agent quality improvement
- Cost-optimized model router (GPT-4o for complex tasks, GPT-4o-mini for simple ones)
- Production multi-agent system with health checks, retries, and alerting

---

## 🌐 Agentic AI Ecosystem Landscape (2026)

> 💡 **Architecture Insight:** The industry has converged on **LangGraph** (orchestration) + **MCP** (tool interop) + **A2A** (agent interop) + **LangSmith** (eval & monitoring) as the reference stack for enterprise-grade agentic AI.

| Framework / Protocol | Type | Core Strengths | Best For |
|---|---|---|---|
| **LangGraph** | Orchestration Framework | Stateful graphs, memory, HITL, production infrastructure | Complex, stateful, production agent systems |
| **OpenAI Agents SDK** | Agent Framework | Native OpenAI integration, Guardrails, Handoffs, Tracing | OpenAI-native applications |
| **CrewAI** | Multi-Agent Framework | Role-based agents, simple API, fast prototyping | Quick multi-agent prototypes |
| **AutoGen (Microsoft)** | Multi-Agent Framework | Conversational agents, group chat patterns | Research & conversational multi-agent |
| **MCP (Anthropic)** | Open Protocol | Standardized tool/context integration, cross-framework | Universal tool access for any agent framework |
| **A2A (Google)** | Open Protocol | Inter-agent comms, Agent Cards, task lifecycle | Cross-framework agent collaboration |
| **LangSmith** | Observability & Eval | Tracing, evaluation datasets, dashboards, monitoring | Agent debugging, testing, production monitoring |
| **LangGraph Platform** | Managed Infrastructure | Deployment, scaling, cron jobs, Assistants API | Production deployment of LangGraph agents |

---

## 💡 Project Ideas

Build these to consolidate your skills. Ordered from beginner to expert:

| # | Project | Description | Stack | Difficulty |
|:--:|---------|-------------|-------|:----------:|
| 1 | **Smart Research Assistant** | Multi-source web research + synthesis via MCP search tools | LangGraph + MCP | ⭐⭐ |
| 2 | **Multi-Agent Customer Support** | Router → retriever → responder with human escalation | LangGraph multi-agent | ⭐⭐⭐ |
| 3 | **Personal Knowledge Manager** | Memory graph assistant with Zettelkasten-style long-term recall | LangGraph + Store API | ⭐⭐⭐ |
| 4 | **Agentic Workflow Automator** | Business process automation (invoice processing, data pipelines) | LangGraph + governed tools | ⭐⭐⭐ |
| 5 | **Multimodal Document Analyst** | Process PDFs, images, tables → generate structured reports | LangGraph multimodal | ⭐⭐⭐ |
| 6 | **Self-Healing Code Agent** | Detects, diagnoses, and fixes bugs with reflexion + test execution | LangGraph + Reflexion | ⭐⭐⭐⭐ |
| 7 | **MCP Universal Agent** | Dynamically discovers and uses tools from any MCP server | LangGraph + MCP | ⭐⭐⭐⭐ |
| 8 | **Real-Time Anomaly Monitor** | Monitors data streams, detects anomalies, triggers automated responses | LangGraph async | ⭐⭐⭐⭐ |
| 9 | **Cross-Framework Agent Network** | LangGraph agents collaborating with OpenAI Agents SDK via A2A | LangGraph + A2A | ⭐⭐⭐⭐⭐ |
| 10 | **Agent-as-a-Service Platform** | Deploy multiple discoverable agents with A2A Agent Cards + management UI | LangGraph Platform | ⭐⭐⭐⭐⭐ |

---

## 🔥 Key Trends (2026)

| Trend | Signal | What to Watch |
|---|---|---|
| **Protocol Convergence** | MCP + A2A becoming universal standards | Framework-agnostic tool & agent integration |
| **Multi-Agent at Scale** | 5–20+ specialized agents per enterprise deployment | Supervisor/swarm replacing monolithic agents |
| **Memory as Infrastructure** | Persistent graphs beyond simple vector search | Context-aware, truly long-running autonomous systems |
| **Evaluation is Non-Negotiable** | LangSmith evals gating every production deployment | Automated quality gates for autonomous AI decisions |
| **Governed Execution** | Finance, healthcare, legal demanding full audit trails | HITL + permissioned tools driving enterprise adoption |
| **Cost-Aware Agent Design** | Model routing + token budgeting at design time | 40–60% cost reduction in production agent systems |
| **Multimodal Goes Mainstream** | Text + image + audio agents shipping to production | Richer inputs enabling substantially more capable systems |
| **Agent Marketplaces Emerging** | Early A2A Agent Cards + MCP tool discovery platforms | Reusable, composable agent components as a service |

> *"Over 55% of enterprise AI projects now include agentic capabilities, up from 40% at the start of 2026."*

> *"MCP adoption grew 300% in Q1 2026 as tool standardization became a top priority for AI teams."*

---

## 💻 Sample Code

### 1. Quickstart — ReAct Agent with Tools

The fastest path to a working agent:

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web for current information."""
    return f"[Search result for: {query}] — LangGraph is the leading agentic AI framework."

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {e}"

llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_react_agent(llm, tools=[web_search, calculator])

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is LangGraph? Also, what is 42 * 17?"}]
})

for msg in result["messages"]:
    print(f"[{msg.type.upper()}]: {msg.content}")
```

---

### 2. Custom StateGraph Agent (Full Control)

```python
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return f"[Simulated search result for: {query}]"

tools = [web_search]
llm = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)
tool_node = ToolNode(tools)

def call_llm(state: AgentState):
    return {"messages": [llm.invoke(state["messages"])]}

def should_use_tool(state: AgentState):
    return "tools" if state["messages"][-1].tool_calls else END

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("tools", tool_node)
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_use_tool)
graph.add_edge("tools", "llm")

agent = graph.compile(checkpointer=MemorySaver())

# Thread-scoped persistent memory
config = {"configurable": {"thread_id": "user-001"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is LangGraph?"}]},
    config=config
)
print(result["messages"][-1].content)
```

---

### 3. Functional API Agent *(2026 Pattern)*

Simpler syntax for linear and checkpoint-heavy workflows:

```python
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

@task
def research(topic: str) -> str:
    return llm.invoke(f"Research this topic thoroughly: {topic}").content

@task
def summarize(text: str) -> str:
    return llm.invoke(f"Summarize this concisely:\n\n{text}").content

@entrypoint(checkpointer=MemorySaver())
def research_agent(topic: str) -> str:
    """Durable research pipeline with automatic checkpointing."""
    raw = research(topic).result()
    return summarize(raw).result()

result = research_agent.invoke(
    "Latest advances in multi-agent AI systems",
    config={"configurable": {"thread_id": "research-001"}}
)
print(result)
```

---

### 4. Multi-Agent Supervisor Pattern

```python
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"[Web results for: {query}]"

@tool
def analyze_data(data: str) -> str:
    """Analyze data and extract key insights."""
    return f"[Analysis]: Positive trend detected in {data}."

@tool
def write_report(content: str) -> str:
    """Format content as a structured report."""
    return f"# Report\n\n{content}\n\n*Generated by AI Agent*"

llm = ChatOpenAI(model="gpt-4o", temperature=0)

researcher = create_react_agent(llm, tools=[search_web],
                                 prompt="You are a research specialist.")
analyst    = create_react_agent(llm, tools=[analyze_data],
                                 prompt="You are a data analyst.")
writer     = create_react_agent(llm, tools=[write_report],
                                 prompt="You are a technical writer.")

class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str

def supervisor(state: SupervisorState):
    response = llm.invoke([
        {"role": "system", "content":
         "You are a supervisor. Choose the next agent: 'researcher', 'analyst', "
         "'writer', or 'FINISH'. Reply with ONLY the agent name."},
        *state["messages"]
    ])
    return {"next_agent": response.content.strip()}

def route(state: SupervisorState) -> Literal["researcher", "analyst", "writer", "__end__"]:
    return "__end__" if state["next_agent"] == "FINISH" else state["next_agent"]

graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", lambda s: researcher.invoke(s))
graph.add_node("analyst",    lambda s: analyst.invoke(s))
graph.add_node("writer",     lambda s: writer.invoke(s))
graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route)
for node in ["researcher", "analyst", "writer"]:
    graph.add_edge(node, "supervisor")

workflow = graph.compile()
result = workflow.invoke({
    "messages": [{"role": "user",
                  "content": "Research LangGraph trends, analyze them, then write a report."}],
    "next_agent": ""
})
```

---

### 5. Human-in-the-Loop with `interrupt()`

```python
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    approved: bool

def generate_action(state: State):
    return {"messages": [{"role": "assistant",
                          "content": "I'd like to send an email to the client. Do you approve?"}]}

def human_review(state: State):
    decision = interrupt({"question": "Approve this action?", "options": ["yes", "no"]})
    return {"approved": decision == "yes"}

def execute_action(state: State):
    msg = "✅ Email sent successfully!" if state["approved"] else "❌ Action cancelled by human."
    return {"messages": [{"role": "assistant", "content": msg}]}

graph = StateGraph(State)
graph.add_node("generate", generate_action)
graph.add_node("review",   human_review)
graph.add_node("execute",  execute_action)
graph.add_edge(START, "generate")
graph.add_edge("generate", "review")
graph.add_edge("review",   "execute")
graph.add_edge("execute",  END)

agent  = graph.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "approval-001"}}

# Step 1: Run until interrupt — agent pauses awaiting human input
result = agent.invoke({"messages": [], "approved": False}, config=config)

# Step 2: Human decides → resume execution
result = agent.invoke(Command(resume="yes"), config=config)
print(result["messages"][-1]["content"])
```

---

### 6. MCP Tool Integration *(Connect to Any Tool Server)*

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def build_mcp_agent():
    async with MultiServerMCPClient({
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"],
        },
        "web_search": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-brave-search"],
            "env": {"BRAVE_API_KEY": "your-api-key"},
        },
    }) as mcp_client:
        tools  = mcp_client.get_tools()
        llm    = ChatOpenAI(model="gpt-4o", temperature=0)
        agent  = create_react_agent(llm, tools=tools)

        return await agent.ainvoke({
            "messages": [{
                "role": "user",
                "content": "Search for LangGraph news and save a summary to notes.txt"
            }]
        })

result = asyncio.run(build_mcp_agent())
```

---

## 📚 Resources

### Official Documentation

| Resource | What It Covers |
|----------|---------------|
| [LangGraph Docs](https://langchain-ai.github.io/langgraph/) | Core framework reference |
| [LangGraph Functional API](https://langchain-ai.github.io/langgraph/concepts/functional_api/) | `@entrypoint` / `@task` patterns |
| [LangGraph MCP Integration](https://langchain-ai.github.io/langgraph/mcp/) | Connecting to MCP servers |
| [LangChain Docs](https://python.langchain.com/docs/introduction/) | Underlying library reference |
| [LangSmith Docs](https://docs.smith.langchain.com/) | Tracing, evaluation, monitoring |
| [LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/) | Production deployment guide |

### Open Protocols

| Protocol | Specification | GitHub |
|----------|--------------|--------|
| **MCP** (Model Context Protocol) | [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io/) | [modelcontextprotocol](https://github.com/modelcontextprotocol) |
| **A2A** (Agent-to-Agent) | [google.github.io/A2A](https://google.github.io/A2A/) | [google/A2A](https://github.com/google/A2A) |

### Courses & Tutorials

| Course | Platform | Focus |
|--------|----------|-------|
| [Intro to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) | LangChain Academy | Core LangGraph concepts |
| [Multi-Agent Systems](https://academy.langchain.com/courses/multi-agent-systems) | LangChain Academy | Multi-agent architecture patterns |
| [AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) | DeepLearning.AI | Practical agent building |
| [Build AI Agents 10x Faster 2026](https://www.udemy.com/course/build-ai-agents-agentic-2026-python-langchain-langgraph/) | Udemy | Full production course |

### Research Papers (Essential Reading)

| Paper | Why It Matters |
|-------|---------------|
| [ReAct (2022)](https://arxiv.org/abs/2210.03629) | Foundational Reasoning + Acting pattern — every agent uses this |
| [Reflexion (2023)](https://arxiv.org/abs/2303.11366) | Self-improving agents via verbal reinforcement learning |
| [Tree of Thoughts (2023)](https://arxiv.org/abs/2305.10601) | Deliberate, structured problem solving |
| [LATS (2023)](https://arxiv.org/abs/2310.04406) | Language Agent Tree Search for complex planning |
| [Agent-as-a-Judge (2024)](https://arxiv.org/abs/2410.10934) | Using agents to evaluate agents at scale |

### Tools & Platforms

| Tool | Purpose |
|------|---------|
| [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) | Visual IDE for agent debugging and inspection |
| [LangSmith](https://smith.langchain.com/) | Tracing, evaluation datasets, production monitoring |
| [LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/) | Managed agent deployment infrastructure |
| [MCP Server Registry](https://github.com/modelcontextprotocol/servers) | Pre-built, ready-to-use MCP tool servers |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get involved:

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/day-10-multi-agent-notes`
3. **Commit your changes**: `git commit -m "Add Day 10: Multi-Agent Supervisor Pattern with examples"`
4. **Push**: `git push origin feature/day-10-multi-agent-notes`
5. **Open a Pull Request** — describe what you added and why

**We're especially looking for:**
- New daily notes (Days 10 and beyond)
- Code improvements, bug fixes, or updated API usage
- Additional project implementations with solutions
- New resource recommendations (papers, tools, courses)
- Clarifications, corrections, and typo fixes

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines and conventions.

---

## ❓ FAQ

**Q: What Python version do I need?**  
A: Python 3.10 or higher. Python 3.12 is recommended for best compatibility.

**Q: Do I need a paid OpenAI account?**  
A: The examples use OpenAI models by default, but all code uses standard LangChain interfaces — you can swap in Anthropic Claude, local Ollama models, Gemini, or any other supported provider with minimal changes.

**Q: How long does this roadmap take?**  
A: Approximately 22–25 weeks at 2–3 hours per day. Move faster or slower depending on your experience — the phases are checkpoints, not deadlines.

**Q: Is this suitable for complete beginners?**  
A: Phase 1 assumes basic Python proficiency and some familiarity with LLMs. If you're starting from scratch, build some Python + LLM fundamentals first, then return here.

**Q: How is this different from the official LangGraph documentation?**  
A: Official docs are reference material. This roadmap provides a *structured learning path* with curated context, annotated code, project-based milestones, and progression through concepts in the right order.

**Q: Can I use this for company / team training?**  
A: Absolutely — it's MIT licensed. Attribution appreciated but not required.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for full details.

---

## 👤 Author

<div align="center">

**Adil Shamim**
AI/ML Engineer · Agentic Systems Builder

[![Website](https://img.shields.io/badge/Website-adilshamim.me-3B82F6?style=for-the-badge&logo=safari&logoColor=white)](https://adilshamim.me/)
[![GitHub](https://img.shields.io/badge/GitHub-AdilShamim8-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AdilShamim8)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-AdilShamim8-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adilshamim8)

*Have a question, idea, or found something broken? [Open an issue](https://github.com/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects/issues) — I read and respond to all of them.*

</div>

---

<div align="center">

### ⭐ If this roadmap helped you, please give it a star — it helps others discover it!

[![Star on GitHub](https://img.shields.io/github/stars/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects?style=social)](https://github.com/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects/stargazers)

*Built with for the Agentic AI community*

</div>
