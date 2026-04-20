# Development Guide

## Table of Contents
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Debugging](#debugging)
- [Contributing](#contributing)
- [Common Tasks](#common-tasks)

---

## Development Setup

### Prerequisites
- Python 3.12+
- Git
- Code editor (VS Code recommended)
- OpenAI API key

### Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd Automated-Candidate-Interview-Evaluation-System

# 2. Create virtual environment (UV recommended)
uv venv dev_env
source dev_env/bin/activate  # or: dev_env\Scripts\activate on Windows

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env  # If exists
# OR
echo 'OPENAI_API_KEY=sk-your-key' > .env

# 5. Run development server
uvicorn app:app --reload --log-level debug
```

### VS Code Setup

#### Recommended Extensions
```json
{
  "extensions": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.debugpy",
    "charliermarsh.ruff",
    "ms-vscode.makefile-tools",
    "ms-vscode-remote.remote-containers"
  ]
}
```

#### Launch Configuration
Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

---

## Project Structure

```
project/
├── app.py                      # Main FastAPI application
├── agent_test.py              # Agent testing utilities
├── requirements.txt           # Dependencies
├── .env                       # Environment variables (gitignored)
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
│
├── all-utils/                 # Core utilities
│   ├── main.py               # Utility entry point
│   ├── requirements.txt       # Utility dependencies
│   ├── utilities/             # Helper modules
│   │   ├── pydantic_models.py
│   │   ├── query_validation_transformation.py
│   │   ├── logging_example.py
│   │   ├── mem0_example.py
│   │   └── *.ipynb           # Jupyter notebooks
│   └── db/                    # Vector database
│       └── chroma.sqlite3
│
├── static/                    # Frontend assets
│   ├── style.css
│   └── script.js
│
├── templates/                 # HTML templates
│   └── index.html
│
├── Assets/                    # Documentation assets
│   └── architecture_*.jpg
│
├── docs/                      # Documentation
│   ├── INSTALLATION.md
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── CONFIGURATION.md
│   └── DEVELOPMENT.md
│
└── workflows/                 # Workflow diagrams
    └── *.md
```

---

## Code Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/):

```python
# ✅ Good
def get_interview_status(interview_id: str) -> dict:
    """Get interview status by ID.
    
    Args:
        interview_id: The interview identifier
        
    Returns:
        Interview status dictionary
    """
    return {"status": "active"}

# ❌ Bad
def getInterviewStatus(id):
    return {"status": "active"}
```

### Type Hints

Always use type hints:

```python
# ✅ Good
from typing import Optional, List
from pydantic import BaseModel

def process_answers(answers: List[str]) -> Optional[dict]:
    if not answers:
        return None
    return {"count": len(answers)}

# ❌ Bad
def process_answers(answers):
    return {"count": len(answers)}
```

### Docstrings

Use Google-style docstrings:

```python
def create_interview_team(
    websocket: WebSocket,
    job_position: str,
    difficulty: str = "medium"
) -> RoundRobinGroupChat:
    """Create an interview team with specified agents.
    
    This function initializes a multi-agent team consisting of
    an Interviewer agent, Evaluator agent, and Candidate proxy.
    
    Args:
        websocket: WebSocket connection for real-time communication
        job_position: The job position for interview context
        difficulty: Interview difficulty level (default: "medium")
        
    Returns:
        RoundRobinGroupChat: Configured interview team
        
    Raises:
        ValueError: If job_position is empty
        WebSocketException: If WebSocket connection fails
        
    Example:
        >>> team = await create_interview_team(ws, "Engineer")
        >>> # Use team for interview
    """
    if not job_position.strip():
        raise ValueError("Job position cannot be empty")
    
    # Implementation
    return team
```

### Imports Organization

```python
# Standard library imports
import os
import json
from typing import Optional, List
from datetime import datetime

# Third-party imports
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel, Field
from autogen_agentchat.agents import AssistantAgent

# Local imports
from all_utils.utilities.pydantic_models import SearchRequest
from all_utils.utilities.logging_example import setup_logging
```

### Error Handling

```python
# ✅ Good
try:
    response = await get_openai_response(prompt)
except openai.APIError as e:
    logger.error(f"OpenAI API error: {e}")
    raise HTTPException(status_code=500, detail="LLM error")
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise

# ❌ Bad
try:
    response = await get_openai_response(prompt)
except:
    pass
```

---

## Testing

### Unit Tests

Create `tests/test_models.py`:

```python
import pytest
from all_utils.utilities.pydantic_models import SearchRequest

def test_search_request_valid():
    """Test valid SearchRequest creation."""
    request = SearchRequest(
        user_id="user123",
        email="user@example.com",
        query="test query"
    )
    assert request.user_id == "user123"

def test_search_request_invalid_email():
    """Test SearchRequest with invalid email."""
    with pytest.raises(ValueError):
        SearchRequest(
            user_id="user123",
            email="invalid-email",
            query="test query"
        )

def test_search_request_empty_query():
    """Test SearchRequest with empty query."""
    with pytest.raises(ValueError):
        SearchRequest(
            user_id="user123",
            email="user@example.com",
            query="   "
        )
```

### Running Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_models.py::test_search_request_valid

# Run with verbose output
pytest -v
```

### Integration Tests

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_interview_start():
    """Test interview start endpoint."""
    response = client.post(
        "/interview/start",
        json={
            "job_position": "Engineer",
            "candidate_name": "John Doe",
            "candidate_email": "john@example.com",
            "experience_level": "mid"
        }
    )
    assert response.status_code == 200
    assert "interview_id" in response.json()
```

---

## Debugging

### Debug Mode

Run with debug logging:

```bash
uvicorn app:app --reload --log-level debug
```

### VS Code Debugging

1. Set breakpoints in code (red dot)
2. Press F5 or click Run → Start Debugging
3. Use Debug Console to inspect variables
4. Step through code with F10 (over) / F11 (into)

### Logging Debug Information

```python
import logging

logger = logging.getLogger(__name__)

def process_interview(interview_id: str):
    logger.debug(f"Processing interview: {interview_id}")
    try:
        # Process
        logger.info(f"Interview {interview_id} processed successfully")
    except Exception as e:
        logger.exception(f"Failed to process interview: {e}")
```

### Print Debugging

```python
# Add strategic prints
print(f"DEBUG: interview_id = {interview_id}")
print(f"DEBUG: response = {response}")
```

### WebSocket Debugging

```javascript
// Browser console debugging
const ws = new WebSocket('ws://localhost:8000/ws/123');

ws.onmessage = function(event) {
    console.log('Received:', event.data);
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};
```

---

## Common Tasks

### Add a New Endpoint

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/interviews")
async def list_interviews(skip: int = 0, limit: int = 10):
    """List all interviews with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum records to return
        
    Returns:
        List of interview summaries
    """
    # Implementation
    return {"interviews": []}
```

### Add a New Model

Create in `all-utils/utilities/pydantic_models.py`:

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class InterviewSummary(BaseModel):
    interview_id: str
    candidate_name: str
    job_position: str
    score: float = Field(..., ge=0.0, le=10.0)
    status: str
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "interview_id": "123",
                "candidate_name": "John Doe",
                "job_position": "Engineer",
                "score": 8.5,
                "status": "completed",
                "created_at": "2024-04-20"
            }
        }
