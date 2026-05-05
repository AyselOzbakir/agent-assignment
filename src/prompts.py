"""
Prompt templates for the agent.

Contains templates for intent classification, task breakdown, clarifying questions,
and final summaries.
"""


class Prompts:
    """Prompt templates for the agent."""

    @staticmethod
    def intent_classifier() -> str:
        """Prompt to classify user intent."""
        return """You are an intent classification system. Analyze the user's request and classify their intent.

Possible intents:
- COWORKING_SEARCH: User is searching for coworking spaces or office spaces
- APPOINTMENT_BOOKING: User wants to book a dentist, doctor, or medical appointment
- MEETING_SCHEDULING: User wants to schedule a business meeting
- SEARCH: User wants to find general information
- REMINDER: User wants to set a reminder or notification

User request: {request}

Respond with ONLY the intent name (COWORKING_SEARCH, APPOINTMENT_BOOKING, MEETING_SCHEDULING, SEARCH, or REMINDER).
If unclear, respond with UNKNOWN."""

    @staticmethod
    def task_breakdown() -> str:
        """Prompt to break down a request into subtasks."""
        return """You are a task planning agent. Break down the user's request into clear, actionable subtasks.

User request: {request}
Detected intent: {intent}

Create a numbered list of 2-4 subtasks that need to be completed to fulfill the request.
Format as a simple list, one per line.

Example:
1. Check calendar availability for the requested date
2. Search for available restaurants matching the criteria
3. Confirm booking with user"""

    @staticmethod
    def clarifying_questions() -> str:
        """Prompt to generate clarifying questions."""
        return """You are a helpful assistant. The user's request might need clarification.

User request: {request}
Detected intent: {intent}

Generate 0-3 clarifying questions to better understand the request.
Only include questions if they're truly necessary for proceeding.
Format as a numbered list.

Examples of good questions:
- "What date are you looking for?"
- "How many people will be attending?"
- "What's your budget range?"

If no clarification is needed, respond with: NO_CLARIFICATION_NEEDED"""

    @staticmethod
    def summary_generator() -> str:
        """Prompt to generate a final summary."""
        return """You are a summary generator. Create a clear, concise summary of what the agent accomplished.

User request: {request}
Intent: {intent}

Actions taken: {actions}
Tool results: {results}
Any blockers encountered: {blockers}

Generate a friendly summary that includes:
1. What was requested
2. What actions were taken
3. What was found or booked
4. Any remaining issues or blockers

Keep it under 100 words."""

    @staticmethod
    def tool_decision() -> str:
        """Prompt to decide which tools to use."""
        return """You are a tool selection agent. Determine which tools to use to fulfill the request.

Available tools:
- calendar_check(date_range): Check calendar availability
- search_service(query): Search for services/items
- booking_service(option): Book something
- reminder_create(details): Create a reminder

User request: {request}
Identified subtasks: {subtasks}

List the tools you would use, in order, with parameters.
Format as JSON array.

Example:
[
  {{"tool": "search_service", "params": {{"query": "restaurants in NYC"}}}},
  {{"tool": "calendar_check", "params": {{"date_range": "tomorrow evening"}}}}
]

If no tools are needed, respond with: []"""
