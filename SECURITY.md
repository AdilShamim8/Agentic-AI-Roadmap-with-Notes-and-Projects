# Security Policy

This repository is a teaching curriculum. It ships Markdown chapters and
small, runnable example programs. It is not a deployed service and holds
no user data, so its attack surface is small. The policy below covers the
parts that still matter.

## Scope

In scope:

- Example code that learners copy and run on their own machines
  (everything under `examples/`, including the MCP servers)
- Dependency declarations in `pyproject.toml`
- Anything that could mislead a learner into an unsafe practice, such as
  an example that logs API keys or embeds a secret in source

Out of scope:

- Content errors (wrong version numbers, dead links) — those are
  ordinary issues, not security reports
- The user's own environment, keys, or deployments

## Reporting a vulnerability

Do not open a public issue for a security problem. Email the maintainer
via the GitHub account listed in `MAINTAINERS.md`, with "security" in
the subject. Include:

1. The affected file and line
2. A minimal reproduction
3. What an attacker could realistically gain

You should get a reply within 72 hours. If the report is accepted, a fix
lands in a patch release and the CHANGELOG credits the reporter (unless
you prefer to stay anonymous).

## Safe-use rules for the examples

- Never commit a real API key. `.env.example` shows the names; copy it
  to `.env` (git-ignored) and fill it locally.
- The MCP server examples bind to localhost by default. Keep it that
  way unless you deliberately expose them, and then put auth in front.
- The examples are deliberately small. They skip input validation that
  production code needs. Treat them as teaching artifacts, not
  hardened services.
