# 📊 Workflow Diagrams & Architecture Documentation

This folder contains comprehensive Mermaid flowcharts and diagrams documenting all major components and processes in the Automated Candidate Interview Evaluation System.

---

## 📑 Quick Navigation

| Diagram | Focus | Key Topics |
|---------|-------|-----------|
| **[Interview Flow](interview_flow.md)** | Overall interview process | Question generation, Answer evaluation, Interview termination |
| **[Agent Communication](agent_communication.md)** | Multi-agent interactions | Agent orchestration, Message passing, Round-robin protocol |
| **[Evaluation Process](evaluation_process.md)** | Answer evaluation pipeline | Scoring methodology, Feedback generation, Data storage |
| **[WebSocket Lifecycle](websocket_lifecycle.md)** | Real-time communication | Connection management, Error handling, Keep-alive mechanism |
| **[System Architecture](system_architecture.md)** | Overall system design | Component layering, Data flow, Deployment patterns |

---

## 🎯 Overview

### Interview Flow
High-level visualization of the complete interview process from initiation to completion.

**Key Insights:**
- Interview loop structure
- Question generation process
- Answer evaluation flow
- Interview termination handling

**View**: [interview_flow.md](interview_flow.md)

---

### Agent Communication
Deep dive into how the multi-agent system orchestrates interview conduct.

**Key Insights:**
- Interviewer, Evaluator, and Candidate Proxy interaction
- Round-robin message passing
- Team initialization and coordination
- Error handling between agents

**View**: [agent_communication.md](agent_communication.md)

---

### Evaluation Process
Detailed pipeline for evaluating candidate answers using LLM integration.

**Key Insights:**
- Prompt construction and validation
- LLM API integration
- Response parsing and scoring
- Multi-question aggregation
- Feedback generation

**View**: [evaluation_process.md](evaluation_process.md)

---

### WebSocket Lifecycle
Complete lifecycle management of WebSocket connections for real-time communication.

**Key Insights:**
- Connection states and transitions
- Message formats and protocols
- Reconnection strategies
- Session state management
- Keep-alive mechanisms

**View**: [websocket_lifecycle.md](websocket_lifecycle.md)

---

### System Architecture
High-level system design showing all components and their interactions.

**Key Insights:**
- Layered architecture (Client, API, Business Logic, Data)
- Technology stack
- External integrations
- Deployment patterns
- Component interactions

**View**: [system_architecture.md](system_architecture.md)

---

## 🔄 Data Flow Summary

```
User Input
    ↓
FastAPI Server (Validation)
    ↓
Interview Orchestrator
    ↓
AutoGen Team (Agents)
    ├─ Interviewer Agent → Question Generation
    ├─ Evaluator Agent → LLM Evaluation
    └─ Candidate Proxy → WebSocket Bridge
    ↓
OpenAI GPT-4o API (Scoring & Feedback)
    ↓
Database Storage (SQLite + Chroma)
    ↓
WebSocket → User Feedback
```

---

## 🛠️ Technology Stack

### Core Components
- **FastAPI**: Web framework and REST API
- **WebSocket**: Real-time bidirectional communication
- **AutoGen**: Multi-agent orchestration
- **OpenAI GPT-4o**: Language model for evaluation
- **Chroma**: Vector database for embeddings
- **SQLite**: Persistent data storage

### Design Patterns
- **Agent Pattern**: Specialized agents collaborating
- **Async/Await**: Non-blocking operations
- **Message Queue**: Asynchronous communication
- **Factory Pattern**: Component creation
- **Dependency Injection**: Configuration management

---

## 📊 Mermaid Diagram Types Used

- **Graph (Flowchart)**: Process flows and decision trees
- **Sequence Diagram**: Interaction sequences over time
- **State Diagram**: State transitions and lifecycle
- **Class Diagram**: Data models and relationships

---

## 🔐 Security Considerations

1. **Input Validation**: All user inputs validated via Pydantic
2. **WebSocket Security**: Session tokens for connection validation
3. **API Key Management**: Environment variables, never hardcoded
4. **CORS Configuration**: Restricted origin access
5. **Error Handling**: Sensitive data excluded from logs

---

## 🚀 Performance Optimization

### Identified Optimization Points
- **Async Processing**: All I/O operations non-blocking
- **Vector Database**: Fast semantic search
- **Caching**: Optional Redis layer
- **Connection Pooling**: API request optimization
- **Worker Scaling**: Multiple Uvicorn workers

### Scalability Considerations
- Horizontal scaling via load balancing
- Database optimization with indexes
- Vector database for efficient queries
- WebSocket distribution across servers

---

## 📈 Metrics & Monitoring

### Key Metrics to Track
- **Response Time**: Question generation, Evaluation latency
- **Success Rate**: Completed interviews / Total initiated
- **API Usage**: OpenAI API calls, Token consumption
- **WebSocket Health**: Connection uptime, Reconnection attempts
- **Database Performance**: Query latency, Storage growth

### Logging Strategy
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Request tracing with interview_id
- Performance profiling

---

## 🔄 Workflow Integration

These diagrams work together to provide complete system understanding:

1. **Start with System Architecture** → Understand overall design
2. **Study Interview Flow** → Follow the user journey
3. **Learn Agent Communication** → Understand multi-agent orchestration
4. **Explore Evaluation Process** → Deep dive into AI evaluation
5. **Master WebSocket Lifecycle** → Understand real-time communication

---

## 📚 Related Documentation

- [Installation Guide](../docs/INSTALLATION.md)
- [Architecture Guide](../docs/ARCHITECTURE.md)
- [API Reference](../docs/API_REFERENCE.md)
- [Configuration Guide](../docs/CONFIGURATION.md)
- [Development Guide](../docs/DEVELOPMENT.md)

---

## 🤝 Contributing

When adding new components or modifying workflows:

1. Update relevant diagram(s)
2. Update this index file
3. Ensure consistency across diagrams
4. Add explanatory notes
5. Link to documentation

---

## 📝 Notes

- All diagrams are created using Mermaid.js
- Diagrams can be edited directly in markdown files
- Color coding helps distinguish different component types:
  - 🔵 **Blue**: Client/Frontend
  - 🟢 **Green**: Successful state
  - 🟡 **Yellow**: Processing/Transition
  - 🔴 **Red**: Error/Failed state
  - 🟣 **Purple**: Business logic
  - 🟠 **Orange**: External services

---

## 🎓 Learning Path

**Beginner**: Start with System Architecture → Interview Flow
**Intermediate**: Add Agent Communication → Evaluation Process
**Advanced**: Master WebSocket Lifecycle → Deep dive into each component

---

**Last Updated**: April 2024

For questions or improvements, refer to the [Development Guide](../docs/DEVELOPMENT.md).

