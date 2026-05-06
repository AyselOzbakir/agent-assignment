"""
Data models for the agent system.

Defines the core types used throughout the agent for requests, responses,
tool calls, and memory management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from datetime import datetime


class Intent(str, Enum):
    """User intent categories."""

    COWORKING_SEARCH = "coworking_search"
    APPOINTMENT_BOOKING = "appointment_booking"
    MEETING_SCHEDULING = "meeting_scheduling"
    TRIP_PLANNING = "trip_planning"
    SEARCH = "search"
    REMINDER = "reminder"
    UNKNOWN = "unknown"


class ToolName(str, Enum):
    """Available tools."""

    CALENDAR_CHECK = "calendar_check"
    SEARCH_SERVICE = "search_service"
    BOOKING_SERVICE = "booking_service"
    REMINDER_CREATE = "reminder_create"
    BUDGET_CHECK = "budget_check"


@dataclass
class ToolCall:
    """Represents a tool invocation."""

    tool: ToolName
    params: dict[str, Any]
    description: str = ""

    def __str__(self) -> str:
        return f"{self.tool.value}({', '.join(f'{k}={v}' for k, v in self.params.items())})"


@dataclass
class ToolResult:
    """Result from executing a tool."""

    tool: ToolName
    success: bool
    data: Any = None
    error: Optional[str] = None
    executed_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        if self.success:
            return f"✓ {self.tool.value}: {self.data}"
        return f"✗ {self.tool.value}: {self.error}"


@dataclass
class UserRequest:
    """User's request to the agent."""

    text: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AgentState:
    """Current state of the agent's processing."""

    request: UserRequest
    intent: Intent = Intent.UNKNOWN
    subtasks: list[str] = field(default_factory=list)
    clarifying_questions: list[str] = field(default_factory=list)
    tool_results: list[ToolResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    summary: Optional[str] = None


@dataclass
class AgentResponse:
    """Final response from the agent."""

    success: bool
    message: str
    intent: Intent
    actions_taken: list[str]
    findings: dict[str, Any]
    blockers: list[str]
    clarifying_questions: list[str]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ConversationState:
    """Tracks pending clarifications for multi-turn conversations."""

    pending_intent: Optional[Intent] = None
    original_request: Optional[str] = None
    missing_field: Optional[str] = None  # e.g., "city", "time", "date"
    clarifying_question: Optional[str] = None

    def has_pending_clarification(self) -> bool:
        """Check if there's a pending clarification waiting for user input."""
        return self.pending_intent is not None

    def clear(self) -> None:
        """Clear the pending clarification state."""
        self.pending_intent = None
        self.original_request = None
        self.missing_field = None
        self.clarifying_question = None
