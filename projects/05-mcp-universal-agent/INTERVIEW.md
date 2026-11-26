# Interview guide - Project 05: MCP universal agent

Status: beta | For: presenting this project in interviews | Related: [project README](README.md), [project stories](../../10-interview-preparation/15-project-stories.md)

## The pitch

"One agent, N tool servers: an agent that consumes tools over MCP - filesystem, web search, sqlite - discovered from server manifests instead of hardcoded. The tools are shared infrastructure: any MCP-capable agent in the org consumes the same servers, which is the whole point of the protocol boundary."

## The whiteboard script

1. The agent on one side, the tool servers on the other, the protocol line drawn explicitly between.
2. The manifest - each server's connection config and tool descriptors.
3. The adapter layer - MCP tool descriptors become agent-bindable tools with schemas.
4. The transport choice - stdio for local servers, streamable HTTP for shared production ones.
5. The auth line - the server authenticates the caller and enforces per-tool authorization.

The line that earns the nod: "The agent does not know MCP exists - the boundary is invisible behind the tool interface, which is the point."

## The numbers you quote

- Server count in the manifest and transport per server.
- Token cost per turn with N tools bound versus a scoped subset - the tool-count tradeoff is measurable.

## The follow-ups

- "Why MCP instead of native tools?" Shared consumers: the moment a second agent needs the same tools, the protocol pays. One consumer, native tools are simpler - say the crossover honestly.
- "How does auth work?" At the server: the caller authenticates, the server maps to scopes, and per-tool authorization executes server-side - the model proposes; the server disposes.
- "What breaks when a server changes?" Contract tests pin the schema; additive changes ship freely, breaking ones go through versioned surfaces. Consumers are agents that cannot read changelogs.
- "Which transport, when?" Stdio for same-machine demos; streamable HTTP for remote, multi-consumer production. The SSE transport is superseded - a design still on it is dated.

## The red flags

- Presenting MCP as a brand feature instead of an integration boundary decision.
- No auth story for a multi-consumer deployment.
- Hardcoding tool lists in the agent after selling the discovery story.

## What this project proves

Protocol-level thinking - the N-by-M integration problem, contract discipline, and the tools-as-boundary judgment platform teams screen for.
