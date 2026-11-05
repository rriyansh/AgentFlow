# AgentFlow: State-Driven Multi-Agent System

## System Overview
AgentFlow is an asynchronous orchestration framework designed to handle complex, cyclical multi-step tasks. Unlike linear LLM chains (which fail gracefully on complex logic), AgentFlow utilizes a graph-based state machine to manage multi-agent interactions, conditional routing, and error recovery.

## Architecture
- **State Graph:** Built on LangGraph, the system defines nodes as specialized agents (e.g., Code Generator, Code Reviewer, Executor) and edges as conditional logic flows.
- **Role Isolation:** Each agent operates with a strictly scoped system prompt and a specific subset of tools (e.g., the Executor has access to a sandboxed Python REPL, while the Researcher has search API access).
- **State Persistence:** Execution states are checkpointed to a SQLite/Redis backend after every node transition. This enables time-travel debugging, human-in-the-loop approvals, and workflow resumption after failures.

## Engineering Challenges Addressed
- **Infinite Recursion Prevention:** Multi-agent systems are prone to infinite loops when agents disagree. Implemented strict state validation barriers and a maximum iteration depth counter to force a hard exit or human escalation.
- **Context Window Management:** As the graph executes, the message history grows rapidly. Implemented an automatic summarization node that compresses older execution logs before passing the state to the next agent, preventing token limit exhaustion.

## Tech Stack
- **Orchestration:** LangGraph, LangChain
- **LLMs:** Anthropic Claude 3.5 Sonnet, GPT-4o
- **State Management:** Redis (Production), SQLite (Local)
