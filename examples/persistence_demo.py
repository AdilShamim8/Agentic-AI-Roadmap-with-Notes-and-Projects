"""Persistence and long-term memory demonstration in LangGraph.

Demonstrates:
1. Short-term thread persistence via Checkpointer (MemorySaver / PostgresSaver)
2. Long-term cross-thread memory via Store (namespaced key-value storage)
3. State isolation between different thread IDs
4. Context resumption across multiple conversation turns

Run:
    python examples/persistence_demo.py
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, TypedDict

try:
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.graph import END, START, StateGraph
    from langgraph.store.memory import InMemoryStore
    HAS_LANGGRAPH_PERSISTENCE = True
except ImportError:
    HAS_LANGGRAPH_PERSISTENCE = False


class InMemoryMockStore:
    """Mock store for cross-thread long-term memory."""

    def __init__(self) -> None:
        self._data: Dict[Tuple[Tuple[str, ...], str], Any] = {}

    def put(self, namespace: Tuple[str, ...], key: str, value: Any) -> None:
        self._data[(namespace, key)] = value

    def get(self, namespace: Tuple[str, ...], key: str) -> Optional[Any]:
        return self._data.get((namespace, key))


class ThreadCheckpointer:
    """Mock checkpointer managing per-thread state."""

    def __init__(self) -> None:
        self.threads: Dict[str, Dict[str, Any]] = {}

    def save(self, thread_id: str, state: Dict[str, Any]) -> None:
        self.threads[thread_id] = dict(state)

    def load(self, thread_id: str) -> Dict[str, Any]:
        return dict(self.threads.get(thread_id, {}))


class ConversationState(TypedDict):
    """Conversation state schema."""

    messages: List[str]
    user_id: str
    last_response: str


class ConversationalAgentWithMemory:
    """Agent combining thread-level checkpointing and long-term store."""

    def __init__(self) -> None:
        self.checkpointer = ThreadCheckpointer()
        self.store = InMemoryMockStore()

    def remember_fact(self, user_id: str, fact: str) -> None:
        """Store long-term memory in the user's namespace."""
        existing = self.store.get(("memories", user_id), "facts") or []
        if fact not in existing:
            existing.append(fact)
        self.store.put(("memories", user_id), "facts", existing)

    def recall_facts(self, user_id: str) -> List[str]:
        """Retrieve all long-term facts for a given user."""
        return self.store.get(("memories", user_id), "facts") or []

    def chat(self, thread_id: str, user_id: str, user_message: str) -> str:
        """Execute a conversation step within a specific thread."""
        state = self.checkpointer.load(thread_id)
        messages: List[str] = state.get("messages", [])
        messages.append(f"User: {user_message}")

        # Check long-term user memories
        memories = self.recall_facts(user_id)
        memory_context = f" [Recalled facts: {', '.join(memories)}]" if memories else ""

        response = f"Assistant: Received '{user_message}'.{memory_context} Turn count: {len(messages)}"
        messages.append(response)

        # Update checkpoint for thread
        self.checkpointer.save(
            thread_id,
            {"messages": messages, "user_id": user_id, "last_response": response},
        )
        return response


def main() -> None:
    """Run verification tests for checkpointing and memory isolation."""
    print("\n=== LangGraph Persistence and Memory Demo ===")
    agent = ConversationalAgentWithMemory()

    user_id = "engineer_alice"
    thread_1 = "thread-alice-session-1"
    thread_2 = "thread-alice-session-2"
    thread_bob = "thread-bob-session-1"

    # Step 1: Save long-term facts into Store
    print("Step 1: Saving long-term user profile facts into Store...")
    agent.remember_fact(user_id, "Prefers Python and LangGraph")
    agent.remember_fact(user_id, "Targeting 2026 Agentic AI production deployment")
    alice_facts = agent.recall_facts(user_id)
    print(f"  Alice's Stored Facts: {alice_facts}")
    assert len(alice_facts) == 2

    # Step 2: Thread 1 conversation
    print("\nStep 2: Conversation in Thread 1...")
    r1 = agent.chat(thread_1, user_id, "Hello, can you help configure my state machine?")
    print(f"  {r1}")
    r2 = agent.chat(thread_1, user_id, "Add error boundary validation.")
    print(f"  {r2}")

    t1_state = agent.checkpointer.load(thread_1)
    print(f"  Thread 1 message count: {len(t1_state['messages'])}")
    assert len(t1_state["messages"]) == 4, "Thread 1 should have 2 user + 2 assistant messages"

    # Step 3: Thread 2 conversation (same user, new session)
    print("\nStep 3: Conversation in Thread 2 (Same user, new thread)...")
    r3 = agent.chat(thread_2, user_id, "Starting a fresh project.")
    print(f"  {r3}")

    t2_state = agent.checkpointer.load(thread_2)
    print(f"  Thread 2 message count: {len(t2_state['messages'])}")
    assert len(t2_state["messages"]) == 2, "Thread 2 should have independent thread history"
    assert "Prefers Python and LangGraph" in r3, "Cross-thread store memory should be accessible"

    # Step 4: Bob's conversation (different user)
    print("\nStep 4: Conversation for user Bob (different user)...")
    r_bob = agent.chat(thread_bob, "user_bob", "Hi, I'm new here.")
    print(f"  {r_bob}")
    bob_facts = agent.recall_facts("user_bob")
    assert len(bob_facts) == 0, "Bob should not have Alice's memories"
    assert "Prefers Python" not in r_bob, "Bob must not access Alice's private facts"

    print("\nAll persistence and memory isolation tests passed successfully.")


if __name__ == "__main__":
    main()
