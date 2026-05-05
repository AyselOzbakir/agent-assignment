# Quick Start Guide

Get the agent running in 2 minutes.

## Setup (First Time Only)

```bash
# 1. Make sure you're in the project directory
cd agent-assignment

# 2. Install dependencies with uv
uv sync

# 3. Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

## Run the Agent

```bash
python main.py
```

You'll see a welcome screen with examples. Start typing requests!

## Try These Examples

````
# Coworking space search
Find me 3 coworking spaces in Warsaw under $20/day

# Dentist appointment booking
Book me a dentist appointment next week after 5pm in Warsaw

# Scheduling request
Schedule a meeting next Monday at 2pm
## Available Commands

Once running, type these commands:

| Command          | What it does              |
| ---------------- | ------------------------- |
| `help`           | Show examples and tips    |
| `memory`         | View conversation history |
| `clear`          | Reset all memory          |
| `quit` or `exit` | End session               |

## Understanding the Output

The agent shows:

- **Intent** - What it understood you were asking for
- **Actions Taken** - Which tools were executed
- **Findings** - What was discovered
- **Blockers** - Any issues encountered

## Project Files

Start with these files to understand the code:

1. **`main.py`** - Entry point, see how the CLI works
2. **`src/models.py`** - Data structures, understand the types
3. **`src/agent.py`** - Core logic, see the workflow
4. **`src/tools.py`** - Tool implementations, see how they work
5. **`src/memory.py`** - Memory tracking
6. **`src/prompts.py`** - Prompt templates for LLMs

## Next Steps

- Read `README.md` for full documentation
- Read `ARCHITECTURE.md` for design decisions
- Modify `src/agent.py` to change behavior
- Replace heuristics with LLM calls for more sophisticated reasoning

## Common Tasks

### Want to modify how the agent behaves?

Edit `src/agent.py` - look at these methods:

- `_classify_intent()` - Change intent detection
- `_plan_tool_calls()` - Change which tools are used
- `_generate_clarifying_questions()` - Change when to ask questions

### Want to add a new tool?

Edit `src/tools.py`:

1. Add tool name to `ToolName` enum in `models.py`
2. Add method to `ToolExecutor` class
3. Add case to `execute()` method

### Want to use a real LLM?

Set your API key:

```bash
export OPENAI_API_KEY="sk-..."
````

Then edit `src/agent.py` to use the OpenAI client instead of heuristics.

## Troubleshooting

**"No module named src"**

- Make sure you're running from project root: `cd agent-assignment`
- Virtual environment is activated: `source .venv/bin/activate`

**"Command not found: uv"**

- Install uv: `pip install uv`

**Agent not responding as expected**

- Check `src/agent.py` for the heuristics
- Try with more specific input (include dates, times, etc.)

## Getting Help

- Look at the code comments - every function is documented
- Check `README.md` for detailed project info
- Check `ARCHITECTURE.md` for design explanations
- Read the docstrings: `help(Agent)` in Python REPL

---

**Ready to go?** Run `python main.py` and start testing!
