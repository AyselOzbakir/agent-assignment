"""
Core agent implementation.

Orchestrates the agent workflow: understanding requests, identifying intent,
breaking down tasks, executing tools, and providing summaries.
"""

from src.models import (
    Intent,
    UserRequest,
    AgentState,
    AgentResponse,
    ToolCall,
    ToolName,
    ConversationState,
)
from src.tools import ToolExecutor
from src.memory import Memory
from src.prompts import Prompts


class Agent:
    """Main agent class that orchestrates the agentic workflow."""

    def __init__(self):
        """Initialize the agent."""
        self.tool_executor = ToolExecutor()
        self.memory = Memory()
        self.prompts = Prompts()
        self.max_iterations = 10
        self.conversation_state = ConversationState()

    def process_request(self, user_input: str) -> AgentResponse:
        """Process a user request and return a response."""

        if self.conversation_state.has_pending_clarification():
            user_input = self._merge_clarification_with_request(user_input)
            self.conversation_state.clear()

        request = UserRequest(text=user_input)
        self.memory.add_user_message(user_input)

        state = AgentState(request=request)

        state.intent = self._classify_intent(user_input)

        state.clarifying_questions = self._generate_clarifying_questions(
            user_input, state.intent
        )

        if state.clarifying_questions:
            self._store_pending_clarification(
                user_input, state.intent, state.clarifying_questions
            )

            return AgentResponse(
                success=True,
                message="I need some clarification to help you better.",
                intent=state.intent,
                actions_taken=[],
                findings={},
                blockers=state.clarifying_questions,
                clarifying_questions=state.clarifying_questions,
            )

        state.subtasks = self._break_down_tasks(user_input, state.intent)

        tool_calls = self._plan_tool_calls(user_input, state.subtasks)

        for tool_call in tool_calls:
            try:
                result = self.tool_executor.execute(tool_call.tool, tool_call.params)
                state.tool_results.append(result)
                self.memory.add_tool_result(result)

                if not result.success:
                    state.errors.append(result.error)

            except Exception as e:
                state.errors.append(f"Error executing {tool_call.tool}: {str(e)}")

        state.summary = self._generate_summary(state)
        self.memory.add_agent_state(state)

        return AgentResponse(
            success=len(state.errors) == 0,
            message=state.summary,
            intent=state.intent,
            actions_taken=[str(call) for call in tool_calls],
            findings=self._extract_findings(state.tool_results),
            blockers=state.errors,
            clarifying_questions=[],
        )

    def _classify_intent(self, user_input: str) -> Intent:
        """Classify the user's intent."""
        text = user_input.lower()

        if any(word in text for word in ["dentist", "dental", "appointment", "doctor"]):
            return Intent.APPOINTMENT_BOOKING

        if any(
            word in text
            for word in ["coworking", "workspace", "co-working", "office space"]
        ):
            return Intent.COWORKING_SEARCH

        if any(word in text for word in ["meeting", "schedule", "calendar"]):
            return Intent.MEETING_SCHEDULING

        if any(word in text for word in ["remind", "reminder", "don't forget"]):
            return Intent.REMINDER

        if any(word in text for word in ["find", "search", "look for", "recommend"]):
            return Intent.SEARCH

        return Intent.UNKNOWN

    def _store_pending_clarification(
        self,
        original_request: str,
        intent: Intent,
        questions: list[str],
    ) -> None:
        """Store a pending clarification so the next user message can continue the original task."""
        missing_field = "unknown"

        if questions:
            first_question = questions[0].lower()

            if "city" in first_question:
                missing_field = "city"
            elif "date" in first_question or "time" in first_question:
                missing_field = "datetime"
            else:
                missing_field = "details"

        self.conversation_state.original_request = original_request
        self.conversation_state.pending_intent = intent
        self.conversation_state.missing_field = missing_field
        self.conversation_state.questions = questions

    def _merge_clarification_with_request(self, clarification: str) -> str:
        """Merge a user's clarification answer with the original pending request."""
        original_request = self.conversation_state.original_request
        missing_field = self.conversation_state.missing_field

        if not original_request:
            return clarification

        clean_request = original_request.rstrip(". ")
        clean_clarification = clarification.strip()

        if missing_field == "city":
            return f"{clean_request} in {clean_clarification} city"

        if missing_field == "datetime":
            return f"{clean_request} {clean_clarification}"

        return f"{clean_request} {clean_clarification}"

    def _generate_clarifying_questions(
        self, user_input: str, intent: Intent
    ) -> list[str]:
        """Generate clarifying questions if needed."""
        text = user_input.lower()
        questions = []

        known_cities = [
            "warsaw",
            "istanbul",
            "bursa",
            "ankara",
            "london",
            "berlin",
            "paris",
            "prague",
        ]

        if intent == Intent.APPOINTMENT_BOOKING:
            has_city = (
                any(city in text for city in known_cities)
                or " city" in text
                or " in " in text
            )

            if not has_city:
                questions.append("What city are you in?")

            has_time = any(
                word in text
                for word in [
                    "tomorrow",
                    "tonight",
                    "today",
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                    "week",
                    "at ",
                    "pm",
                    "am",
                    "after",
                    "before",
                ]
            )

            if not has_time:
                questions.append("What date and time would you prefer?")

        elif intent == Intent.COWORKING_SEARCH:
            has_city = (
                any(city in text for city in known_cities)
                or " city" in text
                or " in " in text
            )

            if not has_city:
                questions.append("Which city are you looking for coworking spaces in?")

        elif intent == Intent.MEETING_SCHEDULING:
            has_time = any(
                word in text
                for word in [
                    "today",
                    "tomorrow",
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "week",
                    "month",
                    "at ",
                    "pm",
                    "am",
                    "afternoon",
                    "morning",
                ]
            )

            if not has_time:
                questions.append("What date and time would you prefer for the meeting?")

        return questions

    def _break_down_tasks(self, user_input: str, intent: Intent) -> list[str]:
        """Break down a request into subtasks."""

        if intent == Intent.APPOINTMENT_BOOKING:
            return [
                "Identify the service type",
                "Extract location and time preferences",
                "Search for available providers",
                "Check calendar availability",
                "Book the appointment",
                "Create a reminder for the appointment",
            ]

        if intent == Intent.COWORKING_SEARCH:
            return [
                "Extract location and price requirements",
                "Search for coworking spaces matching criteria",
                "Filter by price and amenities",
                "Present options to user",
            ]

        if intent == Intent.MEETING_SCHEDULING:
            return [
                "Determine the date and time needed",
                "Check calendar availability",
                "Create a meeting reminder",
            ]

        if intent == Intent.SEARCH:
            return [
                "Identify what the user is searching for",
                "Search for matching results",
                "Present findings in organized way",
            ]

        if intent == Intent.REMINDER:
            return [
                "Extract reminder details and timing",
                "Create the reminder",
            ]

        return ["Clarify the user's intent"]

    def _plan_tool_calls(self, user_input: str, subtasks: list[str]) -> list[ToolCall]:
        """Plan which tools to call based on the request."""
        tool_calls = []
        text = user_input.lower()

        if "dentist" in text or "dental" in text or "appointment" in text:
            tool_calls.append(
                ToolCall(
                    tool=ToolName.SEARCH_SERVICE,
                    params={"query": "dentist appointment"},
                    description="Search for dentist providers",
                )
            )

            tool_calls.append(
                ToolCall(
                    tool=ToolName.CALENDAR_CHECK,
                    params={"date_range": user_input},
                    description="Check appointment availability",
                )
            )

            tool_calls.append(
                ToolCall(
                    tool=ToolName.BOOKING_SERVICE,
                    params={"option": "dentist appointment"},
                    description="Book appointment",
                )
            )

            tool_calls.append(
                ToolCall(
                    tool=ToolName.REMINDER_CREATE,
                    params={"details": f"Dentist appointment - {user_input}"},
                    description="Create appointment reminder",
                )
            )

        elif "coworking" in text or "workspace" in text or "co-working" in text:
            tool_calls.append(
                ToolCall(
                    tool=ToolName.SEARCH_SERVICE,
                    params={"query": user_input},
                    description="Search for coworking spaces",
                )
            )

        elif "meeting" in text or "schedule" in text:
            tool_calls.append(
                ToolCall(
                    tool=ToolName.CALENDAR_CHECK,
                    params={"date_range": user_input},
                    description="Check meeting availability",
                )
            )

            tool_calls.append(
                ToolCall(
                    tool=ToolName.REMINDER_CREATE,
                    params={"details": f"Meeting scheduled - {user_input}"},
                    description="Create meeting reminder",
                )
            )

        elif "remind" in text or "reminder" in text:
            tool_calls.append(
                ToolCall(
                    tool=ToolName.REMINDER_CREATE,
                    params={"details": user_input},
                    description="Create reminder",
                )
            )

        elif any(word in text for word in ["find", "search", "look"]):
            tool_calls.append(
                ToolCall(
                    tool=ToolName.SEARCH_SERVICE,
                    params={"query": user_input},
                    description="Search for information",
                )
            )

        elif any(word in text for word in ["available", "when", "check"]):
            tool_calls.append(
                ToolCall(
                    tool=ToolName.CALENDAR_CHECK,
                    params={"date_range": user_input},
                    description="Check calendar availability",
                )
            )

        return tool_calls

    def _extract_findings(self, tool_results) -> dict:
        """Extract findings from tool results."""
        findings = {}

        for result in tool_results:
            if result.success and result.data:
                tool_name = result.tool.value
                findings[tool_name] = result.data

        return findings

    def _generate_summary(self, state: AgentState) -> str:
        """Generate a summary of what was accomplished."""
        parts = []

        parts.append(f"You asked me to: {state.request.text}")

        if state.intent != Intent.UNKNOWN:
            parts.append(f"\nI understood this as a {state.intent.value} request.")

        if state.tool_results:
            parts.append("\nActions completed:")
            for result in state.tool_results:
                if result.success:
                    parts.append(f"  ✓ {result.tool.value}")
                else:
                    parts.append(f"  ✗ {result.tool.value}: {result.error}")

        findings = self._extract_findings(state.tool_results)

        if findings:
            parts.append("\nFindings:")
            for tool, data in findings.items():
                if isinstance(data, dict) and "results" in data:
                    parts.append(f"  - Found {len(data.get('results', []))} results")
                elif isinstance(data, dict):
                    parts.append(f"  - {tool}: {data}")

        if state.errors:
            parts.append("\nBlockers:")
            for error in state.errors:
                parts.append(f"  ⚠ {error}")

        return "\n".join(parts) if parts else "Request processed."

    def ask_for_clarification(self, user_input: str) -> AgentResponse:
        """Process clarification response from user."""
        self.memory.add_user_message(user_input)
        return self.process_request(user_input)