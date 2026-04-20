# Agent Communication Workflow

## Multi-Agent Architecture

```mermaid
graph TB
    subgraph AutoGenTeam["🤖 AutoGen Team - Interview Orchestration"]
        direction TB
        
        subgraph Agents["Agents"]
            I["📋 Interviewer Agent<br/>Role: Question Generation & Follow-ups"]
            E["👨‍⚖️ Evaluator Agent<br/>Role: Response Evaluation & Scoring"]
            C["🎤 Candidate Proxy<br/>Role: User Bridge & Input Handler"]
        end
        
        subgraph Communication["Communication Channel"]
            Queue["📨 Message Queue<br/>RoundRobinGroupChat"]
        end
        
        I <-->|Messages| Queue
        E <-->|Messages| Queue
        C <-->|Messages| Queue
    end
    
    subgraph External["External Systems"]
        LLM["🤖 OpenAI GPT-4o API"]
        DB["💾 Vector Database<br/>Chroma"]
        WS["🔌 WebSocket<br/>Frontend Bridge"]
    end
    
    I -->|API Calls| LLM
    E -->|API Calls| LLM
    C -->|Store Context| DB
    C <-->|Real-time Data| WS
    
    style AutoGenTeam fill:#e3f2fd
    style I fill:#fce4ec
    style E fill:#fce4ec
    style C fill:#fff3e0
    style LLM fill:#c5e1a5
    style DB fill:#b3e5fc
    style WS fill:#81c784
```

## Agent Interaction Sequence

```mermaid
sequenceDiagram
    participant User as 👤 User<br/>Frontend
    participant Proxy as 🎤 Candidate<br/>Proxy
    participant Queue as 📨 Message<br/>Queue
    participant Interview as 📋 Interviewer<br/>Agent
    participant Evaluator as 👨‍⚖️ Evaluator<br/>Agent
    participant LLM as 🤖 GPT-4o<br/>API

    User->>Proxy: Interview Start Request
    Proxy->>Queue: Initialize Team
    
    activate Interview
    Interview->>Interview: Generate First Question
    Interview->>Queue: Send Question Message
    Queue->>User: Display Question (WebSocket)
    
    User->>User: Think & Type Answer
    User->>Proxy: Submit Answer
    Proxy->>Queue: Forward Answer
    
    deactivate Interview
    activate Evaluator
    
    Evaluator->>Evaluator: Build Evaluation Prompt
    Evaluator->>LLM: Call OpenAI API
    LLM-->>Evaluator: Return Evaluation Score & Feedback
    
    Evaluator->>Queue: Send Evaluation Message
    Queue->>User: Display Feedback (WebSocket)
    
    deactivate Evaluator
    activate Interview
    
    Interview->>Interview: Analyze Feedback<br/>Plan Next Question
    Interview->>Queue: Send Next Question
    Queue->>User: Display Next Question (WebSocket)
    
    deactivate Interview
    
    loop More Questions
        User->>Proxy: Submit Answer
        Proxy->>Queue: Forward Answer
        activate Evaluator
        Evaluator->>LLM: Evaluate
        LLM-->>Evaluator: Score & Feedback
        Evaluator->>Queue: Send Evaluation
        deactivate Evaluator
        Queue->>User: Display Results
        
        activate Interview
        Interview->>Queue: Generate Next Question
        deactivate Interview
        Queue->>User: Display Question
    end
    
    Interview->>Queue: Send Completion Signal
    Queue->>Proxy: Interview End
    Proxy->>User: Display Final Report
```

## Round-Robin Communication Pattern

```mermaid
graph TD
    A["🎯 Start Interview Round"]
    
    A -->|Turn 1| I1["📋 Interviewer<br/>Generates Question"]
    I1 -->|Adds to Queue| Q["📨 Message Queue"]
    Q -->|Delivers| U1["👤 User<br/>Sees Question"]
    
    U1 -->|Turn 2| P1["🎤 Candidate Proxy<br/>Receives Answer"]
    P1 -->|Adds to Queue| Q
    Q -->|Delivers| E1["👨‍⚖️ Evaluator<br/>Evaluates Answer"]
    
    E1 -->|Turn 3| I2["📋 Interviewer<br/>Sees Feedback<br/>Plans Next Question"]
    I2 -->|Adds to Queue| Q
    
    Q -->|Delivers| U2["👤 User<br/>Sees Feedback"]
    
    U2 -->|Repeats| A
    
    style A fill:#fff9c4
    style I1 fill:#fce4ec
    style I2 fill:#fce4ec
    style E1 fill:#fce4ec
    style P1 fill:#fff3e0
    style U1 fill:#e1f5ff
    style U2 fill:#e1f5ff
    style Q fill:#f3e5f5
```

## Interviewer Agent Behavior

```mermaid
graph TD
    A["📋 Interviewer Agent Active"]
    
    A -->|Receive| B{Message Type?}
    
    B -->|Start Signal| C["Initialize Interview Context"]
    C -->|Set| D["Job Position"]
    C -->|Set| E["Difficulty Level"]
    C -->|Set| F["Question Number"]
    
    D & E & F -->|Prepare| G["Generate First Question"]
    
    B -->|Feedback Message| H["Analyze Evaluator Feedback"]
    H -->|Check| I{Performance Level?}
    
    I -->|Excellent| J["Increase Difficulty"]
    I -->|Good| K["Maintain Difficulty"]
    I -->|Poor| L["Decrease Difficulty"]
    
    J & K & L -->|Plan| M["Generate Next Question"]
    
    B -->|End Signal| N["Prepare Completion Message"]
    
    G & M -->|Format| O["Question Message"]
    O -->|Add| P["Metadata"]
    P -->|Send| Q["📨 Message Queue"]
    
    N -->|Send| Q
    
    style A fill:#fce4ec
    style B fill:#ffecb3
    style G fill:#a5d6a7
    style M fill:#a5d6a7
    style Q fill:#f3e5f5
```

