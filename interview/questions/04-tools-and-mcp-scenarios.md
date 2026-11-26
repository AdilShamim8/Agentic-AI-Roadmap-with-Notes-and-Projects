# 04 Tools and MCP - interview scenarios

Status: beta | Teaches: [04 Tools and MCP](../../04-tools-and-mcp/) | Part 2 of 2

1. "Three teams want the same order-lookup tool for their agents. Design the boundary."
One MCP server owning the order domain: streamable HTTP endpoint, auth at the server, the tool schema with bounded returns, and a contract test suite pinning the interface. Each agent consumes it through the adapter; nobody re-implements the lookup. The two extras that make it senior: a deprecation policy so tool changes do not surprise consumers, and per-consumer scopes at the server so an agent sees only the tools it is authorized for. Teaches: [03-mcp-servers](../../04-tools-and-mcp/03-mcp-servers.md) and [05-tool-discovery-and-registries](../../04-tools-and-mcp/05-tool-discovery-and-registries.md).

2. "Your agent calls get_order_status for tracking questions. Fix the wrong-tool rate without touching the model."
Description surgery: each tool's description states its exclusions - "returns order status and dates; does not return tracking events - call get_tracking." Then check the schema: if both tools take order_id with free text, add the discriminating argument. Verify with the eval set's wrong-tool rows; the number should move without any prompt changes. Teaches: [01-tool-design](../../04-tools-and-mcp/01-tool-design.md).

3. "A tool result is 80,000 tokens. What do you do?"
Bound at the tool: cap the row count, project only needed fields, truncate long text fields with an explicit marker, and return a total count so the model can page or filter on a second call. The deeper answer: the payload size is an interface decision made when the tool was designed - "what does the model actually need per step" - not a compression problem discovered at 2 a.m. Teaches: [01-tool-design](../../04-tools-and-mcp/01-tool-design.md).

4. "Legal requires that no agent can ever see documents outside the caller's department. Where do you enforce that?"
In the search tool and the index, never the prompt: the filter chain runs server-side - identity to department to ACL - before ranking, with canary queries in the eval suite proving forbidden documents never surface. The sentence the panel wants: "post-filtering results after retrieval is not enforcement; a leaked-then-filtered result already polluted the ranking." Teaches: [06-retrieval-as-a-tool](../../04-tools-and-mcp/06-retrieval-as-a-tool.md) and [the docs-RAG case](../../10-interview-preparation/09-design-case-docs-rag.md).

5. "The agent keeps re-searching with the same query. What does the tool need to return?"
A signal the loop can read: result counts, "no documents matched," or an explicit no-more-results marker - so the model's next step can change. If the tool returns indistinguishable emptiness, the loop cannot converge; the fix is tool semantics, not prompt pleading. The belt-and-suspenders: a budget field in state that ends the loop deterministically anyway. Teaches: [06-retrieval-as-a-tool](../../04-tools-and-mcp/06-retrieval-as-a-tool.md).

6. "An MCP server you depend on ships a schema change overnight. Walk your morning."
The contract tests caught it or you learn from production traces - either way: pin the server version you tested against, run the contract suite against the new version, and consume the change deliberately (additive fields fine; renamed args need an adapter shim). The design lesson to say out loud: shared tool servers need versioning discipline precisely because their consumers are agents that cannot read a changelog. Teaches: [05-tool-discovery-and-registries](../../04-tools-and-mcp/05-tool-discovery-and-registries.md).

7. "Should this team's five internal tools be one MCP server or five?"
One server when they share a domain, an owner, and a deployment lifecycle - order tools belong together, and the auth boundary is per-domain anyway. Five when the owners differ or the availability requirements diverge (a real-time inventory service should not share a deployment with a batch policy lookup). The answer is organizational first, technical second - say that, and it lands. Teaches: [03-mcp-servers](../../04-tools-and-mcp/03-mcp-servers.md).

8. "You are handed a 40-tool registry and a mandate to use them all. What do you actually do?"
Scope first: no task needs 40 tools - group by intent, bind dynamically per request the relevant 5-10, and mark the rest undiscovered for that context. Then compose: related fine-grained tools collapse into one parameterized action where the model's choice is an argument, not a tool selection. Report the metric: wrong-tool rate and tokens per request before and after - the scoping should show up in both. Teaches: [05-tool-discovery-and-registries](../../04-tools-and-mcp/05-tool-discovery-and-registries.md).

9. "The demo runs MCP servers as local subprocesses; production security wants no subprocesses. What changes?"
The stdio-to-HTTP migration: servers become services behind streamable HTTP with auth, the client config swaps transport, and the code that manages subprocess lifecycles disappears. What should NOT change: the tool schemas and the agent's graph - the protocol isolating them is doing its job, and saying so is the interview point. Teaches: [03-mcp-servers](../../04-tools-and-mcp/03-mcp-servers.md) and [04-mcp-client-in-langgraph](../../04-tools-and-mcp/04-mcp-client-in-langgraph.md).

10. "Your agent is 'sometimes lazy' - it answers from memory instead of calling the lookup tool. Diagnose."
Check the description: does the tool say it is REQUIRED for facts (the model needs "returns live order status; never guess it")? Check the model tier (weaker models skip calls more). Then structural: for facts that must be live, make the graph call the tool - a node that always fetches before generation, or a validator that rejects answers citing order data with no matching tool call in the trajectory. "Sometimes lazy" is a spec gap, not a personality. Teaches: [01-tool-design](../../04-tools-and-mcp/01-tool-design.md) with [06 Evals](../../06-evals-and-observability/).
