"""Reference implementations for the agentic AI roadmap.

This directory contains runnable Python files that demonstrate the core
patterns from the curriculum. Each file is self-contained and can be run
standalone (with the right environment variables set; see .env.example).

Every file is import-safe without API keys: LLM construction happens
inside functions, never at module import, so CI runs without secrets.
Node bodies that would be LLM calls are deterministic mocks in the demos
(the chapter code blocks show the LLM versions).

## Files

Module 01-03 (foundations, LangGraph core, agents in practice):
- `conversational_agent_demo.py` - the minimum viable production agent
- `structured_output_demo.py` - tool-calling loop with retry + limits
- `langgraph_core_demo.py` - state, nodes, edges, conditional edges, loops
- `sequential_workflow_demo.py`, `parallel_workflow_demo.py`,
  `conditional_workflow_demo.py`, `iterative_workflow_demo.py`
- `functional_api_demo.py` - @entrypoint / @task / interrupt
- `persistence_demo.py` - checkpointers + the Store
- `hitl_demo.py` - interrupt() approval workflows
- `streaming_demo.py` - stream modes (updates / values)
- `tool_design_demo.py`, `tool_integration_demo.py`

Module 04 (tools and MCP):
- `mcp_from_scratch_demo.py` - hand-rolled JSON-RPC server
- `mcp_filesystem_server.py`, `mcp_websearch_server.py`,
  `mcp_sqlite_server.py` - SDK servers over stdio
- `mcp_client_demo.py` - MultiServerMCPClient against the real servers

Module 05 (patterns):
- `react_demo.py` - the foundational loop
- `plan_execute_demo.py`, `reflexion_demo.py`, `supervisor_demo.py`,
  `swarm_demo.py`, `hierarchical_demo.py`, `map_reduce_demo.py` (Send)

Module 06 (evals and observability):
- `llm_judge_demo.py` (requires a key), `trajectory_eval_demo.py`,
  `langsmith_demo.py`, `cost_optimization_demo.py`
- `run_evals.py` - the eval runner behind `make eval` and CI

Module 07 (multi-agent and A2A):
- `handoff_demo.py`, `a2a_from_scratch_demo.py`, `a2a_server_demo.py`,
  `cross_framework_demo.py` - all against A2A protocol v1.0

Module 08 (production):
- `durability_demo.py` (Sqlite/Postgres checkpointer), `deploy_demo.py`,
  `cost_optimization_production_demo.py`, `governance_demo.py`,
  `continuous_improvement_demo.py`

## Running

```bash
# Install dependencies
make install

# Set up environment (no keys needed for most demos; see .env.example)
cp .env.example .env

# Run a demo
python examples/react_demo.py

# Run the eval suite
make eval
```
"""

__version__ = "0.3.0"
