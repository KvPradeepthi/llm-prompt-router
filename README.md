# LLM-Powered Prompt Router for Intent Classification

An intelligent service that routes user requests to specialized AI personas based on intent classification. This project implements a sophisticated prompt routing pattern used in production AI systems.

## Overview

This application uses a two-step process:
1. **Classify Intent**: Lightweight LLM call classifies user intent and confidence score
2. **Route & Respond**: Routes to specialized persona prompts for context-aware responses

## Features

- **Intent Classification**: Classifies user messages into: code, data, writing, career, or unclear
- **Specialized Personas**: At least 4 distinct expert system prompts for different domains
- **JSON Logging**: All routing decisions logged to `route_log.jsonl`
- **Error Handling**: Graceful handling of malformed LLM responses
- **Structured Output**: JSON schema validation for LLM responses

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key"
```

2. Run the service:
```bash
python prompt_router.py
```

## Core Components

### `classify_intent(message: str) -> dict`
- Takes user message and classifies intent
- Returns: `{"intent": "string", "confidence": float}`
- Handles malformed JSON by defaulting to unclear

### `route_and_respond(message: str, intent: dict) -> str`
- Routes to appropriate persona based on intent
- Generates context-aware response
- Returns final response as string

### System Prompts

- **Code Expert**: Production-quality code with error handling
- **Data Analyst**: Statistical patterns and visualizations
- **Writing Coach**: Text improvement feedback (no rewrites)
- **Career Advisor**: Concrete, actionable career advice

## Logging

All requests are logged to `route_log.jsonl` with:
- `timestamp`: ISO 8601 timestamp
- `user_message`: Original user input
- `intent`: Classified intent label
- `confidence`: Confidence score (0.0-1.0)
- `final_response`: Generated response

## Requirements

- Python 3.8+
- openai>=1.0.0
- python-dotenv>=0.19.0

## Example Usage

```python
from prompt_router import process_message

response = process_message("How do I sort a list in Python?")
print(response)  # Get expert code assistance
```
