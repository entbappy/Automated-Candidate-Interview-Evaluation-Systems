# Architecture Guide

## Table of Contents
- [System Overview](#system-overview)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)

---

## System Overview

The Automated Candidate Interview Evaluation System is built on a modular, scalable architecture that separates concerns into distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Layer                          │
│              (Web UI - HTML/CSS/JavaScript)                 │
└────────────────────┬────────────────────────────────────────┘
                     │ WebSocket / HTTP
┌────────────────────▼────────────────────────────────────────┐
│                    API Layer (FastAPI)                       │
│           REST Endpoints & WebSocket Handler                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   Business Logic Layer                       │
│    ├─ Interview Orchestration (AutoGen Team)               │
│    ├─ Agent Management                                      │
│    └─ Interview Flow Control                                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   Data Layer                                 │
│    ├─ Vector Database (Chroma)                             │
│    ├─ SQLite Storage                                        │
│    └─ External LLM (OpenAI GPT-4o)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Frontend Application
**Location**: `static/` and `templates/`

**Responsibilities**:
- User interface for conducting interviews
- Real-time WebSocket communication
- Display interview questions and candidate responses
- Show evaluation feedback

**Key Files**:
- `templates/index.html` - Main interview UI
- `static/style.css` - Styling
- `static/script.js` - WebSocket client logic

### 2. FastAPI Server
**Location**: `app.py`

**Responsibilities**:
- HTTP REST API endpoints
- WebSocket endpoint management
- Request/Response handling
- Static file serving

**Key Features**:
```python
# Static and template mounting
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# WebSocket endpoint
@app.websocket("/ws/{interview_id}")
async def interview_websocket(websocket: WebSocket, interview_id: str):
    # Interview real-time communication
```

### 3. AutoGen Team (Multi-Agent System)
**Location**: `app.py` - `create_interview_team()`

**Components**:

#### 3.1 Interviewer Agent (AI)
- **Role**: Conducts the technical/behavioral interview
- **Capabilities**:
  - Generates contextual questions
  - Evaluates initial responses
  - Asks follow-up questions
  - Provides question guidance

#### 3.2 Evaluator Agent (Coach)
- **Role**: Evaluates candidate responses
- **Capabilities**:
  - Provides detailed feedback
  - Scores responses
  - Identifies strengths/weaknesses
  - Suggests improvements

#### 3.3 Candidate Proxy Agent
- **Role**: Acts as the candidate interface
- **Capabilities**:
  - Receives answers from web interface
  - Bridges user and agent communication
  - Manages input/output via WebSocket

**Agent Collaboration**:
```
Interviewer Agent
       ↓
    (asks question)
       ↓
Candidate Proxy (receives user answer)
       ↓
    (evaluates)
       ↓
Evaluator Agent
       ↓
    (provides feedback)
       ↓
Interviewer Agent (adjusts next question)
```

### 4. Data Models
**Location**: `all-utils/utilities/pydantic_models.py`

**Models**:
```python
class SearchRequest(BaseModel):
    user_id: str
    email: EmailStr
    query: str
    tags: Optional[List[str]]

class SearchResponse(BaseModel):
    status: str
    # Additional response fields
```

**Benefits**:
- Type safety
- Automatic validation
- Documentation
- IDE autocomplete

### 5. Vector Database (Chroma)
**Location**: `all-utils/db/`

**Responsibilities**:
- Store candidate profiles
- Semantic search capabilities
- Context retrieval
- Historical data storage

**Collections**:
- Candidate profiles with embeddings
- Interview transcripts
- Evaluation results

### 6. Utilities & Helpers
**Location**: `all-utils/utilities/`

**Modules**:

| Module | Purpose |
|--------|---------|
| `pydantic_models.py` | Request/response models |
| `query_validation_transformation.py` | Input validation and transformation |
| `logging_example.py` | Structured logging setup |
| `mem0_example.py` | Memory management and context |

---

## Data Flow

### Interview Flow Sequence

```
1. User initiates interview
   ↓
2. Frontend sends HTTP POST to /interview/start
   ↓
3. FastAPI creates interview session
   ↓
4. WebSocket connection established (/ws/{interview_id})
   ↓
5. AutoGen Team initialized
   ↓
6. Interviewer Agent generates first question
   ↓
7. Question sent via WebSocket to frontend
   ↓
8. User answers (frontend)
   ↓
9. Answer sent via WebSocket to backend
   ↓
10. WebSocketInputHandler processes answer
    ↓
11. Evaluator Agent evaluates response
    ↓
12. Feedback generated
    ↓
13. Feedback sent to frontend via WebSocket
    ↓
14. Loop: Back to step 6 (next question) or end interview
```

### WebSocket Communication Pattern

```javascript
// Frontend sends
websocket.send(JSON.stringify({
    type: "answer",
    interview_id: "123",
    answer_text: "The answer to the question..."
}));

// Backend processes
async def interview_websocket(websocket: WebSocket, interview_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Process answer
        # Generate feedback
        await websocket.send_text(feedback)
```

### LLM Interaction Flow

```
User Answer
    ↓
Evaluator Agent
    ↓
OpenAI GPT-4o API Call
    ├─ System: Evaluation instructions
    ├─ Messages: Interview context + answer
    └─ Temperature: 0.7 (balanced creativity)
    ↓
LLM Response
    ↓
Parse & Structure Response
    ↓
Send Feedback to User
```

---

## Technology Stack

### Backend Technologies

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Web Framework** | FastAPI | High-performance async web framework |
| **ASGI Server** | Uvicorn | Lightning-fast ASGI server |
| **Multi-Agent** | AutoGen | Agent orchestration and collaboration |
| **LLM Client** | OpenAI Python SDK | GPT-4o API integration |
| **Data Validation** | Pydantic | Type-safe request/response models |
| **Real-time Comms** | WebSockets | Bidirectional server-client communication |
| **Vector DB** | Chroma | Semantic search and embeddings |
| **Database** | SQLite | Lightweight data persistence |

### Frontend Technologies

| Component | Technology |
|-----------|-----------|
| **Markup** | HTML5 |
| **Styling** | CSS3 |
| **Scripting** | Vanilla JavaScript |
| **Real-time** | WebSocket API |
| **Templating** | Jinja2 |

### Development Tools

| Tool | Purpose |
|------|---------|
| **Package Manager** | pip / UV (recommended) |
| **Environment** | venv / conda |
| **API Testing** | OpenAPI/Swagger (automatic) |

---

## Design Patterns

### 1. Agent Pattern
Multiple specialized agents (Interviewer, Evaluator, Candidate) collaborate to achieve common goal.

**Benefits**:
- Separation of concerns
- Reusability
- Scalability
- Independent updates

### 2. Async/Await Pattern
All I/O operations are asynchronous.

```python
async def interview_websocket(websocket: WebSocket, interview_id: str):
    await websocket.accept()
    data = await websocket.receive_text()
```

**Benefits**:
- Non-blocking operations
- Better resource utilization
- Concurrent user handling

### 3. Context Pattern
WebSocketInputHandler maintains context between operations.

```python
class WebSocketInputHandler:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
```

**Benefits**:
- State management
- Clean code
- Reusability

### 4. Factory Pattern
AutoGen team creation encapsulated in factory function.

```python
async def create_interview_team(websocket: WebSocket, job_position: str):
    # Creates and configures all agents
    return team
```

### 5. Dependency Injection
Configuration and dependencies injected into components.

```python
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=OPENAI_API_KEY
)
```

---

## Scalability Considerations

### Horizontal Scaling
- FastAPI runs on ASGI, supports multiple workers
- WebSocket connections distributed across instances
- Shared vector database (Chroma) accessible from all servers

### Performance Optimization
- Async/await for concurrent operations
- Vector database for fast retrieval
- Caching interview context
- Lazy loading of agents

### Resource Management
- Connection pooling for LLM API
- Memory-efficient vector embeddings
- SQLite optimization with indexes
- Worker timeout management

---

## Security Considerations

1. **API Key Management**: Use `.env` files (not in version control)
2. **WebSocket Authentication**: Implement session tokens
3. **Input Validation**: Pydantic models validate all inputs
4. **CORS**: Configure if deploying to production
5. **Rate Limiting**: Implement for OpenAI API
6. **Logging**: Sensitive data excluded from logs

---

## Future Architecture Enhancements

- [ ] Redis caching layer
- [ ] Message queue (RabbitMQ/Kafka) for async tasks
- [ ] Multi-LLM support
- [ ] Kubernetes orchestration
- [ ] Load balancing
- [ ] Analytics and monitoring
- [ ] Persistence layer optimization
- [ ] GraphQL API option

