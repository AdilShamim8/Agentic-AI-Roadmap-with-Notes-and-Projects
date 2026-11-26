# 04 Tools and MCP - interview questions (concepts)

Status: beta | Teaches: [04 Tools and MCP](../../04-tools-and-mcp/) | Part 1 of 2

1. What makes a good tool, in the order the model experiences it?
Name, description, schema - the model reads all three before every call. Good means: a name that says what it does, a description that states what it returns and what it excludes, and typed arguments with constraints. The counter-bar: a tool that needs a paragraph of prompt coaching to be called correctly is a bad tool; the schema should carry the semantics. Teaches: [01-tool-design](../../04-tools-and-mcp/01-tool-design.md).

2. What is MCP, and what problem does it solve?
The Model Context Protocol - a standard protocol (current revision 2025-11-25, carried by the 1.x SDK line) for exposing tools, resources, and prompts from servers that any MCP-capable client consumes. It solves the N-by-M problem: tools written once serve every agent and framework, instead of per-framework integration. The bar: say "protocol boundary between agent and tools" and mean the decoupling, not the branding. Teaches: [02-mcp-from-scratch](../../04-tools-and-mcp/02-mcp-from-scratch.md) and [03-mcp-servers](../../04-tools-and-mcp/03-mcp-servers.md).

3. MCP transports: stdio, streamable HTTP - when do you use each?
Stdio for local, same-machine servers: launch as a subprocess, zero networking, the demo and laptop shape. Streamable HTTP for remote, shared, multi-consumer servers: one endpoint, auth, horizontal scale - the production shape. The historical note that signals depth: the SSE transport is superseded by streamable HTTP; a design still on SSE is dated. Teaches: [03-mcp-servers](../../04-tools-and-mcp/03-mcp-servers.md).

4. Where does authorization live in an MCP deployment?
At the server boundary: the server authenticates the caller (token, session), maps to identity and scopes, and enforces per-tool authorization before executing. The client-side lie to avoid: "the agent decides what it is allowed to call" - the model proposes; the server disposes. Teaches: [03-mcp-servers](../../04-tools-and-mcp/03-mcp-servers.md) and [04-mcp-client-in-langgraph](../../04-tools-and-mcp/04-mcp-client-in-langgraph.md).

5. How does a LangGraph agent consume MCP tools?
Via an adapter layer that discovers the server's tools and exposes them as native tools the agent binds - the LangChain MCP adapters convert MCP tool descriptors into callable tools with schemas. The design consequence: the agent does not know MCP exists; the boundary is invisible behind the tool interface, which is the point of the protocol. Teaches: [04-mcp-client-in-langgraph](../../04-tools-and-mcp/04-mcp-client-in-langgraph.md).

6. What is tool discovery, and when is dynamic discovery worth its cost?
Discovering callable tools at runtime from a registry or MCP server rather than hardcoding the list. Worth it when the tool set varies per tenant or environment, or tools are owned by other teams and change independently. The cost: an extra failure surface at startup and a wider tool list unless you also scope it. Teaches: [05-tool-discovery-and-registries](../../04-tools-and-mcp/05-tool-discovery-and-registries.md).

7. Retrieval as a tool vs retrieval as a pipeline stage - what is the difference?
Pipeline RAG retrieves unconditionally before generation; retrieval-as-a-tool lets the agent decide whether and what to search, reformulate, and search again with better terms. The trade: tool-shaped retrieval adds loop cost but buys adaptive queries, refusals when coverage is absent, and multi-hop behavior. Teaches: [06-retrieval-as-a-tool](../../04-tools-and-mcp/06-retrieval-as-a-tool.md).

8. How do you bound a tool's output, and why does it matter twice?
Structural limits in the tool: cap rows returned, cap characters per field, paginate. It matters for cost (unbounded results resend huge payloads every turn) and for selection accuracy (bloated results drown the reasoning). The follow-up to expect: "what does the model see when results are capped?" - a count plus the truncation marker, so the model knows there is more and can page. Teaches: [01-tool-design](../../04-tools-and-mcp/01-tool-design.md).

9. What is the agent-card idea from A2A doing in a tools conversation?
Separation of mechanism: MCP standardizes tool access within one agent's runtime; A2A standardizes agent-to-agent interaction across runtimes. A production system uses both - tools over MCP, agent-to-agent work over A2A - and knowing which boundary you are designing is the interview point. Teaches: [05-tool-discovery-and-registries](../../04-tools-and-mcp/05-tool-discovery-and-registries.md) with [07 Multi-agent and A2A](../../07-multi-agent-and-a2a/).

10. Give the tool-design smell test for destructive operations.
Name the action explicitly (issue_refund, not process_order), require the identity-bearing arguments in the schema (who and what, never implicit), execute only after an approval gate in the graph for high-risk classes, and be idempotent - a retried call must not double-execute. The bar: destructive safety is tool-layer engineering plus graph structure, never prompt politeness. Teaches: [01-tool-design](../../04-tools-and-mcp/01-tool-design.md).

11. What does versioning look like for an MCP server other teams depend on?
Additive evolution: new tools and optional fields ship without breaking old clients; removals and semantic changes go through a versioned surface or a deprecation window with a changelog. The test discipline: a contract test suite that pins the current schema, run on every server change, so the blast radius of a change is known before it ships. Teaches: [05-tool-discovery-and-registries](../../04-tools-and-mcp/05-tool-discovery-and-registries.md).

12. Why do overlapping tool descriptions cause wrong-tool calls, and what is the fix?
The model selects from descriptions; overlap makes both plausible for one intent, and the cheaper-reading one wins regardless of correctness. Fix by writing exclusions into descriptions ("does not return order status - use get_order_status"), separating scopes, or merging near-duplicates. Then verify with the intent evaluator: wrong-tool rate is measurable, so the fix is checked rather than believed. Teaches: [01-tool-design](../../04-tools-and-mcp/01-tool-design.md) with [06 Evals](../../06-evals-and-observability/).
