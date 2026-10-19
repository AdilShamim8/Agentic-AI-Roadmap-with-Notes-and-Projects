"""Persistence and long-term memory demonstration in LangGraph.

Demonstrates:
1. Short-term thread persistence via the checkpointer (MemorySaver here;
   swap in PostgresSaver for production).
2. Long-term cross-thread memory via the Store (namespaced key-value
   storage).
3. State isolation between different thread IDs.

The conversation logic is mocked, so no API key is required.

Run:
    python examples/persistence_demo.py
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.store.memory import InMemoryStore


class ConversationState(TypedDict):
    """Conversation state schema."""

    messages: Annotated[list, add_messages]
    user_id: str
    last_response: str


# Long-term memory: the Store. Cross-thread, namespace per user.
store = InMemoryStore()


def save_user_memory(user_id: str, fact: str) -> None:
    """Store a long-term fact in the user's namespace.

    Store values are dict payloads (a bare list is rejected); we keep the
    facts under an 'items' key.
    """
    namespace = ("memories", user_id)
    item = store.get(namespace, "facts")
    facts = list(item.value.get("items", [])) if item and item.value else []
    if fact not in facts:
        facts.append(fact)
    store.put(namespace, "facts", {"items": facts})


def recall_user_memories(user_id: str) -> list[str]:
    """Retrieve long-term facts for a user."""
    namespace = ("memories", user_id)
    item = store.get(namespace, "facts")
    if item and item.value:
        return list(item.value.get("items", []))
    return []


def respond(state: ConversationState) -> dict:
    """Produce the next assistant turn (mocked; an LLM would do this)."""
    user_id = state["user_id"]
    last_user_message = state["messages"][-1].content if state["messages"] else ""
    known = recall_user_memories(user_id)
    memory_note = f" I remember about you: {'; '.join(known)}." if known else ""
    reply = (
        f"You said: {last_user_message!r}.{memory_note} "
        "(mocked response; an LLM call goes here in production)"
    )
    # Memory extraction: in production a small model call extracts facts.
    if "favorite" in last_user_message.lower():
        save_user_memory(user_id, last_user_message)
    return {"last_response": reply}


def build_conversation_graph():
    """Build and compile the conversational StateGraph."""
    workflow = StateGraph(ConversationState)
    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile(checkpointer=MemorySaver())


# Module-level compiled graph.
agent = build_conversation_graph()


def main() -> None:
    """Run multi-turn conversations across two threads and two users."""
    print("\n=== Persistence demo ===\n")

    # Thread 1, user alice: two turns. The checkpointer keeps history.
    cfg_alice = {"configurable": {"thread_id": "alice-session-1"}}

    def turn(content: str, user_id: str = "alice") -> dict:
        return {
            "messages": [{"role": "user", "content": content}],
            "user_id": user_id,
            "last_response": "",
        }
    r1 = agent.invoke(turn("Hi"), config=cfg_alice)
    print(f"Turn 1 (alice): {r1['last_response']}")
    r2 = agent.invoke(turn("My favorite color is blue"), config=cfg_alice)
    print(f"Turn 2 (alice): {r2['last_response']}")

    # Thread 2, same user: a new session, but long-term memory persists.
    cfg_alice2 = {"configurable": {"thread_id": "alice-session-2"}}
    r3 = agent.invoke(turn("What do you know about me?"), config=cfg_alice2)
    print(f"New session (alice): {r3['last_response']}")
    assert "favorite color is blue" in r3["last_response"], "Store memory lost"

    # A different user must not see alice's memories (cross-user isolation).
    cfg_bob = {"configurable": {"thread_id": "bob-session-1"}}
    r4 = agent.invoke(
        {
            "messages": [{"role": "user", "content": "What do you know about me?"}],
            "user_id": "bob",
            "last_response": "",
        },
        config=cfg_bob,
    )
    print(f"Other user (bob):  {r4['last_response']}")
    assert "favorite color is blue" not in r4["last_response"], "Memory leaked across users"

    print("\nPersistence, Store memory, and isolation verified.")


if __name__ == "__main__":
    main()
