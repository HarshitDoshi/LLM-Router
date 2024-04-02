# LLM Router

## Overview

The LLM Router API is a FastAPI application designed to route chat messages to different Language Learning Models (LLMs) like OpenAI's GPT-3, Anthropic's Claude, and Cohere's language model. It supports both synchronous and streaming responses, allowing for real-time interaction with the models. This document provides a comprehensive guide to the API's structure, usage, and deployment.

The LLM Router API provides a flexible and easy-to-use interface for interacting with multiple LLM providers. It abstracts away the specifics of each provider's API, allowing clients to send chat messages to different LLMs using a unified interface. With support for both synchronous and streaming responses, it caters to a wide range of use cases.

## Project Structure

The project is structured into several Python modules, each serving a distinct purpose in the application:

- `app.py`: The main FastAPI application module. It defines the API endpoint and handles the routing of chat messages to the appropriate LLM based on the provided model name.
- `factory.py`: Contains the ChatModelFactory class that is responsible for instantiating the correct chat model class based on the provided model name.
- `common.py`: Defines an abstract base class ChatModel that outlines the interface for chat models. Each chat model must implement this interface. Chat model modules (`openai_chat_model.py`, `anthropic_chat_model.py`, `cohere_chat_model.py`): These modules contain the implementation of the chat models for different LLM providers. They handle the specifics of sending messages to their respective APIs and processing the responses.

## Key Components

### FastAPI Application (`app.py`)
The FastAPI application defines a single `POST` endpoint `/chat/` that accepts a JSON payload with the following fields:
    - `message`: The chat message to be sent to the LLM.
    - `chat_model_name`: The name of the LLM to route the message to (openai, anthropic, or cohere).
    - `stream`: A boolean indicating whether the response should be streamed. Depending on the value of the stream field, the endpoint either returns a single JSON response or streams the response back to the client in chunks.

### Chat Model Factory (`factory.py`)
The `ChatModelFactory` class provides a static method create that takes the name of a chat model and returns an instance of the corresponding class. This allows for easy addition of new chat models to the application.

### Chat Model Interface (`common.py`)
The `ChatModel` abstract base class defines two abstract methods that all chat model classes must implement:
    - `__init__`: Initializes the chat model, typically setting up the API client.
    - `send_message`: Sends a message to the LLM and returns the response. For models that support streaming, this method should return an asynchronous generator.

### Chat Model Implementations
Each chat model module implements the `ChatModel` interface for a specific LLM provider. They are responsible for constructing the API requests, handling the responses, and optionally supporting streaming responses.

## Usage

To use the LLM Router API, send a `POST` request to the `/chat/` endpoint with a JSON payload containing the `message`, `chat_model_name`, and optionally, the `stream` field. The API will route the message to the specified LLM and return the response.

Example payload

```json
{
  "message": "Hello, world!",
  "chat_model_name": "openai",
  "stream": false
}
```

## Deployment

The LLM Router API can be deployed as a standard FastAPI application. Ensure that the required environment variables are set (API keys for the LLM providers) and use a WSGI server like Uvicorn or Gunicorn to serve the application.

To deploy it locally, issue the following command:

```sh
python -m poetry run uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Use the following command to start a Docker instance of the LLM Router APIs:

```sh
docker compose --project-name "llm-router" -f docker-compose.yml up --detach --build
```

## Environment Configuration

The application requires API keys for the LLM providers to be set in the environment. This can be done using a `.env` file with the following contents:

```
OPENAI_API_KEY='<your_openai_api_key>'
ANTHROPIC_API_KEY='<your_anthropic_api_key>'
COHERE_API_KEY='<your_cohere_api_key>'
```

Ensure that the .env file is loaded before starting the application.
