"""
Optional OpenAI-backed intent parser.

The main agent uses deterministic routing for reliability in the CLI demo.
This module provides an OpenAI-based parser scaffold that can be used to
replace or augment rule-based intent classification.
"""

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def parse_request_with_llm(user_request: str) -> dict[str, Any]:
    """Parse a user request into intent, missing fields, and subtasks using OpenAI.

    This function is intentionally optional so the CLI can still run without an
    API key during evaluation.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "used_llm": False,
            "intent": "unknown",
            "missing_fields": [],
            "subtasks": [],
            "reason": "OPENAI_API_KEY is not set.",
        }

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an intent parser for a task execution AI agent.

Given a user request, return JSON with:
- intent
- missing_fields
- subtasks

Supported intents:
- coworking_search
- appointment_booking
- meeting_scheduling
- reminder
- search
- unknown

User request:
{user_request}

Return only valid JSON.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    text = response.output_text

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {
            "used_llm": True,
            "intent": "unknown",
            "missing_fields": [],
            "subtasks": [],
            "raw_output": text,
        }

    parsed["used_llm"] = True
    return parsed