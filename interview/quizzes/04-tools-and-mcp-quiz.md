# Quiz 04 - Tools and MCP

Status: beta | Covers: [04 Tools and MCP](../../04-tools-and-mcp/) | 10 questions

1. The model reads these before every tool call, in order:
A) Code, docstring, tests
B) Name, description, schema
C) Schema only
D) Return type only

2. MCP solves:
A) Prompt injection
B) The N-by-M problem - tools written once serve every capable client
C) Model latency
D) Context windows

3. Streamable HTTP transport is for:
A) Local subprocess servers
B) Remote, shared, multi-consumer servers
C) Testing only
D) Streaming tokens

4. Authorization in an MCP deployment lives:
A) In the agent's system prompt
B) At the server boundary, per caller and per tool
C) In the tool description
D) With the provider

5. Overlapping tool descriptions cause:
A) Higher latency
B) Wrong-but-plausible tool selection
C) Compile errors
D) Nothing - the model disambiguates perfectly

6. Bounding a tool's output matters for:
A) Cost and reasoning quality only
B) Cost, reasoning quality, and selection accuracy
C) Nothing - models handle long inputs
D) Security only

7. Retrieval as a tool differs from pipeline RAG because:
A) It uses vectors
B) The agent decides whether and what to search, and can reformulate
C) It is always faster
D) It needs no eval

8. A destructive tool is safe when:
A) Its description says "use with care"
B) It is explicit, identity-bearing, approval-gated, and idempotent
C) It is never exposed to the model
D) The temperature is low

9. Versioning an MCP server other teams consume means:
A) Never changing anything
B) Additive evolution plus contract tests pinning the schema
C) Semver in the README only
D) A new server per change

10. Dynamic tool discovery is worth it when:
A) Always - discovery is modern
B) The tool set varies per tenant or changes across team boundaries
C) Never - hardcoded is safer
D) The model is weak

## Answer key

1. B - the schema carries the semantics ([chapter 01](../../04-tools-and-mcp/01-tool-design.md)).
2. B - protocol boundary between agent and tools ([chapter 02](../../04-tools-and-mcp/02-mcp-from-scratch.md)).
3. B - stdio is the local shape; HTTP the production one ([chapter 03](../../04-tools-and-mcp/03-mcp-servers.md)).
4. B - the model proposes; the server disposes ([chapter 03](../../04-tools-and-mcp/03-mcp-servers.md)).
5. B - exclusions in descriptions fix it ([chapter 01](../../04-tools-and-mcp/01-tool-design.md)).
6. B - unbounded results drown reasoning and bloat every turn ([chapter 01](../../04-tools-and-mcp/01-tool-design.md)).
7. B - adaptive querying, refusal on no-coverage ([chapter 06](../../04-tools-and-mcp/06-retrieval-as-a-tool.md)).
8. B - structural safety, never prompt politeness ([chapter 01](../../04-tools-and-mcp/01-tool-design.md)).
9. B - consumers are agents that cannot read changelogs ([chapter 05](../../04-tools-and-mcp/05-tool-discovery-and-registries.md)).
10. B - precision and scoping, not fashion ([chapter 05](../../04-tools-and-mcp/05-tool-discovery-and-registries.md)).
