"""
Memory management for the agent.

Tracks conversation history, tool results, and agent decisions for context
across interactions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.models import ToolResult, AgentState


@dataclass
class Memory:
    """Agent memory tracking."""

    conversation_history: list[dict[str, str]] = field(default_factory=list)
    tool_history: list[ToolResult] = field(default_factory=list)
    agent_states: list[AgentState] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def add_user_message(self, content: str) -> None:
        """Add a user message to history.

        Args:
            content: The user's message
        """
        self.conversation_history.append(
            {"role": "user", "content": content, "timestamp": datetime.now().isoformat()}
        )

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to history.

        Args:
            content: The assistant's response
        """
        self.conversation_history.append(
            {
                "role": "assistant",
                "content": content,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def add_tool_result(self, result: ToolResult) -> None:
        """Record a tool execution result.

        Args:
            result: The tool result to store
        """
        self.tool_history.append(result)

    def add_agent_state(self, state: AgentState) -> None:
        """Record the agent's state at a decision point.

        Args:
            state: The agent state to store
        """
        self.agent_states.append(state)

    def get_context(self, max_messages: int = 10) -> str:
        """Get formatted context for the model.

        Args:
            max_messages: Maximum conversation messages to include

        Returns:
            Formatted context string
        """
        context_parts = []

        # Add recent conversation
        recent_messages = self.conversation_history[-max_messages:]
        if recent_messages:
            context_parts.append("Recent conversation:")
            for msg in recent_messages:
                role = msg["role"].upper()
                content = msg["content"]
                context_parts.append(f"{role}: {content}")

        # Add recent tool results
        recent_tools = self.tool_history[-5:]
        if recent_tools:
            context_parts.append("\nRecent tool results:")
            for result in recent_tools:
                context_parts.append(f"  - {result}")

        return "\n".join(context_parts)

    def get_summary(self) -> str:
        """Get a summary of the memory.

        Returns:
            Summary of conversation and actions
        """
        return (
            f"Messages: {len(self.conversation_history)}, "
            f"Tools used: {len(self.tool_history)}, "
            f"States tracked: {len(self.agent_states)}"
        )

    def clear(self) -> None:
        """Clear all memory."""
        self.conversation_history.clear()
        self.tool_history.clear()
        self.agent_states.clear()