```

### Update Dependencies

```bash
# View outdated packages
pip list --outdated

# Update specific package
pip install --upgrade fastapi

# Update all packages
pip install --upgrade -r requirements.txt

# Generate new requirements.txt
pip freeze > requirements.txt
```

### Create Database Migration

```python
# Backup current database
import shutil
shutil.copytree("all-utils/db", "all-utils/db.backup")

# Modify schema
# Re-initialize collections if needed
```

### Add Environment Variable

1. Add to `.env`:
   ```env
   NEW_VAR=value
   ```

2. Load in code:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   new_var = os.getenv("NEW_VAR", "default_value")
   ```

---

## Git Workflow

### Feature Branch

```bash
# Create feature branch
git checkout -b feature/interview-improvements

# Make changes
git add .
git commit -m "Add interview improvements"

# Push to remote
git push origin feature/interview-improvements

# Create pull request on GitHub
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add interview status endpoint"
git commit -m "fix: correct WebSocket handler error"
git commit -m "docs: update README with setup instructions"
git commit -m "test: add unit tests for models"
git commit -m "refactor: simplify agent creation logic"
git commit -m "perf: optimize vector database queries"
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `chore`: Maintenance

---

## Performance Optimization

### Profile Code

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
result = expensive_operation()

profiler.disable()
stats = pstats.Stats(profiler)
stats.print_stats()
```

### Async Performance

```python
# ✅ Good - Concurrent
async def process_multiple():
    tasks = [get_data(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    return results

# ❌ Bad - Sequential
async def process_multiple():
    results = []
    for i in range(10):
        result = await get_data(i)
        results.append(result)
    return results
```

### Database Optimization

```python
# Add indexes for common queries
collection.create_index()

# Batch operations
collection.add(
    ids=ids_batch,
    embeddings=embeddings_batch,
    documents=documents_batch
)
```

---

## Deployment

### Development
```bash
uvicorn app:app --reload
```

### Staging
```bash
uvicorn app:app --workers 2 --host 0.0.0.0
```

### Production
```bash
uvicorn app:app \
  --workers 4 \
  --host 0.0.0.0 \
  --port 8000 \
  --ssl-certfile=/path/to/cert.pem \
  --ssl-keyfile=/path/to/key.pem
```

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [PEP 8 Style Guide](https://pep8.org/)

