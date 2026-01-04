# LangChain Text Analyzer

A FastAPI-based text analysis service that uses Google's Gemini AI to classify and analyze user messages. The service identifies topics, detects language, analyzes sentiment, and generates contextual responses.

## Features

- **Topic Classification**: Categorizes messages into predefined topics (Flight Information, General Information, Prompt Injection, RAG Agent, Comparison Agent, Chit-chat)
- **Language Detection**: Identifies the language of the input text
- **Sentiment Analysis**: Classifies sentiment as Angry, Happy, or Neutral
- **AI Response Generation**: Provides contextual responses in the same language as the input
- **Database Logging**: Stores all analyzed messages with their metadata in SQLite
- **Migration Support**: Uses Alembic for database schema management

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **LangChain**: Framework for developing applications with LLMs
- **Google Gemini 2.5 Flash**: AI model for text analysis
- **SQLModel**: SQL database interaction with Pydantic models
- **Alembic**: Database migration tool
- **Uvicorn**: ASGI server
- **Docker**: Containerization support

## Project Structure

```
langchain-text-analyzer/
├── app/
│   ├── alembic/              # Database migrations
│   ├── core/                 # Configuration and dependencies
│   │   ├── config.py         # Environment configuration
│   │   └── dependencies.py   # Dependency injection
│   ├── db/                   # Database setup
│   │   └── database.py       # Database engine and session
│   ├── infra/                # Infrastructure layer
│   │   └── ai_providers.py   # Gemini client implementation
│   ├── interfaces/           # Abstract interfaces
│   │   └── ai_client.py      # AI client interface
│   ├── models/               # Database models
│   │   └── ai.py             # MessageLog model
│   ├── routers/              # API routes
│   │   └── ai.py             # Analysis endpoint
│   ├── runner/               # Application setup
│   │   ├── asgi.py           # ASGI entry point
│   │   └── setup.py          # FastAPI app configuration
│   ├── schemas/              # Pydantic schemas
│   │   └── schemas.py        # Request/response models
│   └── services/             # Business logic
│       ├── chat_service.py   # Main service logic
│       └── prompts.py        # AI prompts
├── .env.example              # Environment variables example
├── alembic.ini               # Alembic configuration
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image configuration
├── pyproject.toml            # Project dependencies
└── uv.lock                   # Dependency lock file
```

## Prerequisites

- Python 3.13+
- Google API Key for Gemini
- UV package manager (for local setup)
- Docker and Docker Compose (for Docker setup)

## Installation and Running

### Option 1: Docker (Recommended)

This is the easiest way to get started. Docker will handle all dependencies and setup automatically.

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd langchain-text-analyzer
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   DB_NAME=database
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   The API will be available at `http://localhost:8000`

4. **Stop the application**
   ```bash
   docker-compose down
   ```

**Note**: With Docker, database migrations run automatically on startup, and the database file is persisted in your project directory.

---

### Option 2: Local Setup

For development or if you prefer running without Docker.

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd langchain-text-analyzer
   ```

2. **Install UV package manager** (if not already installed)
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   DB_NAME=database
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn app.runner.asgi:app --reload
   ```

   The API will be available at `http://localhost:8000`

---

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Analyze Message

**POST** `/analyze`

Analyzes a user message and returns topic, language, sentiment, and AI response.

**Request Body:**
```json
{
  "message": "Hello! How are you today?"
}
```

**Response:**
```json
{
  "status": "success",
  "response": "I'm doing well, thank you for asking! How can I help you today?"
}
```

## Usage Examples

### Using cURL

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather like?"}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={"message": "როგორ ხარ?"}  # Georgian: "How are you?"
)

print(response.json())
```

### Using JavaScript/Fetch

```javascript
fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Hello! How are you?'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```


### Project Architecture

The project follows clean architecture principles:

1. **Routers**: Handle HTTP requests and responses
2. **Services**: Contain business logic
3. **Infrastructure**: Implement external service integrations
4. **Models**: Define database schemas
5. **Schemas**: Define API request/response structures
6. **Interfaces**: Define abstract contracts

## Configuration

### Supported Topic Categories

- Flight Information
- General Information (Date, weather, etc.)
- Prompt Injection (Malicious attempts)
- RAG Agent (Questions about scraped site content)
- Comparison Agent (Comparing two things)
- Chit-chat (Casual conversation)

### Sentiment Categories

- Angry
- Happy
- Neutral

### AI Model Settings

The Gemini client is configured with:
- Model: `gemini-2.5-flash`
- Temperature: `0.3`
- Uses Vertex AI integration

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | - | Yes |
| `DB_NAME` | Database name | `database` | No |
| `DB_URL` | Full database URL | `sqlite:///{DB_NAME}.db` | No |

## Troubleshooting

### Docker Issues

- **Port already in use**: Change the port mapping in `docker-compose.yml`
- **Permission denied**: Make sure Docker daemon is running and you have proper permissions

### Local Setup Issues

- **Module not found**: Make sure you ran `uv sync` to install dependencies
- **Database errors**: Run `alembic upgrade head` to ensure migrations are applied
- **API key errors**: Verify your `.env` file contains a valid `GOOGLE_API_KEY`
