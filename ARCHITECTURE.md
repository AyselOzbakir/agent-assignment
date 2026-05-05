# Architecture Guide for AI Agent Assignment

This document explains the design decisions and architecture of the agent assignment to help you understand and extend it.

## Core Components

### 1. Data Models (`src/models.py`)

All data flows through strongly-typed Pydantic models:

- **Intent**: Enum classifying user intent (BOOKING, SCHEDULING, SEARCH, REMINDER, UNKNOWN)
- **ToolName**: Available tools
- **UserRequest**: Input with timestamp
- **AgentState**: Mutable state during processing
- **AgentResponse**: Immutable final output
- **ToolCall**: Plan for tool execution
- **ToolResult**: Tool execution outcome

**Why?** Type safety, clarity, and easy serialization for logging/debugging.

### 2. Tool Executor (`src/tools.py`)

Handles all external tool interactions. Currently mock implementations.

**Key points:**

- Each tool returns `ToolResult` (not exceptions) for graceful error handling
- Mock data is stored as instance variables for consistency
- Easy to replace with real API calls - just modify method bodies
- Tool executor is stateless (can be parallelized if needed)

**To add a new tool:**

1. Add to `ToolName` enum
2. Add method to `ToolExecutor`
3. Add case to `execute()` dispatcher

### 3. Memory System (`src/memory.py`)

Tracks conversation context for multi-turn interactions.

**Stores:**

- Conversation history (user/assistant messages)
- Tool results for reference
- Agent states for analysis
- Provides formatted context for LLM calls

**Design:** Simple chronological tracking. Could be enhanced with:

- Semantic similarity search
- Importance weighting
- Persistent storage (DB/file)

### 4. Agent Orchestration (`src/agent.py`)

Main agent class coordinating the workflow.

**Workflow:**

```
process_request(user_input)
  ├─ Classify intent
  ├─ Generate clarifying questions (if needed → return early)
  ├─ Break into subtasks
  ├─ Plan tool calls based on subtasks
  ├─ Execute tools (handle failures gracefully)
  └─ Generate summary
```

**Key methods:**

- `_classify_intent()` - Keyword-based (replace with LLM)
- `_generate_clarifying_questions()` - Heuristic-based
- `_break_down_tasks()` - Template-based for different intents
- `_plan_tool_calls()` - Heuristic-based tool selection
- `_generate_summary()` - Formats results for display

**Design philosophy:**

- Each method is self-contained and testable
- Graceful degradation (errors don't stop the agent)
- Clear separation between analysis and execution

### 5. Prompts (`src/prompts.py`)

Prompt templates for LLM integration.

**Current use:** Documentation only
**Future use:** Pass to OpenAI API for sophisticated reasoning

Each prompt includes:

- Clear system context
- Input variables in `{braces}`
- Expected output format
- Examples

### 6. Interactive CLI (`main.py`)

User-facing interface with rich formatting.

**Features:**

- Welcome screen with examples
- Formatted responses (intent, actions, findings, blockers)
- Built-in commands (help, memory, clear)
- Error handling and graceful interruption

## Design Patterns

### Pattern 1: Result Objects Instead of Exceptions

```python
# Instead of:
try:
    calendar.check(date)
except CalendarError as e:
    # Handle error

# Do this:
result = ToolExecutor.execute(CALENDAR_CHECK, params)
if result.success:
    process(result.data)
else:
    handle_error(result.error)
```

**Benefit:** Error handling is explicit and the agent can continue on failures.

### Pattern 2: State Objects for Decision Making

```python
state = AgentState(request=request)
state.intent = self._classify_intent(...)
state.subtasks = self._break_down_tasks(...)
state.tool_results = [...]
```

**Benefit:** Clear audit trail, easy debugging, simple to extend with new fields.

### Pattern 3: Heuristic → LLM Progression

The code starts simple (heuristics) and is designed for easy LLM replacement:

```python
# Current: Keyword-based
def _classify_intent(self, text):
    if "book" in text.lower():
        return Intent.BOOKING

# Future: LLM-based
def _classify_intent(self, text):
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": Prompts.intent_classifier().format(request=text)
        }]
    )
    return Intent[response.content]
```

## Extension Points

### Easy Extensions

1. **Add tools** - New methods in `ToolExecutor`
2. **Add intents** - New enum values, task templates
3. **Improve clarification** - Better heuristics in `_generate_clarifying_questions()`
4. **Better formatting** - Rich library features in main.py

### Medium Extensions

1. **LLM integration** - Replace heuristic methods with LLM calls
2. **Persistent memory** - Add SQLite/PostgreSQL backing
3. **Multi-turn refinement** - Track clarifications and refine plans
4. **Tool result interpretation** - Parse tool results for context

### Complex Extensions

1. **Tool composition** - Execute tools in parallel/sequence
2. **Reasoning loops** - Iterate on tool results
3. **Failure recovery** - Try alternate tools on failure
4. **Learning** - Log successes/failures for improvement

## Testing Strategy

### Unit Test Ideas

```python
# Test intent classification
assert agent._classify_intent("book a table") == Intent.BOOKING

# Test task breakdown
tasks = agent._break_down_tasks("...", Intent.BOOKING)
assert len(tasks) > 0

# Test tool execution
result = executor.execute(CALENDAR_CHECK, {"date_range": "tomorrow"})
assert result.success
```

### Integration Test Ideas

```python
# End-to-end workflow
response = agent.process_request("Book a restaurant tomorrow at 7pm for 2")
assert response.intent == Intent.BOOKING
assert len(response.actions_taken) > 0
assert response.success
```

### Manual Testing

See the example requests in README.md.

## Performance Considerations

**Current:** Everything is synchronous and sequential

- Tool calls execute one at a time
- No optimization needed for small requests

**Scalability improvements:**

1. Parallel tool execution (tools are independent)
2. Streaming responses (start summary while tools run)
3. Caching tool results (Redis for calendar data)
4. LLM response caching (semantic cache for similar requests)

## Security Considerations

**Current implementation is for learning only.** For production:

1. **Input validation** - Sanitize user inputs
2. **API key management** - Use secrets manager, not .env files
3. **Tool access control** - Don't let users book arbitrary items
4. **Audit logging** - Log all tool calls and results
5. **Rate limiting** - Prevent abuse of tools

## Common Debugging

### Issue: Wrong intent classified

```python
# Debug:
intent = agent._classify_intent(user_input)
print(f"Classified as: {intent}")

# Solution: Update keywords in _classify_intent()
# Long-term: Switch to LLM-based classification
```

### Issue: Tool not called

```python
# Debug:
tool_calls = agent._plan_tool_calls(user_input, subtasks)
print(f"Planned tools: {[str(t) for t in tool_calls]}")

# Solution: Update heuristics in _plan_tool_calls()
# Or improve subtask breakdown
```

### Issue: Memory growing too large

```python
# Solution: Implement memory truncation
if len(self.memory.conversation_history) > 100:
    self.memory.conversation_history = self.memory.conversation_history[-50:]
```

## Next Steps for Enhancement

**Priority 1 (Quick wins):**

- Add unit tests
- Improve clarifying questions logic
- Add more example intents

**Priority 2 (Core improvements):**

- Integrate OpenAI API for intent classification
- Add tool composition (execute tools in sequence)
- Implement memory persistence

**Priority 3 (Production readiness):**

- Add comprehensive logging
- Implement error recovery strategies
- Add rate limiting and security checks
- Build monitoring and alerting

## References

- **Pydantic:** Data validation and serialization
- **Rich:** Terminal formatting and user experience
- **OpenAI API:** For future LLM integration
- **Design patterns:** Result objects, state machines
