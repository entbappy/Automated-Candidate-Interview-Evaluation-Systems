# API Reference

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## Overview

The Automated Candidate Interview Evaluation System provides both HTTP REST endpoints and WebSocket connections for real-time communication.

### Base URL
```
http://localhost:8000
```

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Authentication

### API Key Management
Currently uses environment variable-based authentication. For production, implement:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    token = credentials.credentials
    if token != valid_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
```

---

## Endpoints

### Root Endpoint

#### GET `/`
Returns the main interview UI.

**Response**: HTML page

```bash
curl http://localhost:8000/
```

---

### Interview Management

#### POST `/interview/start`
Initiates a new interview session.

**Request**:
```json
{
    "job_position": "Software Engineer",
    "candidate_name": "John Doe",
    "candidate_email": "john@example.com",
    "experience_level": "mid"
}
```

**Response**:
```json
{
    "interview_id": "uuid-123456",
    "status": "started",
    "job_position": "Software Engineer",
    "timestamp": "2024-04-20T10:30:00Z"
}
```

**Status Codes**:
- `200`: Interview started successfully
- `400`: Invalid request data
- `500`: Server error

---

#### GET `/interview/{interview_id}`
Retrieves interview status and details.

**Parameters**:
- `interview_id` (path): Interview unique identifier

**Response**:
```json
{
    "interview_id": "uuid-123456",
    "status": "in_progress",
    "current_question": "Tell us about your experience with Python",
    "questions_asked": 5,
    "responses_collected": 5,
    "job_position": "Software Engineer",
    "started_at": "2024-04-20T10:30:00Z",
    "last_updated": "2024-04-20T10:35:00Z"
}
```

**Status Codes**:
- `200`: Interview found
- `404`: Interview not found
- `500`: Server error

---

#### POST `/interview/{interview_id}/end`
Concludes an interview and generates final evaluation.

**Parameters**:
- `interview_id` (path): Interview unique identifier

**Request** (optional):
```json
{
    "notes": "Additional interviewer notes"
}
```

**Response**:
```json
{
    "interview_id": "uuid-123456",
    "status": "completed",
    "final_score": 8.5,
    "summary": "Strong technical knowledge with good communication",
    "strengths": [
        "Problem-solving approach",
        "Communication clarity"
    ],
    "areas_for_improvement": [
        "System design experience"
    ],
    "completed_at": "2024-04-20T10:50:00Z",
    "duration_minutes": 20
}
```

**Status Codes**:
- `200`: Interview ended successfully
- `404`: Interview not found
- `500`: Server error

---

### WebSocket Endpoints

#### WebSocket `/ws/{interview_id}`
Real-time bidirectional communication channel for interview conduct.

**Connection**:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/uuid-123456');
```

**Message Format** (Client → Server):
```json
{
    "type": "answer",
    "interview_id": "uuid-123456",
    "answer_text": "My answer to the question...",
    "timestamp": "2024-04-20T10:35:00Z"
}
```

**Message Format** (Server → Client):
```json
{
    "type": "question",
    "content": "What is your experience with REST APIs?",
    "question_number": 3
}
```

or

```json
{
    "type": "feedback",
    "evaluation": "Good understanding of REST principles. Could elaborate more on error handling.",
    "score": 8.0,
    "follow_up_question": "Can you explain how you would handle 404 errors?"
}
```

**WebSocket Events**:

| Event | Direction | Purpose |
|-------|-----------|---------|
| `question` | Server → Client | Send interview question |
| `answer` | Client → Server | Submit candidate answer |
| `feedback` | Server → Client | Provide evaluation feedback |
| `next_question` | Server → Client | Move to next question |
| `interview_complete` | Server → Client | Interview finished |
| `error` | Server → Client | Error occurred |

---

## Data Models

### Interview Model
```python
class Interview(BaseModel):
    interview_id: str
    job_position: str
    candidate_name: str
    candidate_email: EmailStr
    experience_level: str  # "junior" | "mid" | "senior"
    status: str  # "not_started" | "in_progress" | "completed"
    started_at: datetime
    ended_at: Optional[datetime]
    questions: List[str]
    answers: List[str]
    evaluations: List[str]
    final_score: Optional[float]
```

### Question Model
```python
class Question(BaseModel):
    id: str
    interview_id: str
    content: str
    category: str  # "technical" | "behavioral"
    difficulty: str  # "easy" | "medium" | "hard"
    question_number: int
    created_at: datetime
```

