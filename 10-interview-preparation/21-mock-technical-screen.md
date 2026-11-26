# Mock: technical screen

Module: 10-interview-preparation
Chapter: 21-mock-technical-screen
Status: beta
Last reviewed: 2026-11-26
Estimated time: 1 hour

## Learning objectives

- Watch a full technical screen pass, with examiner commentary on each move
- See where candidates lose the same screen, in the same minute, every time
- Use the transcript as a drill script with a partner or alone

## How to read the transcript

Interviewer lines are plain; the candidate's moves get the commentary. The prompt is the classic Shape-2 screen from [04 Technical screens](04-technical-screens.md): tool design. Sixty minutes compressed to the load-bearing exchanges.

## The transcript

Interviewer: "Here is a function that looks up orders for a customer. Wrap it as an agent tool and tell me what you would change about it."

Candidate: "Before I write anything - who calls this, the agent, or the agent on behalf of an end user?"

[Commentary: 30 seconds in, the candidate has already separated the two failure modes this screen tests - a tool an agent calls for a user needs identity scoping; a tool the agent calls for itself needs neither. Most candidates start typing a wrapper.]

Interviewer: "On behalf of an end user, in a support chat."

Candidate: "Then the `customer_id` cannot come from the model. I will take it from the session and inject it in the tool wrapper - the model supplies the query terms, never the identity. First the signature, then the schema."

```python
def get_orders(
    customer_id: str,          # injected by the app, not the model
    status: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """Return the customer's orders, newest first.

    Each item: order_id, status, placed_at, total. Does not return
    tracking detail or line items - call get_order_status for one order.
    Returns at most `limit` items.
    """
```

[Commentary: three scoring lines in one artifact - identity out of the model's reach, a bounded return, and a docstring that tells the model what NOT to ask this tool for. The exclusions sentence is the part strong candidates add and average candidates omit.]

Interviewer: "Why the limit?"

Candidate: "Token discipline. A customer with 400 orders is a 40K-token tool result; the agent then reasons over it badly and expensively. Twenty newest serves the support cases, and the count itself is a signal - 'you have 37 orders' is often the whole answer."

Interviewer: "The docstring - why list what it does not return?"

Candidate: "Tool descriptions are the model's API docs. Overlapping coverage is how you get the wrong-but-plausible call - search_docs asked for order status. The exclusions line is the cheapest routing fix there is; I would rather write it than tune prompts."

Interviewer: "What happens when the lookup fails - bad id, backend down?"

Candidate: "Two different failures, two different returns. Unknown customer: an empty structured result with a `found: false` field, because the model needs to distinguish 'no orders' from 'no customer.' Backend down: a structured error the tool layer raises after one retry, and the graph routes to an apology-plus-escalation node, not a model retry - the model cannot fix a 503, and letting it retry just burns tokens in a loop."

[Commentary: this is the answer that separates the pass from the strong pass. Failures are enumerated, distinguished, and routed structurally. The unasked version of this question is where the screen is silently failed - a tool that cannot fail.]

Interviewer: "Last thing - the team also has a research agent that needs order history. Same tool?"

Candidate: "Same tool, different caller - so this is the MCP moment. I would move it to a small MCP server with the auth check at the server boundary, and both agents consume it. For one caller, a native tool is simpler and I would not build the server. Two callers is exactly when the protocol pays."

[Commentary: the candidate closed with a scope-appropriate architecture judgment, not a technology preference. Notice there is no pydantic showpiece, no framework lecture - the screen is passed in the schema, the boundaries, and the failure routing.]

## Where the same screen fails

Minute 5: typing a `@tool` decorator around the function with no signature change - identity unscoped, result unbounded.

Minute 20: the failure question answered with "I would add try/except" - catching without routing, and the model still sees an exception string.

Minute 40: "I would fine-tune the model on our order data" for what is a tool-design problem. Any screen where the answer is a fine-tune, the question was structural.

## The drill

Run it twice: once as the candidate with a friend reading the interviewer lines, once solo, aloud, timed to 25 minutes. Swap in the Shape-1 prompt (the routing graph) and re-run - the moves transfer: state first, boundaries stated, failures routed, no default to prompt fixes.

## What is next

[22 Mock: system design](22-mock-system-design.md) - the design round, same treatment.
