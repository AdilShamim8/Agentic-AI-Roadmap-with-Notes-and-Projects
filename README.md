# Agentic AI Roadmap with Notes Using LangGraph

<p align="center">
  <a href="https://langchain-ai.github.io/langgraph/">
    <img src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/dark/langgraph.png" alt="LangGraph Logo" width="200"/>
  </a>
</p>

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/AdilShamim8/Agentic-AI-Roadmap-with-Notes-Using-LangGraph?style=social)
![GitHub forks](https://img.shields.io/github/forks/AdilShamim8/Agentic-AI-Roadmap-with-Notes-Using-LangGraph?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/AdilShamim8/Agentic-AI-Roadmap-with-Notes-Using-LangGraph)
![License](https://img.shields.io/github/license/AdilShamim8/Agentic-AI-Roadmap-with-Notes-Using-LangGraph)

**Last Updated: March 24, 2026**

</div>

## Table of Contents

- [Introduction](#introduction)
- [What is Agentic AI?](#what-is-agentic-ai)
- [Why LangGraph for Agentic AI?](#why-langgraph-for-agentic-ai)
- [Agentic AI Ecosystem Landscape (2026)](#agentic-ai-ecosystem-landscape-2026)
- [End-to-End Agentic AI Roadmap](#end-to-end-agentic-ai-roadmap)
  - [Phase 1: Foundations (2-3 weeks)](#phase-1-foundations-2-3-weeks)
  - [Phase 2: LangGraph Core Mastery (3-4 weeks)](#phase-2-langgraph-core-mastery-3-4-weeks)
  - [Phase 3: Building Agentic Workflows (4-5 weeks)](#phase-3-building-agentic-workflows-4-5-weeks)
  - [Phase 4: Advanced Agentic Patterns (4-6 weeks)](#phase-4-advanced-agentic-patterns-4-6-weeks)
  - [Phase 5: Agent Protocols & Interoperability (2-3 weeks)](#phase-5-agent-protocols--interoperability-2-3-weeks)
  - [Phase 6: Production & Scaling (3-4 weeks)](#phase-6-production--scaling-3-4-weeks)
- [Project Ideas](#project-ideas)
- [Key 2026 Trends (Updated March 2026)](#key-2026-trends-updated-march-2026)
- [Top Resources](#top-resources)
- [Sample Code](#sample-code)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

This roadmap provides a structured, hands-on path for mastering **Agentic AI** development using **LangGraph**. It's designed for developers who want to build production-grade autonomous AI systems—agents that plan, reason, use tools, persist memory, collaborate in multi-agent architectures, and communicate across frameworks via open protocols like **MCP** and **A2A**.

> 🔄 **March 2026 Update:** This roadmap now covers the **Model Context Protocol (MCP)**, **Agent-to-Agent (A2A) Protocol**, **LangGraph Platform & Studio**, **OpenAI Agents SDK interoperability**, **agent evaluation with LangSmith**, and the latest LangGraph functional API patterns.

---

## What is Agentic AI?

**Agentic AI** refers to systems that can autonomously reason, plan, and take actions to accomplish goals without explicit step-by-step instructions. Key characteristics:

- 🧠 **Reasoning:** Deliberative problem solving (fast & slow thinking)
- 🔄 **Self-improvement:** Reflexion/self-critique loops with persistent learning
- 🔧 **Tool Use:** Integrating APIs, databases, web search via standardized protocols (MCP)
- 🤝 **Multi-Agent Collaboration:** Teams of specialized agents communicating via open standards (A2A)
- 🧲 **Persistent Memory:** Long-term, context-aware knowledge with memory graphs
- 🛡️ **Governed Execution:** Safe, compliant, auditable tool invocation
- 🌐 **Interoperability:** Cross-framework agent communication and tool sharing

---

## Why LangGraph for Agentic AI?

**LangGraph** is a stateful orchestration framework designed for building agentic workflows. It extends LangChain with:

- **Graph-based workflows:** Model complex agent behaviors as state machines
- **Dual API surface:** Both the class-based `StateGraph` API and the new **functional API** (`@entrypoint` / `@task`)
- **Multi-agent support:** Compose specialized agents with supervisor, swarm, and hierarchical patterns
- **Persistent memory graphs:** Store and recall experiences atomically with Zettelkasten-style linking
- **Reflexion loops:** Built-in support for agent self-improvement
- **MCP integration:** Native support for the Model Context Protocol for standardized tool access
- **Human-in-the-loop:** `interrupt()` / `Command(resume=...)` patterns for human oversight
- **LangGraph Platform:** Managed infrastructure for deploying agent APIs at scale
- **LangGraph Studio:** Visual IDE for debugging, inspecting, and testing agent graphs
- **Production features:** Checkpointing, tracing (via LangSmith), error handling, streaming

> **March 2026**: LangGraph now supports adaptive deliberation, the functional API, native MCP tool servers, A2A protocol bridges, and deep LangSmith integration for agent evaluation—solidifying its position as the leading framework for production agentic AI.
> [[1]](https://www.marktechpost.com/2026/01/06/how-to-design-an-agentic-ai-architecture-with-langgraph-and-openai-using-adaptive-deliberation-memory-graphs-and-reflexion-loops/) [[2]](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/) [[3]](https://langchain-ai.github.io/langgraph/mcp/)

---

## Agentic AI Ecosystem Landscape (2026)

Understanding where LangGraph fits in the broader ecosystem is critical for making informed architecture decisions.

| Framework / Protocol | Type | Strengths | Best For |
|---|---|---|---|
| **LangGraph** | Orchestration Framework | Stateful graphs, memory, human-in-the-loop, production-ready | Complex, stateful, production agent systems |
| **OpenAI Agents SDK** | Agent Framework | Native OpenAI integration, Guardrails, Handoffs, Tracing | OpenAI-native agent applications |
| **CrewAI** | Multi-Agent Framework | Role-based agents, simple API, rapid prototyping | Quick multi-agent prototypes |
| **AutoGen (Microsoft)** | Multi-Agent Framework | Conversational agents, group chat patterns | Research & conversational multi-agent systems |
| **MCP (Model Context Protocol)** | Open Protocol (Anthropic) | Standardized tool/context integration, cross-framework | Universal tool access for any agent framework |
| **A2A (Agent-to-Agent Protocol)** | Open Protocol (Google) | Inter-agent communication, Agent Cards, task management | Cross-framework agent collaboration |
| **LangSmith** | Observability & Eval | Tracing, evaluation, datasets, monitoring | Agent debugging, testing, and production monitoring |
| **LangGraph Platform** | Managed Infrastructure | Deployment, scaling, cron jobs, assistants API | Production deployment of LangGraph agents |

> 💡 **Key Insight (March 2026):** The industry is converging on **LangGraph for orchestration**, **MCP for tool interop**, and **A2A for agent interop**. These three together form the "agentic stack" for enterprise-grade systems.

---

## End-to-End Agentic AI Roadmap

### Phase 1: Foundations (2-3 weeks)

**Goal:** Build a rock-solid base in AI, LLMs, and LangChain. 📚

| Topic | Key Concepts |
|-------|--------------|
| **LLM Fundamentals** | Tokenization, prompting, inference, temperature, structured outputs |
| **Prompt Engineering** | Zero/Few-shot, Chain of Thought, Self-consistency, ReAct prompting |
| **LangChain Basics** | Chains, Agents, Memory, Tools, LCEL, Chat Models |
| **Python Async & State Mgmt** | asyncio, state machines, event-driven programming |
| **Modern LLM Models** | GPT-4o, GPT-4.5, Claude 3.5/Claude 4, Gemini 2.0 Pro, Llama 3, Mistral Large |
| **Structured Outputs** | JSON mode, function calling, tool calling schemas |

**Mini-Projects:**
- Build a simple Q&A chatbot with LangChain
- Implement a retrieval-augmented generator (RAG) with structured output
- Create a function-calling agent using OpenAI/Anthropic tool calling

---

### Phase 2: LangGraph Core Mastery (3-4 weeks)

**Goal:** Deeply understand LangGraph's architecture, both APIs, and core primitives. 🏗️

| Topic | Key Concepts |
|-------|--------------|
| **Graph Architecture** | Nodes, edges, state, transitions, conditional logic |
| **StateGraph API** | Class-based graph construction, `TypedDict`/`Pydantic` state, reducers |
| **Functional API (NEW)** | `@entrypoint`, `@task` decorators, Pythonic workflow definition |
| **Building State Machines** | Designing, running, debugging agent graphs |
| **Memory in LangGraph** | Checkpointing (`MemorySaver`, Postgres), episodic memory, `Store` API for long-term memory |
| **Tool Integration** | Connecting LLMs to APIs, DBs, external services, `ToolNode` |
| **Human-in-the-Loop** | `interrupt()` function, `Command(resume=...)`, approval workflows |
| **Prebuilt Agents** | `create_react_agent()` for rapid prototyping |
| **LangGraph Studio** | Visual debugging, graph inspection, step-through execution |
| **Streaming** | Token streaming, event streaming, streaming in production |

**Mini-Projects:**
- Create a customer support agent using `StateGraph`
- Rebuild the same agent using the functional API (`@entrypoint`/`@task`)
- Add persistent memory and tool calling with human approval checkpoints
- Debug and visualize your agent in LangGraph Studio

---

### Phase 3: Building Agentic Workflows (4-5 weeks)

**Goal:** Design, build, and test advanced agentic systems. 🤖

| Topic | Key Concepts |
|-------|--------------|
| **Multi-Agent Orchestration** | Supervisor pattern, swarm pattern, hierarchical teams |
| **ReAct Agents** | Reasoning + Acting loops, self-correction, `create_react_agent` |
| **Plan-and-Execute Pattern** | Decompose & conquer complex tasks, dynamic replanning |
| **Reflexion Loops** | Self-review, introspection, iterative improvement, scoring |
| **Agentic Memory Graphs** | Zettelkasten-style linking, context-aware retrieval, semantic memory |
| **Map-Reduce Agents** | Parallel processing with fan-out/fan-in patterns |
| **Agent Handoffs** | Transferring control between specialized agents |
| **Subgraph Composition** | Nesting graphs within graphs for modularity |

**Mini-Projects:**
- Build a plan-and-execute document analyst with reflexion
- Multi-agent workflow: supervisor + researcher + analyst + writer
- Map-reduce agent for parallel document analysis
- Agent with long-term memory using the `Store` API

---

### Phase 4: Advanced Agentic Patterns (4-6 weeks)

**Goal:** Master enterprise-grade and cutting-edge agent patterns. 🚀

| Topic | Key Concepts |
|-------|--------------|
| **Adaptive Deliberation** | Fast/slow reasoning, context-aware switching, thinking budgets |
| **Self-Improving Agents** | Learning from past errors, memory-enhanced agents, experience replay |
| **Governed Tool Use** | Permissions, logging, safety constraints, guardrails |
| **Complex Branching & Cycles** | Non-linear graphs, parallel/sequential flows, dynamic routing |
| **Multimodal Agents** | Integrating text, images, audio, video in agent workflows |
| **Enterprise Compliance** | Audit trails, data privacy, PII handling, compliance layers |
| **Agent Evaluation** | LangSmith evaluations, agent benchmarking, regression testing |
| **Guardrails & Safety** | Input/output validation, content filtering, hallucination detection |
| **Background & Cron Agents** | Long-running tasks, scheduled agent execution |

**Mini-Projects:**
- Self-improving code review agent with reflexion and persistent learning
- Governed multi-tool workflow for regulated domains (healthcare, finance)
- Multimodal agent that processes documents with text + images
- Comprehensive agent evaluation suite using LangSmith

---

### Phase 5: Agent Protocols & Interoperability (2-3 weeks)

**Goal:** Master open protocols for tool standardization and cross-agent communication. 🌐

> 🆕 **NEW PHASE (March 2026):** This phase was added to address the rapidly growing importance of agent interoperability standards.

| Topic | Key Concepts |
|-------|--------------|
| **Model Context Protocol (MCP)** | MCP servers, MCP clients, tool discovery, resource access, standardized tool schemas |
| **MCP with LangGraph** | Using `@tool` with MCP servers, connecting to MCP tool registries, dynamic tool loading |
| **Agent-to-Agent Protocol (A2A)** | Agent Cards, task lifecycle, inter-agent messaging, capability discovery |
| **A2A with LangGraph** | Exposing LangGraph agents via A2A, consuming external agents |
| **Cross-Framework Interop** | LangGraph ↔ OpenAI Agents SDK ↔ CrewAI bridges |
| **Tool Registries & Discovery** | Dynamic tool registration, capability catalogs, tool versioning |

**Mini-Projects:**
- Build an MCP tool server and connect it to a LangGraph agent
- Create a LangGraph agent that exposes itself via an A2A Agent Card
- Multi-framework workflow: LangGraph supervisor coordinating agents from different frameworks
- Dynamic tool discovery agent that finds and uses MCP tools at runtime

---

### Phase 6: Production & Scaling (3-4 weeks)

**Goal:** Deploy, monitor, and scale agentic AI systems. ⚙️

| Topic | Key Concepts |
|-------|--------------|
| **LangGraph Platform** | Managed deployment, Assistants API, cron jobs, store management |
| **Checkpointing & Reliability** | Save/restore state, error handling, retries, durable execution |
| **LangSmith Monitoring** | Tracing, observability, production dashboards, alerting |
| **Deployment Options** | LangGraph Cloud, self-hosted (Docker), FastAPI wrapping, Kubernetes |
| **Scaling Multi-Agent Systems** | Distributed agents, load balancing, async execution |
| **Continuous Improvement** | User feedback loops, A/B testing, online evaluation, agent versioning |
| **Security & Access Control** | API key management, role-based access, secrets management |
| **Cost Optimization** | Token budgeting, model routing (expensive ↔ cheap), caching strategies |

**Mini-Projects:**
- Deploy a production-ready agent API on LangGraph Platform with LangSmith monitoring
- Build a feedback loop pipeline for continuous agent improvement
- Implement cost-optimized model routing (GPT-4o for complex, GPT-4o-mini for simple tasks)
- Production multi-agent system with health checks, retries, and alerting

---

## Project Ideas

| Project | Description | Difficulty |
|---------|-------------|------------|
| **Autonomous Research Assistant** | Researches, summarizes, and compiles information from web and documents using MCP-connected search tools | ⭐⭐ |
| **Multi-Agent Customer Support** | Router, retriever, and responder agents with handoff patterns and human escalation | ⭐⭐⭐ |
| **Self-Healing Code Agent** | Detects, diagnoses, and fixes code bugs autonomously with reflexion and test execution | ⭐⭐⭐⭐ |
| **Personal Knowledge Manager** | Memory graph-powered assistant with long-term recall using Zettelkasten patterns | ⭐⭐⭐ |
| **Agentic Workflow Automation** | Multi-step business process automation (e.g., invoice processing) with governed tool use | ⭐⭐⭐ |
| **MCP-Powered Universal Agent** | Agent that dynamically discovers and uses tools from any MCP server | ⭐⭐⭐⭐ |
| **Cross-Framework Agent Network** | LangGraph agents collaborating with OpenAI Agents SDK agents via A2A protocol | ⭐⭐⭐⭐⭐ |
| **Multimodal Document Analyst** | Processes PDFs, images, tables, and charts to generate structured reports | ⭐⭐⭐ |
| **Agent-as-a-Service Platform** | Deploy multiple agents as discoverable services with Agent Cards and A2A | ⭐⭐⭐⭐⭐ |
| **Real-Time Data Pipeline Agent** | Monitors data streams, detects anomalies, and triggers automated responses | ⭐⭐⭐⭐ |

---

## Key 2026 Trends (Updated March 2026)

### 🔥 Hottest Trends Right Now

- **Agent Protocol Wars → Convergence:** MCP (Anthropic) and A2A (Google) are rapidly becoming industry standards. Most frameworks now support both. The debate has shifted from "which protocol?" to "how to combine them effectively."
  
- **Multi-Agent Systems at Scale:** Enterprises are deploying orchestrated teams of 5-20+ specialized agents. The supervisor/swarm pattern has replaced monolithic agents in production.

- **Agentic Memory as Infrastructure:** Persistent, structured memory (not just vector search) is now considered essential. Memory graphs with semantic linking are the new standard.

- **Agent Evaluation is Non-Negotiable:** Production teams now run automated evaluation suites (via LangSmith or similar) before every agent deployment. "Vibe-checking" agents is no longer acceptable.

- **Governed & Auditable Agents:** Regulated industries (finance, healthcare, legal) require full audit trails, permissioned tool use, and human-in-the-loop checkpoints. This is driving adoption of LangGraph's governed execution model.

### 📈 Industry Shifts

- **"Agentic Stack" Emerging:** LangGraph (orchestration) + MCP (tool interop) + A2A (agent interop) + LangSmith (eval & monitoring) is becoming the reference architecture.

- **Functional API Adoption:** LangGraph's new `@entrypoint`/`@task` functional API is gaining traction for simpler workflows, while `StateGraph` remains preferred for complex branching.

- **Cost-Aware Agent Design:** With LLM costs still significant, model routing (expensive model for hard tasks, cheap model for easy tasks) and token budgeting are standard practices.

- **Multimodal Agents Going Mainstream:** Agents that process text, images, audio, and structured data are moving from experiments to production.

- **Agent Marketplaces:** Early agent discovery platforms are emerging, powered by A2A Agent Cards and MCP tool registries.

> *"Over 55% of enterprise AI projects now include agentic capabilities, up from 40% at the start of 2026."*
> [[2]](https://acuvate.com/blog/2026-agentic-ai-expert-predictions/)

> *"MCP adoption grew 300% in Q1 2026 as tool standardization became a top priority for AI teams."*

---

## Top Resources

### Official Documentation
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangGraph Functional API Guide](https://langchain-ai.github.io/langgraph/concepts/functional_api/)
- [LangGraph MCP Integration](https://langchain-ai.github.io/langgraph/mcp/)
- [LangChain Documentation](https://python.langchain.com/docs/introduction/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangSmith Docs](https://docs.smith.langchain.com/)
- [LangGraph Platform Docs](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/)

### Protocol Specifications
- [Model Context Protocol (MCP) Spec](https://spec.modelcontextprotocol.io/)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [Agent-to-Agent (A2A) Protocol](https://google.github.io/A2A/)
- [A2A GitHub](https://github.com/google/A2A)

### Tutorials & Courses
- [LangChain Academy - Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph)
- [LangChain Academy - LangGraph: Multi-Agent Systems](https://academy.langchain.com/courses/multi-agent-systems)
- [DeepLearning.AI - AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/)
- [DeepLearning.AI - AI Agentic Design Patterns with AutoGen](https://www.deeplearning.ai/short-courses/)
- [Udemy: Build AI Agents 10x Faster 2026](https://www.udemy.com/course/build-ai-agents-agentic-2026-python-langchain-langgraph/)
- [AICurator: LangGraph Conversational AI Guide 2026](https://aicurator.io/langgraph-conversational-ai-app/)

### Articles & Guides
- [How to Design Agentic AI with LangGraph (MarkTechPost)](https://www.marktechpost.com/2026/01/06/how-to-design-an-agentic-ai-architecture-with-langgraph-and-openai-using-adaptive-deliberation-memory-graphs-and-reflexion-loops/)
- [7 Agentic AI Trends to Watch in 2026](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/)
- [Agentic AI Frameworks: Enterprise Guide 2026](https://www.spaceo.ai/blog/agentic-ai-frameworks/)
- [MCP: The USB-C of AI Tool Integration](https://modelcontextprotocol.io/introduction)
- [Building Multi-Agent Systems with LangGraph (LangChain Blog)](https://blog.langchain.dev/)
- [A2A Protocol: Enabling Agent Interoperability (Google)](https://developers.googleblog.com/)

### Research Papers
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [Tree of Thoughts: Deliberate Problem Solving](https://arxiv.org/abs/2305.10601)
- [LATS: Language Agent Tree Search](https://arxiv.org/abs/2310.04406)
- [Agent-as-a-Judge: Evaluating Agents with Agents](https://arxiv.org/abs/2410.10934)

### Tools & Platforms
- [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) — Visual agent debugging IDE
- [LangSmith](https://smith.langchain.com/) — Tracing, evaluation, monitoring
- [LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/) — Managed deployment
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers) — Pre-built MCP tool servers

---

## Sample Code

### Basic LangGraph Agent with `create_react_agent` (Recommended Starting Point)

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Define tools
@tool
def web_search(query: str) -> str:
    """Search the web for current information."""
    return f"[Search result for: {query}] — LangGraph is a stateful orchestration framework for agentic AI."

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# Create a ReAct agent (the simplest way to get started)
llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_react_agent(llm, tools=[web_search, calculator])

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is LangGraph and what is 42 * 17?"}]}
)

for msg in result["messages"]:
    print(f"{msg.type}: {msg.content}")
```

### Custom StateGraph Agent (Full Control)

```python
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Define state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Define tools
@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return f"[Simulated search result for: {query}]"

tools = [web_search]
tool_node = ToolNode(tools)

# Define the LLM node
llm = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

def call_llm(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Define routing logic
def should_use_tool(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Build graph
graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("tools", tool_node)
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_use_tool)
graph.add_edge("tools", "llm")

# Compile with memory
from langgraph.checkpoint.memory import MemorySaver
agent = graph.compile(checkpointer=MemorySaver())

# Run with thread-based memory
config = {"configurable": {"thread_id": "user-123"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is LangGraph?"}]},
    config=config
)
print(result["messages"][-1].content)
```

### Functional API Agent (NEW in 2026)

```python
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

@task
def research(topic: str) -> str:
    """Research a topic using the LLM."""
    response = llm.invoke(f"Research the following topic thoroughly: {topic}")
    return response.content

@task
def summarize(research_text: str) -> str:
    """Summarize research findings."""
    response = llm.invoke(f"Summarize the following research concisely:\n\n{research_text}")
    return response.content

@entrypoint(checkpointer=MemorySaver())
def research_agent(topic: str) -> str:
    """A simple research agent using the functional API."""
    # Tasks run as durable steps with automatic checkpointing
    raw_research = research(topic).result()
    summary = summarize(raw_research).result()
    return summary

# Run the agent
result = research_agent.invoke(
    "Latest advances in agentic AI with LangGraph",
    config={"configurable": {"thread_id": "research-001"}}
)
print(result)
```

### Multi-Agent Supervisor Pattern

```python
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages

# Define specialized agents
@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"[Web results for: {query}]"

@tool
def analyze_data(data: str) -> str:
    """Analyze data and provide insights."""
    return f"[Analysis of: {data}] — Key insight: trends are positive."

@tool
def write_report(content: str) -> str:
    """Write a formatted report."""
    return f"# Report\n\n{content}\n\n*Generated by AI Agent*"

llm = ChatOpenAI(model="gpt-4o", temperature=0)

researcher = create_react_agent(llm, tools=[search_web], prompt="You are a research specialist.")
analyst = create_react_agent(llm, tools=[analyze_data], prompt="You are a data analyst.")
writer = create_react_agent(llm, tools=[write_report], prompt="You are a report writer.")

# Define supervisor state
class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str

def supervisor(state: SupervisorState):
    """Route tasks to the appropriate specialist agent."""
    response = llm.invoke([
        {"role": "system", "content": """You are a supervisor. Based on the conversation, 
         decide which agent to call next: 'researcher', 'analyst', 'writer', or 'FINISH'.
         Respond with just the agent name."""},
        *state["messages"]
    ])
    return {"next_agent": response.content.strip()}

def route(state: SupervisorState) -> Literal["researcher", "analyst", "writer", "__end__"]:
    if state["next_agent"] == "FINISH":
        return "__end__"
    return state["next_agent"]

# Build supervisor graph
graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", lambda s: researcher.invoke(s))
graph.add_node("analyst", lambda s: analyst.invoke(s))
graph.add_node("writer", lambda s: writer.invoke(s))

graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route)
graph.add_edge("researcher", "supervisor")
graph.add_edge("analyst", "supervisor")
graph.add_edge("writer", "supervisor")

workflow = graph.compile()
result = workflow.invoke({
    "messages": [{"role": "user", "content": "Research LangGraph trends, analyze them, and write a report."}],
    "next_agent": ""
})
```

### Human-in-the-Loop with `interrupt()` (March 2026 Pattern)

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
    """Generate a proposed action for human review."""
    return {"messages": [{"role": "assistant", "content": "I'd like to send an email to the client. Approve?"}]}

def human_review(state: State):
    """Pause and wait for human approval."""
    decision = interrupt({"question": "Do you approve sending the email?", "options": ["yes", "no"]})
    return {"approved": decision == "yes"}

def execute_action(state: State):
    if state["approved"]:
        return {"messages": [{"role": "assistant", "content": "✅ Email sent successfully!"}]}
    return {"messages": [{"role": "assistant", "content": "❌ Action cancelled by human."}]}

graph = StateGraph(State)
graph.add_node("generate", generate_action)
graph.add_node("review", human_review)
graph.add_node("execute", execute_action)
graph.add_edge(START, "generate")
graph.add_edge("generate", "review")
graph.add_edge("review", "execute")
graph.add_edge("execute", END)

agent = graph.compile(checkpointer=MemorySaver())

# Step 1: Run until interrupt
config = {"configurable": {"thread_id": "review-001"}}
result = agent.invoke({"messages": [], "approved": False}, config=config)

# Step 2: Resume with human decision
result = agent.invoke(Command(resume="yes"), config=config)
print(result["messages"][-1]["content"])
```

### MCP Tool Integration (March 2026)

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

# Connect to MCP tool servers
async def build_mcp_agent():
    async with MultiServerMCPClient(
        {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"],
            },
            "web_search": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "env": {"BRAVE_API_KEY": "your-api-key"},
            },
        }
    ) as mcp_client:
        # Get tools from MCP servers
        tools = mcp_client.get_tools()
        
        # Create agent with MCP tools
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        agent = create_react_agent(llm, tools=tools)
        
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Search for LangGraph news and save a summary to notes.txt"}]}
        )
        return result

# Run
import asyncio
result = asyncio.run(build_mcp_agent())
```

---

## Roadmap Visual Summary

```
Phase 1 (Weeks 1-3)        Phase 2 (Weeks 4-7)         Phase 3 (Weeks 8-12)
┌─────────────────┐        ┌──────────────────┐         ┌───────────────────────┐
│  LLM & LangChain│───────▶│  LangGraph Core  │────────▶│  Agentic Workflows    │
│  Foundations     │        │  Mastery         │         │  Multi-Agent Systems  │
└─────────────────┘        └──────────────────┘         └───────────────────────┘
                                                                  │
         ┌────────────────────────────────────────────────────────┘
         ▼
Phase 4 (Weeks 13-18)      Phase 5 (Weeks 19-21)       Phase 6 (Weeks 22-25)
┌─────────────────────┐    ┌───────────────────────┐    ┌───────────────────────┐
│  Advanced Patterns   │───▶│  Protocols & Interop  │───▶│  Production & Scale   │
│  Eval & Safety       │    │  MCP, A2A             │    │  LangGraph Platform   │
└─────────────────────┘    └───────────────────────┘    └───────────────────────┘
```

**Total Duration: ~22-25 weeks (5-6 months)**

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

- Website: [Adil Shamim](https://adilshamim.me/)
- GitHub: [Adil Shamim](https://github.com/AdilShamim8)
- Create an issue in this repository for questions or suggestions

---

<p align="center">
  <a href="https://github.com/AdilShamim8">
    <img src="https://img.shields.io/badge/GitHub-AdilShamim8-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile"/>
  </a>
  <span style="opacity:.6"> &nbsp; </span>
  <a href="https://www.linkedin.com/in/adilshamim8">
    <img src="https://img.shields.io/badge/LinkedIn-AdilShamim8-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Profile"/>
  </a>
</p>
<div align="center">

⭐ **If you find this repository helpful, please consider giving it a star!** ⭐

</div>
