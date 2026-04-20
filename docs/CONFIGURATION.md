# Configuration Guide

## Table of Contents
- [Environment Variables](#environment-variables)
- [FastAPI Configuration](#fastapi-configuration)
- [Agent Configuration](#agent-configuration)
- [Database Configuration](#database-configuration)
- [Logging Configuration](#logging-configuration)
- [Security Configuration](#security-configuration)

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

### Required Variables

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-api-key-here
```

**How to get API Key**:
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create account
3. Go to **Settings → API Keys**
4. Click **Create new secret key**
5. Copy and paste into `.env`

### Optional Variables

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true
LOG_LEVEL=INFO

# Model Configuration
MODEL_NAME=gpt-4o
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=2000

# Database Configuration
DATABASE_URL=sqlite:///./all-utils/db/chroma.sqlite3
CHROMA_COLLECTION_NAME=interviews

# Interview Configuration
DEFAULT_INTERVIEW_DURATION_MINUTES=30
DEFAULT_NUM_QUESTIONS=5
INTERVIEW_DIFFICULTY=medium

# Logging
LOG_FILE=logs/app.log
LOG_FORMAT=json
```

### ⚠️ Security Best Practices

1. **Never commit `.env` to version control**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables in production**
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. **Rotate API keys regularly**

4. **Use separate keys for development and production**

5. **Monitor API usage**
   - Go to [Usage Dashboard](https://platform.openai.com/account/usage/overview)
   - Set spending limits

---

## FastAPI Configuration

### Server Settings

Start the server with custom configuration:

```bash
# Default (development)
uvicorn app:app --reload

# Production
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# Specific port
uvicorn app:app --port 8001

# Custom host
uvicorn app:app --host 192.168.1.100 --port 8000

# Debugging
uvicorn app:app --reload --log-level debug
```

### Configuration in Code

Modify `app.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Interview Evaluation System",
    description="Automated candidate interview evaluation",
    version="1.0.0",
    debug=False  # Set to False in production
)

# Add CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Static Files Configuration

```python
from fastapi.staticfiles import StaticFiles

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
```

### Template Configuration

```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
```

---

## Agent Configuration

### OpenAI Client Configuration

```python
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",  # Available: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,  # 0.0 (deterministic) to 1.0 (creative)
    max_tokens=2000,
    timeout=30,
)
```

### Agent Configuration Parameters

```python
interviewer_config = {
    "name": "Interviewer",
    "system_prompt": """You are an expert technical interviewer...""",
    "max_messages": 50,
    "temperature": 0.7,
}

evaluator_config = {
    "name": "Evaluator",
    "system_prompt": """You are an expert evaluator...""",
    "max_messages": 50,
    "temperature": 0.5,  # Lower temperature for consistency
}

candidate_config = {
    "name": "Candidate",
    "system_prompt": """You are a job candidate...""",
    "human_input_mode": "ALWAYS",  # Use WebSocket for input
}
```

### Team Configuration

```python
from autogen_agentchat.teams import RoundRobinGroupChat

team = RoundRobinGroupChat(
    participants=[interviewer, evaluator, candidate],
    max_turns=10,  # Maximum conversation turns
    messages=[],
)
```

### Temperature Settings Explanation

| Temperature | Behavior | Use Case |
|-------------|----------|----------|
| 0.0 | Deterministic, focused | Evaluations, factual responses |
| 0.3 | Mostly consistent | Guidelines, structured tasks |
| 0.5 | Balanced | General conversations |
| 0.7 | Creative, varied | Interview questions |
| 1.0 | Very creative, random | Creative tasks |

---

## Database Configuration

### Chroma Vector Database

Location: `all-utils/db/chroma.sqlite3`

```python
import chromadb

# Local SQLite database
client = chromadb.Client(
    settings=chromadb.Settings(
        chroma_db_impl="duckdb",
        persist_directory="./all-utils/db",
        anonymized_telemetry=False,
    )
)

# Get or create collection
collection = client.get_or_create_collection(name="interviews")
```

### Data Persistence

```python
# Add data
collection.add(
    ids=["id1", "id2"],
    embeddings=[[1.2, 2.3], [4.5, 6.9]],
    metadatas=[{"name": "Alice"}, {"name": "Bob"}],
    documents=["Interview transcript 1", "Interview transcript 2"]
)

# Query
results = collection.query(
    query_embeddings=[[1.2, 2.3]],
    n_results=10
)
```

### Backup Configuration

```bash
# Backup database
cp -r all-utils/db all-utils/db.backup

# Restore from backup
cp -r all-utils/db.backup all-utils/db
```

---

## Logging Configuration

### Logging Setup

```python
import logging
from logging.handlers import RotatingFileHandler

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler
handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10485760,  # 10MB
    backupCount=5
)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### Log Levels

| Level | Severity | Usage |
|-------|----------|-------|
| DEBUG | Low | Detailed debugging info |
| INFO | Low | General informational messages |
| WARNING | Medium | Warning messages |
| ERROR | High | Error messages |
| CRITICAL | Critical | Critical errors |

### Logging in Application

```python
logger.debug("Debug message")
logger.info("Interview started")
logger.warning("API rate limit approaching")
logger.error("Failed to evaluate response")
logger.critical("Database connection failed")
```

### Uvicorn Logging

```bash
# Different log levels
uvicorn app:app --log-level debug      # Detailed
uvicorn app:app --log-level info       # Standard
uvicorn app:app --log-level warning    # Important only
```

---

## Security Configuration

### API Key Security

✅ **Good Practices**:
```python
# Load from environment
api_key = os.getenv("OPENAI_API_KEY")

# Never hardcode
# api_key = "sk-..."  # ❌ DON'T DO THIS
```

### WebSocket Security

```python
@app.websocket("/ws/{interview_id}")
async def interview_websocket(websocket: WebSocket, interview_id: str):
    # Validate session/token
    token = websocket.query_params.get("token")
    if not validate_token(token):
        await websocket.close(code=1008, reason="Unauthorized")
        return
    
    await websocket.accept()
    # Handle connection
```

### CORS Configuration for Production

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://app.yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age=600,
)
```

### HTTPS Configuration

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with HTTPS
uvicorn app:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

### Input Validation

Always validate input:

```python
from pydantic import BaseModel, Field, validator

class InterviewRequest(BaseModel):
    job_position: str = Field(..., min_length=1, max_length=100)
    candidate_name: str = Field(..., min_length=1, max_length=200)
    
    @validator('job_position')
    def job_position_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Job position cannot be empty')
        return v
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/interview/{interview_id}")
@limiter.limit("100/minute")
async def get_interview(interview_id: str):
    # Implementation
```

---

## Performance Tuning

### Uvicorn Workers

```bash
# Multiple workers (production)
uvicorn app:app --workers 4

# More workers = higher throughput
# Recommended: number of CPU cores
```

### Model Optimization

```python
# Faster model (less capable but cheaper)
model="gpt-3.5-turbo"

# More capable but slower/expensive
model="gpt-4o"
```

### Database Optimization

```python
# Add indexes to Chroma
collection.create_index()

# Query optimization
results = collection.query(
    query_embeddings=embeddings,
    n_results=5,  # Limit results
    where={"score": {"$gte": 0.7}}  # Filter
)
```

---

## Environment-Specific Configuration

### Development
```bash
OPENAI_API_KEY=sk-...
LOG_LEVEL=DEBUG
RELOAD=true
```

### Staging
```bash
OPENAI_API_KEY=sk-...
LOG_LEVEL=INFO
RELOAD=false
WORKERS=2
```

### Production
```bash
OPENAI_API_KEY=sk-...
LOG_LEVEL=WARNING
RELOAD=false
WORKERS=4
SSL_CERTFILE=/path/to/cert.pem
SSL_KEYFILE=/path/to/key.pem
```

---

## Troubleshooting Configuration

### Issue: "API key not found"
```bash
# Check .env exists
cat .env

# Check environment variable
echo $OPENAI_API_KEY
```

### Issue: "Port already in use"
```bash
# Use different port
uvicorn app:app --port 8001

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000    # Windows
```

### Issue: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Clear cache
pip cache purge
pip install -r requirements.txt
```

