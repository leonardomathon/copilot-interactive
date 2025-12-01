# Copilot Interactive

A FastAPI application that enables interactive Copilot sessions by allowing Copilot to request user input within a single token session.

## Overview

GitHub Copilot charges 1 "agent token" per request, regardless of how long the request is. Normally, if Copilot needs more information, it would need to make another request, costing another token.

This application creates a local endpoint that Copilot can call to request user input. The script waits for the user's response, and Copilot receives the response within the same token session. This effectively creates an interactive loop inside a single Copilot agent request.

## Usage

You need to let your Github Copilot agent know to use this local endpoint to request user input. You can do this by either configuring an `AGENTS.MD` file in your repository or by modifying the system prompt to include instructions for using the local endpoint. You can use the following example system prompt:

````
You are an Interactive Agent that follows it's main system prompt. You can ask clarifying questions within the same request to gather more information before providing a final answer or solution. To do this, you will use the terminal command `curl` to make a POST request to the local endpoint `http://localhost:4000/user-input` with a plain text body containing your question or request for information.

At the end, when you are done outputting always ask the user if they need anything else via the same endpoint. That way we can keep the conversation going without having to start a new request.

## Interactive User Input

When you need clarification, confirmation, or additional information from the user during a task, you can request input directly without ending your current session. This allows for an interactive conversation loop within a single request.

### Why Use This

Instead of making assumptions or stopping to ask for another request, you can pause and wait for user input. This is useful when you:
- Need clarification on ambiguous requirements
- Want confirmation before making destructive or irreversible changes
- Require additional context or data the user hasn't provided
- Need the user to choose between multiple options

### How to Request User Input

Make a POST request to the local endpoint:

**Endpoint:** `POST http://localhost:4000/user-input`
**Content-Type:** `text/plain`
**Body:** A clear description of what input you need from the user

**Example using curl:**
```bash
curl -X POST -H "Content-Type: text/plain" \
  -d 'I found 3 database migration files. Which should I run: (1) all of them, (2) only the latest, or (3) none?' \
  http://localhost:4000/user-input

````

## Installation

### Using Poetry

```bash
cd copilot-interactive
poetry install
```

### Using pip

```bash
pip install -e ".[dev]"
```

## Configuration

Copy `.env.example` to `.env` and customize as needed:

```bash
cp .env.example .env
```

### Environment Variables

| Variable                          | Description                        | Default           |
| --------------------------------- | ---------------------------------- | ----------------- |
| `APP_PORT`                        | Port to run the server on          | `4000`            |
| `APP_HOST`                        | Host to bind to                    | `0.0.0.0`         |
| `INPUT_TIMEOUT`                   | Timeout for user input in seconds  | `540` (9 minutes) |
| `ASSISTANT_HOST`                  | Host of the local AI assistant     | `localhost`       |
| `ASSISTANT_PORT`                  | Port of the local AI assistant     | `4141`            |
| `ASSISTANT_TIMEOUT`               | Timeout for assistant requests     | `10`              |
| `ASSISTANT_MODEL`                 | Model name for the assistant       | `gpt-5-mini`      |
| `NOTIFICATION_ENABLED`            | Enable system notifications        | `true`            |
| `NOTIFICATION_MAX_CONTENT_LENGTH` | Max length of notification content | `200`             |

## Usage

### Running the Server

```bash
# Using the installed command
copilot-interactive

# Or using Python
python -m copilot_interactive.main

# Or using uvicorn directly
uvicorn copilot_interactive.main:app --host 0.0.0.0 --port 4000
```

### API Endpoints

#### POST /user-input

Request user input with plain text body:

```bash
curl -X POST -H "Content-Type: text/plain" \
  -d 'Confirm deployment target and version; awaiting user input' \
  http://localhost:4000/user-input
```

#### POST /user-input/json

Request user input with JSON body:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"context": "Confirm deployment target and version"}' \
  http://localhost:4000/user-input/json
```

#### GET /health

Health check endpoint:

```bash
curl http://localhost:4000/health
```

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_utils.py

# Run with verbose output
pytest -v
```

### Type Checking

```bash
mypy src/copilot_interactive
```

### Linting and Formatting

```bash
# Check for issues
ruff check src tests

# Auto-fix issues
ruff check --fix src tests

# Format code
ruff format src tests
```
