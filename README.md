# Task Execution AI Agent

A command-line task execution AI agent built for a Junior AI Agentic Engineer take-home assignment.

The agent takes a natural language user request, identifies the intent, breaks the task into subtasks, asks clarifying questions when required, uses mock tools, handles missing information and tool failures, and returns a structured final response.

## Assignment Goal

The assignment asks for an AI agent that can complete real-world assistant tasks such as:

- Booking an appointment
- Finding services or places
- Planning or scheduling tasks
- Creating reminders

This implementation focuses on the core agentic workflow rather than real external integrations.

## Features

- Natural language request handling
- Intent detection
- Task decomposition
- Clarifying questions for missing information
- Multi-turn clarification handling
- Mock tool orchestration
- Error and blocker reporting
- Structured final summaries
- CLI interface
- Python project managed with `uv`

## Supported Task Types

The current implementation supports:

- Finding coworking spaces
- Booking dentist appointments
- Scheduling meetings
- Creating reminders

## LLM Integration

The main CLI flow uses deterministic routing for reliability and easy evaluation. The project also includes an optional OpenAI-backed parser scaffold in `src/llm_parser.py`.

This allows the rule-based intent classification step to be replaced or augmented with an LLM parser when `OPENAI_API_KEY` is configured.

## Required Tools

The assignment required the following tools. They are implemented as deterministic mock tools:

- `calendar_check(date_range)`
- `search_service(query)`
- `booking_service(option)`
- `reminder_create(details)`

## Extra Features

In addition to the core requirements, this project includes:

- Multi-turn clarification memory
- Structured action trace showing which tools were called
- Rich CLI output
- Non-interactive CLI test commands
- Separate architecture and quickstart documentation

## How the Agent Works

The agent follows this workflow:

1. Receive a user request.
2. Classify the intent.
3. Check whether required information is missing.
4. Ask a clarifying question if needed.
5. Store the pending clarification state.
6. Merge the user’s clarification with the original request.
7. Break the task into subtasks.
8. Plan tool calls.
9. Execute the required mock tools.
10. Return a structured summary with actions, findings, and blockers.

## Example Flow: Coworking Search

Input:

```text
Find me 3 coworking spaces in Warsaw under $20/day.
```
