"""
Main entry point for the agent assignment.

Provides an interactive interface to test the agent with various user requests.
"""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
import json

from src.agent import Agent
from src.models import AgentResponse, Intent


class AgentInterface:
    """Interactive interface for the agent."""

    def __init__(self):
        """Initialize the interface."""
        self.agent = Agent()
        self.console = Console()
        self.running = True

    def display_welcome(self) -> None:
        """Display welcome message."""
        welcome = """
[bold cyan]AI Agent Assignment[/bold cyan]
[dim]A junior engineer's take-home assignment[/dim]

This agent can help you with:
• [yellow]Finding[/yellow] coworking spaces
• [yellow]Booking[/yellow] dentist appointments
• [yellow]Scheduling[/yellow] meetings and checking availability
• [yellow]Setting reminders[/yellow]

Type 'help' for commands or 'quit' to exit.
"""
        self.console.print(Panel(welcome, border_style="cyan"))

    def display_response(self, response: AgentResponse) -> None:
        """Display the agent's response in a formatted way.

        Args:
            response: The agent's response
        """
        # Main message
        self.console.print(f"\n[bold green]Agent Response:[/bold green]")
        self.console.print(f"\n{response.message}\n")

        # Intent
        intent_color = "yellow" if response.intent == Intent.UNKNOWN else "cyan"
        self.console.print(f"[{intent_color}]Intent:[/{intent_color}] {response.intent.value}")

        # Actions taken
        if response.actions_taken:
            self.console.print("\n[bold]Actions Taken:[/bold]")
            for action in response.actions_taken:
                self.console.print(f"  • {action}")

        # Findings
        if response.findings:
            self.console.print("\n[bold]Findings:[/bold]")
            for tool, data in response.findings.items():
                self.console.print(f"  {tool}:")
                # Pretty print the data
                json_str = json.dumps(data, indent=2)
                self.console.print(
                    Syntax(json_str, "json", theme="monokai", line_numbers=False)
                )

        # Clarifying questions
        if response.clarifying_questions:
            self.console.print("\n[bold yellow]⚠ Clarification Needed:[/bold yellow]")
            for i, question in enumerate(response.clarifying_questions, 1):
                self.console.print(f"  {i}. {question}")

        # Blockers
        if response.blockers:
            self.console.print("\n[bold red]Blockers:[/bold red]")
            for blocker in response.blockers:
                self.console.print(f"  ✗ {blocker}")

        # Status
        status = "[bold green]✓ Success[/bold green]" if response.success else "[bold red]✗ Failed[/bold red]"
        self.console.print(f"\n{status}")

    def display_help(self) -> None:
        """Display help message."""
        help_text = """
[bold]Available Commands:[/bold]

[cyan]Examples you can try:[/cyan]
• "Find me 3 coworking spaces in Warsaw under $20/day"
• "Book me a dentist appointment next week after 5pm in Warsaw"
• "Schedule a meeting next Monday at 2pm"
• "Remind me to call John tomorrow at 3pm"
• "What coworking spaces are available in the city?"

[cyan]Commands:[/cyan]
• help      - Show this help message
• memory    - Show conversation memory summary
• clear     - Clear memory and start fresh
• quit/exit - Exit the program

[cyan]Tips:[/cyan]
• Be specific with dates, times, and locations for better results
• For appointments, include both date/time and location (e.g., "Warsaw")
• The agent may ask clarifying questions
"""
        self.console.print(Panel(help_text, border_style="blue", title="Help"))

    def display_memory(self) -> None:
        """Display memory summary."""
        summary = self.agent.memory.get_summary()
        context = self.agent.memory.get_context(max_messages=5)

        self.console.print(
            Panel(
                f"[bold]Memory Summary:[/bold]\n{summary}\n\n[dim]{context}[/dim]",
                border_style="magenta",
                title="Memory",
            )
        )

    def run(self) -> None:
        """Main interactive loop."""
        self.display_welcome()

        while self.running:
            try:
                # Get user input
                user_input = self.console.input(
                    "\n[bold cyan]You:[/bold cyan] "
                ).strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() == "quit" or user_input.lower() == "exit":
                    self.console.print(
                        "[bold yellow]Thanks for using the agent! Goodbye.[/bold yellow]"
                    )
                    self.running = False
                    break

                if user_input.lower() == "help":
                    self.display_help()
                    continue

                if user_input.lower() == "memory":
                    self.display_memory()
                    continue

                if user_input.lower() == "clear":
                    self.agent.memory.clear()
                    self.console.print("[green]Memory cleared.[/green]")
                    continue

                # Process request
                response = self.agent.process_request(user_input)
                self.display_response(response)

                # If clarification needed, ask for more info
                if response.clarifying_questions:
                    clarification = self.console.input(
                        "\n[bold cyan]Please clarify:[/bold cyan] "
                    ).strip()

                    if clarification:
                        response = self.agent.ask_for_clarification(clarification)
                        self.display_response(response)

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted.[/yellow]")
                self.running = False
            except Exception as e:
                self.console.print(f"[bold red]Error:[/bold red] {str(e)}")


def main() -> None:
    """Main entry point."""
    interface = AgentInterface()
    interface.run()


if __name__ == "__main__":
    main()
