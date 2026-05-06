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
            "hotels prague": [
                {
                    "name": "Prague Central Hotel",
                    "location": "Prague, Czech Republic",
                    "price": "€80/night",
                    "total_2_nights": "€160",
                    "amenities": ["WiFi", "Breakfast", "Gym"],
                    "rating": 4.6,
                },
                {
                    "name": "Charles Bridge View Hostel",
                    "location": "Prague, Czech Republic",
                    "price": "€45/night",
                    "total_2_nights": "€90",
                    "amenities": ["Free WiFi", "Kitchen", "Rooftop bar"],
                    "rating": 4.4,
                },
                {
                    "name": "Old Town Boutique",
                    "location": "Prague, Czech Republic",
                    "price": "€95/night",
                    "total_2_nights": "€190",
                    "amenities": ["WiFi", "Spa", "Restaurant"],
                    "rating": 4.8,
                },
            ],
            "flights prague": [
                {
                    "name": "Direct Flight to Prague",
                    "route": "Your City → Prague",
                    "price": "€80",
                    "duration": "2-3 hours",
                    "rating": 4.5,
                },
                {
                    "name": "Budget Flight to Prague",
                    "route": "Your City → Prague",
                    "price": "€50",
                    "duration": "4-5 hours",
                    "rating": 4.2,
                },
                {
                    "name": "Premium Flight to Prague",
                    "route": "Your City → Prague",
                    "price": "€120",
                    "duration": "2 hours",
                    "rating": 4.9,
                },
            ],
        }

    def calendar_check(self, date_range: str) -> ToolResult:
        """Mock calendar availability checker.

        Returns realistic availability across the next 7 days based on simple
        time preferences in the user's request.
        """
        query = date_range.lower()

        weekly_slots = {
            "2026-05-11 Monday": {
                "morning": ["09:30", "10:30", "11:00"],
                "afternoon": ["13:00", "14:30", "16:00"],
                "evening": ["17:30", "18:00", "18:30"],
            },
            "2026-05-12 Tuesday": {
                "morning": ["09:00", "10:00", "11:30"],
                "afternoon": ["14:00", "15:30", "16:00"],
                "evening": ["17:30", "18:15", "19:00"],
            },
            "2026-05-13 Wednesday": {
                "morning": ["09:30", "10:45", "11:15"],
                "afternoon": ["13:30", "15:00", "16:30"],
                "evening": ["17:15", "18:00", "18:45"],
            },
            "2026-05-14 Thursday": {
                "morning": ["09:00", "10:30", "11:00"],
                "afternoon": ["13:00", "14:00", "15:30"],
                "evening": ["17:30", "18:30", "19:00"],
            },
            "2026-05-15 Friday": {
                "morning": ["09:30", "10:30", "11:00"],
                "afternoon": ["13:00", "15:00", "16:30"],
                "evening": ["17:30", "18:00", "18:30"],
            },
            "2026-05-16 Saturday": {
                "morning": ["10:00", "11:00"],
                "afternoon": ["13:30", "15:00"],
                "evening": ["17:00"],
            },
            "2026-05-17 Sunday": {
                "morning": ["10:30"],
                "afternoon": ["14:00", "16:00"],
                "evening": ["17:30"],
            },
        }

        def flatten_slots(period: str | None = None) -> list[str]:
            slots = []

            for day, periods in weekly_slots.items():
                if period:
                    for time in periods[period]:
                        slots.append(f"{day} {time}")
                else:
                    for times in periods.values():
                        for time in times:
                            slots.append(f"{day} {time}")

            return slots

        requested_day = None

        day_map = {
            "monday": "2026-05-11 Monday",
            "tuesday": "2026-05-12 Tuesday",
            "wednesday": "2026-05-13 Wednesday",
            "thursday": "2026-05-14 Thursday",
            "friday": "2026-05-15 Friday",
            "saturday": "2026-05-16 Saturday",
            "sunday": "2026-05-17 Sunday",
        }

        for day_name, full_day in day_map.items():
            if day_name in query:
                requested_day = full_day
                break

        if "after" in query and "pm" in query:
            preferred_period = "evening"
        elif "morning" in query:
            preferred_period = "morning"
        elif "afternoon" in query:
            preferred_period = "afternoon"
        elif "evening" in query:
            preferred_period = "evening"
        else:
            preferred_period = None

        if requested_day:
            periods = weekly_slots[requested_day]

            if preferred_period:
                available_slots = [
                    f"{requested_day} {time}" for time in periods[preferred_period]
                ]
            else:
                available_slots = [
                    f"{requested_day} {time}"
                    for times in periods.values()
                    for time in times
                ]

        elif "next week" in query or "week" in query:
            available_slots = flatten_slots(preferred_period)

        elif "tomorrow" in query:
            tomorrow = "2026-05-07 Thursday"
            # Keep tomorrow simple for mock purposes.
            available_slots = [
                f"{tomorrow} 10:00",
                f"{tomorrow} 14:00",
                f"{tomorrow} 17:30",
            ]

            if preferred_period == "morning":
                available_slots = [f"{tomorrow} 10:00"]
            elif preferred_period == "afternoon":
                available_slots = [f"{tomorrow} 14:00"]
            elif preferred_period == "evening":
                available_slots = [f"{tomorrow} 17:30"]

        else:
            # Default to a small representative sample instead of failing immediately.
            available_slots = [
                "2026-05-11 Monday 10:30",
                "2026-05-12 Tuesday 14:00",
                "2026-05-13 Wednesday 17:30",
            ]

        # Keep output readable by showing the first 7 matches.
        available_slots = available_slots[:7]

        data = {
            "query": date_range,
            "available_slots": available_slots,
            "total_available": len(available_slots),
        }

        return ToolResult(
            tool=ToolName.CALENDAR_CHECK,
            success=len(available_slots) > 0,
            data=data,
            error=None if available_slots else "No available slots found.",
        )
    def search_service(self, query: str, city: str = "Warsaw") -> ToolResult:
        """Search for services or items using mock data."""
        try:
            text = query.lower()

            country_map = {
                "Istanbul": "Turkey",
                "Ankara": "Turkey",
                "Bursa": "Turkey",
                "Warsaw": "Poland",
                "Berlin": "Germany",
                "London": "UK",
                "Paris": "France",
                "Prague": "Czech Republic",
            }
            country = country_map.get(city, None)

            if "coworking" in text or "workspace" in text or "co-working" in text:
                search_type = "coworking"
            elif "dentist" in text or "dental" in text or "appointment" in text:
                search_type = "dentist"
            elif "hotel" in text or "accommodation" in text:
                if "prague" in text:
                    search_type = "hotels prague"
                else:
                    search_type = "hotels prague"  # Default to Prague for demo
            elif "flight" in text or "transportation" in text:
                if "prague" in text:
                    search_type = "flights prague"
                else:
                    search_type = "flights prague"  # Default to Prague for demo
            else:
                search_type = "coworking" if "work" in text or "space" in text else "dentist"

            # Generate dynamic results based on city for dentist and coworking
            if search_type == "dentist":
                results = [
                    {
                        "name": f"Smile Dental Clinic",
                        "location": f"{city}, {country}" if country else city,
                        "availability": "Mon-Fri 9am-6pm",
                        "rating": 4.8,
                        "services": ["Checkup", "Cleaning", "Whitening"],
                    },
                    {
                        "name": f"Modern Teeth {city}",
                        "location": f"{city}, {country}" if country else city,
                        "availability": "Mon-Sat 10am-7pm",
                        "rating": 4.6,
                        "services": ["Checkup", "Cleaning", "Root canal"],
                    },
                    {
                        "name": f"DentaPoint",
                        "location": f"{city}, {country}" if country else city,
                        "availability": "Mon-Fri 8am-5pm",
                        "rating": 4.4,
                        "services": ["Checkup", "Cleaning", "Implants"],
                    },
                ]
            elif search_type == "coworking":
                results = [
                    {
                        "name": f"HubSpace {city}",
                        "location": f"{city}, {country}" if country else city,
                        "price": "$18/day",
                        "amenities": ["WiFi", "Coffee", "Meeting rooms"],
                        "rating": 4.7,
                    },
                    {
                        "name": f"WorkNest",
                        "location": f"{city}, {country}" if country else city,
                        "price": "$15/day",
                        "amenities": ["High-speed WiFi", "24/7 access", "Events"],
                        "rating": 4.5,
                    },
                    {
                        "name": f"ProSpace {city}",
                        "location": f"{city}, {country}" if country else city,
                        "price": "$19/day",
                        "amenities": ["Private desks", "WiFi", "Coffee bar"],
                        "rating": 4.6,
                    },
                ]
            else:
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

    def budget_check(self, request: str) -> ToolResult:
        """Check if trip costs fit within budget constraints."""
        try:
            import re
            text = request.lower()

            # Extract budget from request
            budget_match = re.search(r'under\s+[€$]?(\d+)', text)
            budget = None
            if budget_match:
                budget = int(budget_match.group(1))

            # Mock calculation
            estimated_cost = 0
            if "prague" in text or "2-day" in text or "2 day" in text:
                # Hotel + flights for Prague 2-day trip
                estimated_cost = 230  # €160 (hotel) + €70 (avg flight)

            result_data = {
                "budget_limit": budget,
                "estimated_total": estimated_cost,
                "fits_budget": budget is None or estimated_cost <= budget,
                "breakdown": {
                    "accommodation": "€160 (2 nights)",
                    "transportation": "€70 (round-trip flight)",
                    "contingency": "€50 (meals, activities)",
                    "total": f"€{estimated_cost}",
                }
            }

            return ToolResult(
                tool=ToolName.BUDGET_CHECK,
                success=True,
                data=result_data,
                error=None,
            )

        except Exception as e:
            return ToolResult(
                tool=ToolName.BUDGET_CHECK,
                success=False,
                data={},
                error=f"Budget check failed: {str(e)}",
            )

    def execute(self, tool_name: ToolName, params: dict[str, Any]) -> ToolResult:
        """Execute a tool by name with given parameters."""
        if tool_name == ToolName.CALENDAR_CHECK:
            return self.calendar_check(params.get("date_range", ""))

        if tool_name == ToolName.SEARCH_SERVICE:
            return self.search_service(params.get("query", ""), params.get("city", "Warsaw"))

        if tool_name == ToolName.BOOKING_SERVICE:
            return self.booking_service(params.get("option", ""))

        if tool_name == ToolName.REMINDER_CREATE:
            return self.reminder_create(params.get("details", ""))

        if tool_name == ToolName.BUDGET_CHECK:
            return self.budget_check(params.get("request", ""))

        return ToolResult(
            tool=tool_name,
            success=False,
            data={},
            error=f"Unknown tool: {tool_name}",
        )