### Answer Model
```python
class Answer(BaseModel):
    id: str
    interview_id: str
    question_id: str
    candidate_response: str
    submitted_at: datetime
    duration_seconds: int
```

### Evaluation Model
```python
class Evaluation(BaseModel):
    id: str
    interview_id: str
    question_id: str
    answer_id: str
    score: float  # 0.0 - 10.0
    feedback: str
    strengths: List[str]
    areas_for_improvement: List[str]
    evaluator_agent: str
    evaluated_at: datetime
```

### Request Validation Model
```python
class SearchRequest(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    query: str = Field(..., min_length=1, max_length=200)
    tags: Optional[List[str]] = Field(default_factory=list)

    @field_validator('query')
    def query_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Query must not be empty or whitespace')
        return value.strip()
```

---

## Error Handling

### Error Response Format
```json
{
    "detail": "Error message",
    "status_code": 400,
    "error_type": "ValidationError",
    "timestamp": "2024-04-20T10:35:00Z"
}
```

### Common Error Codes

| Code | Meaning | Cause |
|------|---------|-------|
| `200` | OK | Request successful |
| `400` | Bad Request | Invalid input data |
| `401` | Unauthorized | Missing/invalid authentication |
| `404` | Not Found | Resource doesn't exist |
| `422` | Unprocessable Entity | Validation error |
| `500` | Internal Server Error | Server-side error |
| `503` | Service Unavailable | Service temporarily unavailable |

### Validation Errors
```json
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "invalid email address",
            "type": "value_error.email"
        }
    ]
}
```

---

## Examples

### Example 1: Start Interview
```bash
curl -X POST http://localhost:8000/interview/start \
  -H "Content-Type: application/json" \
  -d '{
    "job_position": "Backend Engineer",
    "candidate_name": "Alice Johnson",
    "candidate_email": "alice@example.com",
    "experience_level": "mid"
  }'
```

**Response**:
```json
{
    "interview_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "started"
}
```

---

### Example 2: WebSocket Real-Time Interview
```javascript
// JavaScript client
const ws = new WebSocket('ws://localhost:8000/ws/550e8400-e29b-41d4-a716-446655440000');

ws.onopen = function() {
    console.log('Connected to interview');
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    
    if (message.type === 'question') {
        console.log('Q: ' + message.content);
        // Show question to user
        // Wait for answer
        // Send answer
        ws.send(JSON.stringify({
            type: 'answer',
            answer_text: 'User\'s answer here'
        }));
    } else if (message.type === 'feedback') {
        console.log('Feedback: ' + message.evaluation);
        // Display feedback to user
    } else if (message.type === 'interview_complete') {
        console.log('Interview completed!');
        // Show final results
    }
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};
```

---

### Example 3: Get Interview Status
```bash
curl http://localhost:8000/interview/550e8400-e29b-41d4-a716-446655440000
```

**Response**:
```json
{
    "interview_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "in_progress",
    "current_question": "Describe your approach to debugging a complex issue",
    "questions_asked": 3,
    "responses_collected": 3,
    "job_position": "Backend Engineer"
}
```

---

### Example 4: End Interview
```bash
curl -X POST http://localhost:8000/interview/550e8400-e29b-41d4-a716-446655440000/end \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Very impressive candidate with strong fundamentals"
  }'
```

**Response**:
```json
{
    "interview_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "final_score": 8.7,
    "summary": "Excellent technical knowledge with outstanding communication skills",
    "strengths": [
        "Strong problem-solving abilities",
        "Clear communication",
        "Good understanding of system design"
    ],
    "areas_for_improvement": [
        "More experience with distributed systems",
        "Cloud platform expertise"
    ],
    "duration_minutes": 25
}
```

---

## Rate Limiting

Current implementation does not have rate limiting. For production, implement:

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

## Pagination

Currently not implemented. For large datasets:

```python
class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)

@app.get("/interviews")
async def list_interviews(params: PaginationParams = Depends()):
    # Paginated response
```

---

## Webhook Support

Webhooks can be added for async notifications:

```python
class WebhookEvent(BaseModel):
    event_type: str  # "interview.started", "interview.completed"
    interview_id: str
    timestamp: datetime
    data: dict

@app.post("/webhooks/register")
async def register_webhook(url: str, events: List[str]):
    # Register webhook endpoint
```

