# System Architecture Overview

## Complete System Architecture

```mermaid
graph TB
    subgraph Client["🌐 Client Layer"]
        Browser["Web Browser"]
        UI["User Interface<br/>HTML/CSS/JS"]
        WS["WebSocket Client"]
    end
    
    subgraph API["🚀 API Layer - FastAPI"]
        Routes["HTTP Routes"]
        WS_Endpoint["WebSocket Endpoint"]
        Auth["Authentication<br/>& Validation"]
    end
    
    subgraph Business["💼 Business Logic Layer"]
        Interview["Interview<br/>Orchestrator"]
        Session["Session<br/>Manager"]
        Team["AutoGen<br/>Team Manager"]
    end
    
    subgraph Agents["🤖 Agent Layer"]
        Interviewer["📋 Interviewer<br/>Agent"]
        Evaluator["👨‍⚖️ Evaluator<br/>Agent"]
        Proxy["🎤 Candidate<br/>Proxy"]
        Queue["📨 Message<br/>Queue"]
    end
    
    subgraph External["☁️ External Services"]
        LLM["OpenAI<br/>GPT-4o API"]
        Embeddings["Embedding<br/>Service"]
    end
    
    subgraph Data["💾 Data Layer"]
        SQLite["SQLite<br/>Database"]
        Chroma["Chroma Vector<br/>Database"]
        Cache["Redis Cache<br/>Optional"]
    end
    
    Browser -->|HTTP/WebSocket| UI
    UI -->|WebSocket| WS
    WS -->|Connect| WS_Endpoint
    
    Routes & WS_Endpoint -->|Routes| Auth
    Auth -->|Validates| Interview
    
    Interview -->|Manages| Session
    Session -->|Creates| Team
    
    Team -->|Contains| Interviewer
    Team -->|Contains| Evaluator
    Team -->|Contains| Proxy
    
    Interviewer & Evaluator & Proxy -->|Communicate via| Queue
    
    Interviewer -->|API Calls| LLM
    Evaluator -->|API Calls| LLM
    
    Interviewer -->|Generate| Embeddings
    Evaluator -->|Generate| Embeddings
    
    Proxy -->|Store State| SQLite
    Evaluator -->|Store Results| SQLite
    
    Interviewer -->|Store Context| Chroma
    Evaluator -->|Query Context| Chroma
    
    Interview -->|Cache| Cache
    Session -->|Cache| Cache
    
    LLM -->|Return| Evaluator
    Embeddings -->|Return| Chroma
    
    style Client fill:#e1f5ff
    style API fill:#f3e5f5
    style Business fill:#e8f5e9
    style Agents fill:#fce4ec
    style External fill:#fff3e0
    style Data fill:#b3e5fc
```

## Data Flow Diagram

```mermaid
graph LR
    subgraph Input["📥 Input"]
        User["👤 User Input"]
        Config["⚙️ Configuration"]
    end
    
    subgraph Processing["🔄 Processing"]
        Validate["Validate"]
        Transform["Transform"]
        Route["Route"]
        Execute["Execute"]
    end
    
    subgraph Logic["🧠 Business Logic"]
        Interview["Interview Logic"]
        Agent["Agent Logic"]
        LLM["LLM Integration"]
    end
    
    subgraph Storage["💾 Storage"]
        DB["Persistent Store"]
        Vector["Vector Store"]
    end
    
    subgraph Output["📤 Output"]
        Response["HTTP Response"]
        WebSocket["WebSocket Message"]
        Report["Final Report"]
    end
    
    User & Config -->|Input| Validate
    Validate -->|Valid| Transform
    Transform -->|Transformed| Route
    Route -->|Routed| Execute
    
    Execute -->|Executes| Interview
    Interview -->|Calls| Agent
    Agent -->|Calls| LLM
    
    Interview & Agent & LLM -->|Store| DB
    Agent -->|Store Embeddings| Vector
    
    Execute -->|Format| Response
    Execute -->|Send| WebSocket
    Interview -->|Generate| Report
    
    Response & WebSocket -->|Client| Output
    Report -->|Client| Output
    
    style Input fill:#e1f5ff
    style Processing fill:#fff3e0
    style Logic fill:#f3e5f5
    style Storage fill:#b3e5fc
    style Output fill:#a5d6a7
```

## Component Interaction Matrix

```mermaid
graph TD
    A["🔗 Component Interactions"]
    
    A -->|FastAPI ↔ WebSocket| B["Bidirectional<br/>Communication"]
    A -->|Interview ↔ AutoGen| C["Team<br/>Orchestration"]
    A -->|Agents ↔ Queue| D["Message<br/>Passing"]
    A -->|Evaluator ↔ LLM| E["API<br/>Integration"]
    A -->|All ↔ Database| F["Persistence"]
    A -->|Context ↔ Vector DB| G["Semantic<br/>Search"]
    
    B -->|Enables| H["Real-time Updates"]
    C -->|Enables| I["Multi-agent Collaboration"]
    D -->|Enables| J["Async Processing"]
    E -->|Enables| K["Intelligent Evaluation"]
    F -->|Enables| L["Data Recovery"]
    G -->|Enables| M["Context Management"]
    
    H & I & J & K & L & M -->|Result| N["✅ Seamless Interview<br/>Experience"]
    
    style A fill:#b3e5fc
    style N fill:#81c784
```

## Deployment Architecture

```mermaid
graph TD
    A["🚀 Deployment"]
    
    A -->|Development| B["Local Machine"]
    B -->|Run| C["uvicorn app:app<br/>--reload"]
    C -->|Access| D["http://localhost:8000"]
    
    A -->|Staging| E["Staging Server"]
    E -->|Run| F["Multiple Workers"]
    F -->|Behind| G["Nginx/LoadBalancer"]
    G -->|Access| H["https://staging.example.com"]
    
    A -->|Production| I["Production Cluster"]
    I -->|Container| J["Docker"]
    I -->|Orchestration| K["Kubernetes/Docker Compose"]
    I -->|Behind| L["Nginx/Load Balancer"]
    L -->|SSL/TLS| M["https://app.example.com"]
    
    B & E & I -->|All Connect| N["External Services"]
    N -->|OpenAI API| O["GPT-4o"]
    N -->|Database Backup| P["Cloud Storage"]
    
    style A fill:#b3e5fc
    style B fill:#fff3e0
    style E fill:#fff9c4
    style I fill:#ffecb3
    style O fill:#c5e1a5
```

---

## Architecture Principles

1. **Separation of Concerns**: Each layer has distinct responsibility
2. **Asynchronous Processing**: Non-blocking operations throughout
3. **Scalability**: Horizontal scaling support via load balancing
4. **Resilience**: Error handling and recovery mechanisms
5. **Observability**: Logging and monitoring at each layer
6. **Security**: Input validation, authentication, encryption
7. **Maintainability**: Clear module structure and documentation