## Evaluator Agent Behavior

```mermaid
graph TD
    A["👨‍⚖️ Evaluator Agent Active"]
    
    A -->|Receive| B["Answer Message"]
    
    B -->|Extract| C["Candidate Answer"]
    B -->|Extract| D["Question Context"]
    B -->|Extract| E["Interview Context"]
    
    C & D & E -->|Build| F["Evaluation Prompt"]
    
    F -->|Add| G["Evaluation Criteria"]
    G -->|Add| H["Scoring Rubric"]
    
    F & G & H -->|Compile| I["📤 LLM Request"]
    
    I -->|Call| J["🤖 OpenAI API"]
    J -->|Parse| K["Response Analysis"]
    
    K -->|Extract| L["Numerical Score"]
    K -->|Extract| M["Qualitative Feedback"]
    K -->|Extract| N["Strengths"]
    K -->|Extract| O["Areas for Improvement"]
    
    L & M & N & O -->|Structure| P["Evaluation Result"]
    
    P -->|Store| Q["💾 Database"]
    P -->|Format| R["Feedback Message"]
    
    R -->|Add Metadata| S["Question ID"]
    R -->|Add Metadata| T["Answer ID"]
    R -->|Add Metadata| U["Timestamp"]
    
    S & T & U -->|Complete| V["📨 Message Queue"]
    
    style A fill:#fce4ec
    style B fill:#fff3e0
    style I fill:#ffe082
    style J fill:#c5e1a5
    style P fill:#a5d6a7
    style V fill:#f3e5f5
```

## Candidate Proxy Behavior

```mermaid
graph TD
    A["🎤 Candidate Proxy Active"]
    
    A -->|Connect| B["🔌 WebSocket"]
    B -->|Listen| C{Data Received?}
    
    C -->|Question from Interviewer| D["Forward to Frontend"]
    D -->|Send| B
    
    C -->|Feedback from Evaluator| E["Forward to Frontend"]
    E -->|Send| B
    
    C -->|Answer from User| F["Validate Input"]
    F -->|Check| G{Valid?}
    
    G -->|No| H["Send Error Message"]
    H -->|Send| B
    
    G -->|Yes| I["Extract Answer Text"]
    I -->|Create| J["Answer Message"]
    
    J -->|Add| K["Question ID"]
    J -->|Add| L["Timestamp"]
    J -->|Add| M["Metadata"]
    
    K & L & M -->|Complete| N["📨 Message Queue"]
    N -->|To Evaluator| O["👨‍⚖️ Evaluator Agent"]
    
    C -->|End Signal| P["Close Connection"]
    P -->|Cleanup| Q["Release Resources"]
    
    style A fill:#fff3e0
    style B fill:#81c784
    style F fill:#fff9c4
    style G fill:#ffecb3
    style J fill:#fff9c4
    style N fill:#f3e5f5
```

## Error Handling in Agent Communication

```mermaid
graph TD
    A["🚨 Error Detected"]
    
    A -->|In Agent| B["Agent Logs Error"]
    B -->|Level?| C{Error Severity?}
    
    C -->|Low| D["Continue Processing"]
    C -->|Medium| E["Attempt Retry"]
    C -->|High| F["Escalate to Handler"]
    
    E -->|Retry Logic| G{Retry Success?}
    G -->|Yes| D
    G -->|No| F
    
    F -->|Log| H["Error Details"]
    H -->|Notify| I["👤 User via WebSocket"]
    I -->|Message| J["Error: Cannot continue interview"]
    
    F -->|Cleanup| K["Release Resources"]
    K -->|Store| L["💾 Partial Data in DB"]
    L -->|Signal| M["📨 Message Queue"]
    M -->|End Interview| N["Terminate Session"]
    
    D -->|Resume| O["Continue Normally"]
    
    style A fill:#ffcccc
    style C fill:#ffecb3
    style F fill:#ff8a80
    style N fill:#ff5252
    style O fill:#81c784
```

## Agent Performance Metrics

```mermaid
graph LR
    A["📊 Agent Metrics Collection"]
    
    A -->|Track| B["Interviewer Agent"]
    B -->|Measure| C["Questions Generated: 5"]
    B -->|Measure| D["Avg Question Quality: 8.5/10"]
    B -->|Measure| E["Response Time: 500ms"]
    
    A -->|Track| F["Evaluator Agent"]
    F -->|Measure| G["Evaluations Done: 5"]
    F -->|Measure| H["Avg Accuracy: 95%"]
    F -->|Measure| I["LLM API Calls: 5"]
    
    A -->|Track| J["Candidate Proxy"]
    J -->|Measure| K["Messages Processed: 12"]
    J -->|Measure| L["Connection Uptime: 99.9%"]
    J -->|Measure| M["Error Rate: 0.5%"]
    
    C & D & E & G & H & I & K & L & M -->|Store| N["📈 Analytics DB"]
    
    style A fill:#b3e5fc
    style B fill:#fce4ec
    style F fill:#fce4ec
    style J fill:#fff3e0
    style N fill:#a5d6a7
```

---

## Key Communication Principles

1. **Asynchronous Messaging**: Agents communicate via message queue
2. **Round-Robin Turn-Taking**: Each agent gets its turn
3. **Context Preservation**: Full interview context maintained
4. **Error Isolation**: Errors in one agent don't crash others
5. **Real-Time Updates**: User sees all updates via WebSocket
6. **Scalability**: Can add more agents without breaking system

