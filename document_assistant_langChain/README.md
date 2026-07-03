# Document-Based Financial Assistant

This project is a conversational agent built with LangChain and LangGraph to answer questions about financial and administrative documents, summarize content, and perform calculations based on retrieved data.

The project works with a set of simulated in-memory documents, including invoices, contracts, and claims, and exposes a simple CLI interface through `main.py`.

## Getting Started

These instructions describe how to run the project locally in a development environment.

### Dependencies

```text
Python 3.9+
langchain>=0.2.0
langgraph>=0.6.7
langchain-openai>=0.1.0
langchain-core>=0.2.0
pydantic>=2.0.0
python-dotenv>=1.0.0
openai>=1.0.0
print-color>=0.4.6
```

### Installation

1. Create a virtual environment.
2. Activate the environment.
3. Install the project dependencies.
4. Create a `.env` file with your `OPENAI_API_KEY`.
5. Start the CLI application.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
echo OPENAI_API_KEY=your_key_here > .env
python main.py
```

## Overview

The agent's main flow is:

`classify_intent -> qa | summarization | calculation -> update_memory -> END`

The core modules are in `src/`:

- `assistant.py`: initializes the LLM, retriever, tools, workflow, and session.
- `agent.py`: defines the LangGraph state and workflow nodes.
- `retrieval.py`: loads sample documents and handles retrieval by keyword, type, and value range.
- `tools.py`: exposes the agent tools, including search, reading, statistics, and calculator.
- `schemas.py`: Pydantic contracts used for intents, responses, and memory.
- `prompts.py`: prompts for classification, Q&A, summarization, calculation, and memory summary.


## Implementation Decisions


- Retrieval is intentionally simple: `SimulatedRetriever` keeps documents in memory and matches by keyword, type, and values. This reduces dependencies and makes the behavior predictable for study and demonstration.
- Agent operations go through tools (`@tool`) instead of embedding everything in the prompt. This is especially important for document reading and calculations.
- The calculation agent is instructed to use the calculator tool for any math operation, avoiding "mental" calculations by the model.

## State and Memory

The workflow shared state is defined in `AgentState` and includes, among other fields:

- `user_input`: current user message.
- `messages`: message history used by LangGraph.
- `intent`: classified intent for the current turn.
- `next_step`: next node to execute.
- `conversation_summary`: short summary of the conversation so far.
- `active_documents`: IDs of the documents currently in focus.
- `tools_used`: tools triggered during the turn.
- `actions_taken`: trace of the executed nodes.

There are two memory layers in the project:

1. Workflow memory: the graph is compiled with `InMemorySaver`, so the state is associated with the session `thread_id` and can be recovered across invocations.
2. Session persistence: `DocumentAssistant` saves a `SessionState` as JSON in `./sessions`, storing history, document context, and timestamps.

In practice, memory works like this:

- `process_message()` builds the initial state with `session_id`, previous history, and active documents.
- The `update_memory` node generates a short conversation summary and updates `active_documents`.
- At the end of the turn, the current session is saved to disk.

This enables follow-ups such as "summarize that contract" followed by "what is its total value?", reusing context already established in the conversation.

## How Structured Outputs Are Enforced

The project uses Pydantic to enforce the format of the most important responses.

Models defined in `schemas.py`:

- `UserIntent`: classifies the request as `qa`, `summarization`, `calculation`, or `unknown`.
- `AnswerResponse`: question-answer response with sources and confidence.
- `SummarizationResponse`: summary with key points and related documents.
- `CalculationResponse`: expression, result, and explanation.
- `UpdateMemoryResponse`: conversation summary and active documents.

This structure is applied in two ways:

- `llm.with_structured_output(...)` is used for intent classification and memory update.
- `create_react_agent(..., response_format=...)` is used in the Q&A, summarization, and calculation agents to request a response that matches the expected schema.

This reduces manual parsing, improves field validation, and makes integration between workflow nodes more reliable.

## Available Tools

- `document_search`: searches documents by keyword, type, or monetary criteria.
- `document_reader`: reads the full content of a document by ID.
- `document_statistics`: returns general statistics about the collection.
- `calculator_tool`: evaluates simple mathematical expressions with basic regex validation.

## Sample Documents

The retriever loads some simulated in-memory documents, for example:

- `INV-001`: invoice for Acme Corporation.
- `CON-001`: service contract with a total value of `$180,000`.
- `CLM-001`: insurance claim for `$2,450`.
- `INV-002` and `INV-003`: invoices with higher totals, useful for value-range queries.

## Example Conversations

### 1. Question answering with source

```text
User: What is the total value of contract CON-001?
Assistant: The total value of contract CON-001 is $180,000.
Sources: ['CON-001']
Confidence: 0.95
```

### 2. Document summarization

```text
User: Summarize contract CON-001.
Assistant: The contract establishes platform access, 24/7 support, monthly reports, and compliance monitoring. The term is 12 months and the monthly fee is $15,000.
Key points: [...]
Documents summarized: ['CON-001']
```

### 3. Document-based calculation

```text
User: What is the subtotal plus tax for invoice INV-001?
Assistant: Invoice INV-001 shows a subtotal of $20,000 and tax of $2,000. The calculation performed was 20000 + 2000 = 22000.
```

### 4. Value range search

```text
User: Which documents have values above $50,000?
Assistant: CON-001, INV-002, and INV-003 were found, along with their values and preview excerpts.
```

### 5. Memory-based follow-up

```text
User: Summarize contract CON-001.
Assistant: [contract summary]

User: And what is its duration?
Assistant: The contract duration is 12 months.
```

In this last case, the agent reuses conversation context and the active document to answer the follow-up without requiring the user to repeat the full request.

## Testing

The repository does not currently include a formal automated test suite. The closest existing validation artifact is [src/teste.py](src/teste.py), which manually exercises the calculator behavior.

### Break Down Tests

The current manual check in [src/teste.py](src/teste.py) validates that:

- arithmetic expressions matching the allowed regex are evaluated correctly
- invalid expressions can be rejected before evaluation
- the calculator returns a formatted string with the computed result

Example:

```bash
python src/teste.py
```

## Project Instructions

This project asks the student to build a document assistant that:

- routes user requests by intent
- uses tools to retrieve and read documents
- enforces structured outputs with Pydantic schemas
- maintains state and memory across turns
- demonstrates the implemented features through example conversations

Those deliverables are documented in the sections above, especially `Implementation Decisions`, `State and Memory`, `How Structured Outputs Are Enforced`, and `Example Conversations`.

## Built With

- [LangChain](https://www.langchain.com/) - LLM application framework used for prompts, tools, and agent integration.
- [LangGraph](https://www.langchain.com/langgraph) - Workflow orchestration layer used to model the multi-step agent state machine.
- [Pydantic](https://docs.pydantic.dev/) - Data validation library used to enforce structured outputs.
- [OpenAI Python SDK](https://github.com/openai/openai-python) - Client library used through the configured chat model integration.

## License

No license file is currently included in this repository.