# Task Execution AI Agent

A task execution AI agent built for a Junior AI Agentic Engineer take-home assignment.

The agent can understand natural language requests, identify intent, break requests into subtasks, ask clarifying questions, use mock tools, handle missing information and failures, and return structured final results.

The project includes both a CLI interface and a Streamlit web UI.

## Features

- Intent detection
- Task decomposition
- Clarifying questions
- Multi-turn context handling
- Mock tool orchestration
- Missing information handling
- Failure and blocker reporting
- Structured final summaries
- CLI interface
- Streamlit web UI
- Optional OpenAI-backed parser with deterministic fallback
- Trip planning with budget checking
- Calendar availability across a mock 7-day schedule

## Supported Task Types

The current implementation supports:

- Coworking space search
- Dentist appointment booking
- Meeting scheduling
- Trip planning
- Reminder creation

## Required Tools

The assignment required the following tools. They are implemented as mock tools:

- `calendar_check(date_range)`
- `search_service(query)`
- `booking_service(option)`
- `reminder_create(details)`

The project also includes an additional mock tool:

- `budget_check(request)`

This tool is used for trip-planning requests with budget constraints.

## LLM Integration

The agent includes an optional OpenAI-backed parser in `src/llm_parser.py`.

When `OPENAI_API_KEY` is configured, the agent can use the LLM parser for intent understanding. If no API key is available, the agent safely falls back to deterministic rule-based routing.

This keeps the project easy to run during review while still supporting LLM-based parsing.

## Data Source Note

The search, booking, calendar, reminder, and budget tools are implemented as mock tools. They simulate external services but do not fetch live data.

The mock dataset is intentionally small and focused on:

- Warsaw coworking examples
- Warsaw and Istanbul dentist examples
- Prague trip-planning examples
- Mock calendar availability

Live restaurant, travel, calendar, or place data would require separate third-party API integrations.

## Example Workflows

### 1. Coworking Search

Input:

```text
Find me 3 coworking spaces in Warsaw under $20/day.
```

Expected behavior:

- Identifies the request as `coworking_search`
- Calls `search_service`
- Returns 3 coworking options in Warsaw
- Shows price, location, rating, and amenities

### 2. Dentist Appointment Booking

Input:

```text
Book me a dentist appointment next week after 5pm.
```

The agent asks:

```text
What city are you in?
```

User clarification:

```text
Warsaw
```

Expected behavior:

- Merges the clarification with the original request
- Identifies the request as `appointment_booking`
- Calls `search_service`
- Calls `calendar_check`
- Calls `booking_service`
- Calls `reminder_create`
- Returns available slots, booking confirmation, and reminder ID

### 3. Meeting Scheduling

Input:

```text
Schedule a meeting with John next Tuesday afternoon.
```

Expected behavior:

- Identifies the request as `meeting_scheduling`
- Calls `calendar_check`
- Calls `reminder_create`
- Returns available meeting slots and reminder details

### 4. Trip Planning

Input:

```text
Plan a 2-day trip to Prague under €300.
```

Expected behavior:

- Identifies the request as `trip_planning`
- Searches for hotel options
- Searches for flight options
- Checks whether the trip fits the budget
- Creates a trip reminder
- Returns a cost breakdown

Example budget result:

```text
Budget limit: €300
Estimated total: €230
Fits budget: Yes
Accommodation: €160
Transportation: €70
Contingency: €50
```

## Setup

Install dependencies with `uv`:

```bash
uv sync
```

## Run the CLI

```bash
uv run python main.py
```

Then type a request into the CLI.

To exit:

```text
quit
```

## Run the Streamlit UI

```bash
uv run streamlit run streamlit_app.py
```

This opens a local browser-based interface for interacting with the agent.

## Non-Interactive Test Commands

Coworking search:

```bash
printf "Find me 3 coworking spaces in Warsaw under \$20/day.\nquit\n" | uv run python main.py
```

Dentist appointment booking with clarification:

```bash
printf "Book me a dentist appointment next week after 5pm.\nWarsaw\nquit\n" | uv run python main.py
```

Meeting scheduling:

```bash
printf "Schedule a meeting with John next Tuesday afternoon.\nquit\n" | uv run python main.py
```

Trip planning:

```bash
printf "Plan a 2-day trip to Prague under €300.\nquit\n" | uv run python main.py
```

## Project Structure

```text
agent-assignment/
├── main.py
├── streamlit_app.py
├── pyproject.toml
├── uv.lock
├── .env.example
├── README.md
├── ARCHITECTURE.md
├── QUICKSTART.md
└── src/
    ├── agent.py
    ├── llm_parser.py
    ├── memory.py
    ├── models.py
    ├── prompts.py
    └── tools.py
```

## Design Notes

The agent follows this workflow:

1. Receive a user request.
2. Classify the intent.
3. Check whether required information is missing.
4. Ask clarifying questions when needed.
5. Store pending clarification state.
6. Merge the user's clarification with the original request.
7. Break the task into subtasks.
8. Plan tool calls.
9. Execute mock tools.
10. Return a structured response with actions, findings, and blockers.

## Error Handling

The agent reports blockers when:

- Required information is missing
- A tool returns no result
- A tool execution fails
- The request cannot be confidently handled
- Mock data is unavailable for a requested scenario

## Limitations

- The tools use mock data, not live APIs.
- Search results are limited to sample data.
- Real booking, calendar, travel, and reminder integrations are not included.
- The OpenAI parser is optional and falls back to deterministic routing if no API key is configured.
- Geographic coverage is intentionally limited for reliable evaluation.

## Future Improvements

- Add real calendar integration
- Add real search APIs such as Google Places or travel APIs
- Add real booking providers
- Add persistent database-backed memory
- Add automated tests
- Add richer option-selection flows for booking a selected result
- Expand mock data coverage for more cities and travel destinations
