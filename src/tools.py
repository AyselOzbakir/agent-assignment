

from typing import Any
import random

from src.models import ToolName, ToolResult


class ToolExecutor:
    """Executes tools and returns ToolResult objects."""

    def __init__(self):
        """Initialize mock data."""
        self.search_results_db = {
            "coworking": [
                {
                    "name": "HubSpace Warsaw",
                    "location": "Warsaw, Poland",
                    "price": "$18/day",
                    "amenities": ["WiFi", "Coffee", "Meeting rooms"],
                    "rating": 4.7,
                },
                {
                    "name": "WorkNest",
                    "location": "Warsaw, Poland",
                    "price": "$15/day",
                    "amenities": ["High-speed WiFi", "24/7 access", "Events"],
                    "rating": 4.5,
                },
                {
                    "name": "ProSpace Warsaw",
                    "location": "Warsaw, Poland",
                    "price": "$19/day",
                    "amenities": ["Private desks", "WiFi", "Coffee bar"],
                    "rating": 4.6,
                },
            ],
            "dentist": [
                {
                    "name": "Smile Dental Clinic",
                    "location": "Warsaw, Poland",
                    "availability": "Mon-Fri 9am-6pm",
                    "rating": 4.8,
                    "services": ["Checkup", "Cleaning", "Whitening"],
                },
                {
                    "name": "Modern Teeth Warsaw",
                    "location": "Warsaw, Poland",
                    "availability": "Mon-Sat 10am-7pm",
                    "rating": 4.6,
                    "services": ["Checkup", "Cleaning", "Root canal"],
                },
                {
                    "name": "DentaPoint",
                    "location": "Warsaw, Poland",
                    "availability": "Mon-Fri 8am-5pm",
                    "rating": 4.4,
                    "services": ["Checkup", "Cleaning", "Implants"],
                },
            ],
        }

    def calendar_check(self, date_range: str) -> ToolResult:
        """Mock calendar availability checker."""
        query = date_range.lower()

        if "after 5pm" in query or "after 5 pm" in query:
            data = {
                "query": date_range,
                "available_slots": [
                    "2026-05-11 17:30",
                    "2026-05-12 18:00",
                    "2026-05-13 18:30",
                ],
                "total_available": 3,
            }

        elif "next tuesday" in query:
            data = {
                "query": date_range,
                "available_slots": [
                    "2026-05-12 14:00",
                    "2026-05-12 15:30",
                    "2026-05-12 16:00",
                ],
                "total_available": 3,
            }

        elif "next week" in query:
            data = {
                "query": date_range,
                "available_slots": [
                    "2026-05-11 10:00",
                    "2026-05-12 14:00",
                    "2026-05-13 16:00",
                ],
                "total_available": 3,
            }

        else:
            data = {
                "query": date_range,
                "available_slots": [],
                "total_available": 0,
                "error": "No available slots found for the requested date range.",
            }

        return ToolResult(
            tool=ToolName.CALENDAR_CHECK,
            success=data["total_available"] > 0,
            data=data,
            error=None if data["total_available"] > 0 else data["error"],
        )

    def search_service(self, query: str) -> ToolResult:
        """Search for services or items using mock data."""
        try:
            text = query.lower()

            if "coworking" in text or "workspace" in text or "co-working" in text:
                search_type = "coworking"
            elif "dentist" in text or "dental" in text or "appointment" in text:
                search_type = "dentist"
            else:
                search_type = "coworking" if "work" in text or "space" in text else "dentist"

            results = self.search_results_db.get(search_type, [])

            return ToolResult(
                tool=ToolName.SEARCH_SERVICE,
                success=True,
                data={
                    "query": query,
                    "results": results,
                    "total": len(results),
                },
                error=None,
            )

        except Exception as e:
            return ToolResult(
                tool=ToolName.SEARCH_SERVICE,
                success=False,
                data={},
                error=f"Search failed: {str(e)}",
            )

    def booking_service(self, option: str) -> ToolResult:
        """Book an option using a mock booking service."""
        try:
            confirmation_id = f"BOOKING-{random.randint(10000, 99999)}"

            return ToolResult(
                tool=ToolName.BOOKING_SERVICE,
                success=True,
                data={
                    "confirmation_id": confirmation_id,
                    "booking": option,
                    "status": "confirmed",
                    "confirmation_sent_to": "user@example.com",
                },
                error=None,
            )

        except Exception as e:
            return ToolResult(
                tool=ToolName.BOOKING_SERVICE,
                success=False,
                data={},
                error=f"Booking failed: {str(e)}",
            )

    def reminder_create(self, details: str) -> ToolResult:
        """Create a reminder using a mock reminder service."""
        try:
            reminder_id = f"REM-{random.randint(10000, 99999)}"

            return ToolResult(
                tool=ToolName.REMINDER_CREATE,
                success=True,
                data={
                    "reminder_id": reminder_id,
                    "details": details,
                    "status": "set",
                },
                error=None,
            )

        except Exception as e:
            return ToolResult(
                tool=ToolName.REMINDER_CREATE,
                success=False,
                data={},
                error=f"Reminder creation failed: {str(e)}",
            )

    def execute(self, tool_name: ToolName, params: dict[str, Any]) -> ToolResult:
        """Execute a tool by name with given parameters."""
        if tool_name == ToolName.CALENDAR_CHECK:
            return self.calendar_check(params.get("date_range", ""))

        if tool_name == ToolName.SEARCH_SERVICE:
            return self.search_service(params.get("query", ""))

        if tool_name == ToolName.BOOKING_SERVICE:
            return self.booking_service(params.get("option", ""))

        if tool_name == ToolName.REMINDER_CREATE:
            return self.reminder_create(params.get("details", ""))

        return ToolResult(
            tool=tool_name,
            success=False,
            data={},
            error=f"Unknown tool: {tool_name}",
        )