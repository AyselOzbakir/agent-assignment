import json
import streamlit as st

from src.agent import Agent


st.set_page_config(
    page_title="AI Agent Assignment",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Agent Assignment")
st.caption("A simple task execution AI agent with tool orchestration and clarification flow.")


def format_response(response) -> str:
    parts = []

    if response.intent:
        try:
            parts.append(f"**Intent:** `{response.intent.value}`")
        except Exception:
            parts.append(f"**Intent:** `{response.intent}`")

    if response.actions_taken:
        parts.append("\n**Actions completed:**")
        for action in response.actions_taken:
            tool_name = action.split("(")[0]
            parts.append(f"- ✅ `{tool_name}`")

    if response.findings:
        parts.append("\n**Results:**")

        for tool, data in response.findings.items():
            if not isinstance(data, dict):
                continue

            results = data.get("results")

            if results:
                for index, item in enumerate(results, start=1):
                    name = item.get("name", "Unnamed option")
                    parts.append(f"\n### {index}. {name}")

                    if item.get("location"):
                        parts.append(f"- **Location:** {item['location']}")

                    if item.get("route"):
                        parts.append(f"- **Route:** {item['route']}")

                    if item.get("price"):
                        parts.append(f"- **Price:** {item['price']}")

                    if item.get("duration"):
                        parts.append(f"- **Duration:** {item['duration']}")

                    if item.get("rating"):
                        parts.append(f"- **Rating:** {item['rating']}")

                    if item.get("availability"):
                        parts.append(f"- **Availability:** {item['availability']}")

                    if item.get("amenities"):
                        parts.append(f"- **Amenities:** {', '.join(item['amenities'])}")

                    if item.get("services"):
                        parts.append(f"- **Services:** {', '.join(item['services'])}")

            if "available_slots" in data:
                parts.append("\n### Available slots")
                for slot in data["available_slots"]:
                    parts.append(f"- {slot}")

            if "budget_limit" in data:
                parts.append("\n### Budget check")
                parts.append(f"- **Budget limit:** €{data.get('budget_limit')}")
                parts.append(f"- **Estimated total:** €{data.get('estimated_total')}")
                parts.append(
                    f"- **Fits budget:** {'Yes' if data.get('fits_budget') else 'No'}"
                )

                breakdown = data.get("breakdown", {})
                if breakdown:
                    parts.append("\n**Cost breakdown:**")
                    for key, value in breakdown.items():
                        parts.append(f"- **{key.title()}:** {value}")

            if "confirmation_id" in data:
                parts.append("\n### Booking confirmation")
                parts.append(f"- **Confirmation ID:** {data['confirmation_id']}")
                parts.append(f"- **Status:** {data.get('status', 'confirmed')}")

            if "reminder_id" in data:
                parts.append("\n### Reminder")
                parts.append(f"- **Reminder ID:** {data['reminder_id']}")
                parts.append(f"- **Status:** {data.get('status', 'set')}")

    if response.blockers:
        parts.append("\n**Blockers / Clarifications:**")
        for blocker in response.blockers:
            parts.append(f"- {blocker}")

    if not parts and response.message:
        parts.append(response.message)

    return "\n".join(parts)


if "agent" not in st.session_state:
    st.session_state.agent = Agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your request...")

if user_input:
    # Kullanıcı mesajı
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agent cevabı
    response = st.session_state.agent.process_request(user_input)
    assistant_text = format_response(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_text}
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_text)