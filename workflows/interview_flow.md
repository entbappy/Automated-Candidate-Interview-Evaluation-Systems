# Interview Flow Workflow

## Overall Interview Process

```mermaid
graph TD
    A["👤 User/Candidate"] -->|Initiates| B["🌐 Web Browser"]
    B -->|HTTP POST| C["🚀 FastAPI Server"]
    C -->|Creates| D["🆔 Interview Session"]
    D -->|Initializes| E["🤖 AutoGen Team"]
    E -->|Starts| F["📋 Interviewer Agent"]
    
    F -->|Generates| G["❓ Interview Question"]
    G -->|Sends via| H["🔌 WebSocket"]
    H -->|Displays| B
    
    B -->|User Types Answer| I["📝 Answer Input"]
    I -->|Sends via| H
    H -->|Receives| J["✅ Answer Handler"]
    
    J -->|Passes to| K["👨‍⚖️ Evaluator Agent"]
    K -->|Evaluates with| L["🤖 OpenAI GPT-4o"]
    L -->|Returns| M["📊 Score & Feedback"]
    
    M -->|Sends| H
    H -->|Shows| B
    
    B -->|Continue?| N{Questions Remaining?}
    N -->|Yes| F
    N -->|No| O["🏁 End Interview"]
    
    O -->|Generates| P["📈 Final Report"]
    P -->|Sends| H
    H -->|Displays| B
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style E fill:#e8f5e9
    style F fill:#fce4ec
    style K fill:#fce4ec
    style L fill:#c5e1a5
    style P fill:#b3e5fc
```

## Detailed Interview Loop

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant Frontend as 🌐 Frontend
    participant Backend as 🚀 Backend
    participant Interviewer as 📋 Interviewer Agent
    participant Evaluator as 👨‍⚖️ Evaluator Agent
    participant LLM as 🤖 OpenAI GPT-4o
    participant DB as 💾 Database

    User->>Frontend: Start Interview
    Frontend->>Backend: POST /interview/start
    Backend->>DB: Create Interview Record
    Backend->>Interviewer: Initialize Agent
    
    loop Interview Questions
        Interviewer->>Interviewer: Generate Question
        Interviewer->>Frontend: Send Question (WebSocket)
        Frontend->>User: Display Question
        
        User->>Frontend: Enter Answer
        Frontend->>Backend: Send Answer (WebSocket)
        Backend->>Evaluator: Evaluate Answer
        
        Evaluator->>LLM: Call API with Answer
        LLM->>Evaluator: Return Evaluation
        Evaluator->>DB: Store Evaluation
        
        Evaluator->>Frontend: Send Feedback (WebSocket)
        Frontend->>User: Display Feedback
        
        alt Continue Interview
            Interviewer->>Interviewer: Adjust Next Question
        else End Interview
            break Interview Complete
        end
    end
    
    Interviewer->>Backend: Interview Complete
    Backend->>DB: Generate Final Report
    Backend->>Frontend: Send Final Report
    Frontend->>User: Display Results
```

## Question Generation Flow

```mermaid
graph LR
    A["📋 Interviewer Agent"] -->|Context| B["Job Position"]
    A -->|Context| C["Difficulty Level"]
    A -->|Context| D["Question Number"]
    A -->|Context| E["Previous Answers"]
    
    B & C & D & E -->|Input| F["Question Generation Logic"]
    
    F -->|Queries| G["LLM"]
    G -->|Returns| H["Generated Question"]
    
    H -->|Validation| I{Valid Question?}
    I -->|No| F
    I -->|Yes| J["✅ Question Ready"]
    
    J -->|Format| K["JSON Response"]
    K -->|Send via| L["🔌 WebSocket"]
    L -->|Display| M["👤 User"]
    
    style A fill:#fce4ec
    style G fill:#c5e1a5
    style J fill:#a5d6a7
```

## Answer Evaluation Flow

```mermaid
graph TD
    A["📝 Candidate Answer"] -->|Received| B["Answer Handler"]
    B -->|Validate| C{Valid Input?}
    
    C -->|No| D["❌ Error Message"]
    D -->|Send| E["👤 User"]
    
    C -->|Yes| F["Build Evaluation Prompt"]
    
    F -->|Include| G["Job Position"]
    F -->|Include| H["Question Context"]
    F -->|Include| I["Candidate Answer"]
    F -->|Include| J["Evaluation Criteria"]
    
    G & H & I & J -->|Compile| K["📤 LLM Request"]
    
    K -->|Call| L["🤖 OpenAI GPT-4o"]
    
    L -->|Parse Response| M["Extract Score"]
    L -->|Parse Response| N["Extract Feedback"]
    L -->|Parse Response| O["Extract Strengths"]
    L -->|Parse Response| P["Extract Improvements"]
    
    M & N & O & P -->|Structure| Q["Evaluation Object"]
    
    Q -->|Store| R["💾 Database"]
    Q -->|Format| S["JSON Response"]
    
    S -->|Send| T["🔌 WebSocket"]
    T -->|Display| E
    
    style A fill:#fff3e0
    style C fill:#ffecb3
    style L fill:#c5e1a5
    style Q fill:#a5d6a7
    style T fill:#81c784
```

## Interview Termination

```mermaid
graph TD
    A{Termination Trigger?}
    
    A -->|Max Questions| B["Questions Limit Reached"]
    A -->|User Request| C["User Clicked End"]
    A -->|Timeout| D["Session Timeout"]
    A -->|Error| E["Critical Error"]
    
    B & C & D & E -->|Signal| F["End Interview Command"]
    
    F -->|Notify| G["Interviewer Agent"]
    G -->|Prepare| H["Final Summary"]
    
    H -->|Include| I["Questions Asked"]
    H -->|Include| J["Answers Provided"]
    H -->|Include| K["Evaluations"]
    H -->|Include| L["Overall Score"]
    
    I & J & K & L -->|Compile| M["Final Report"]
    
    M -->|Store| N["💾 Database"]
    M -->|Send| O["🔌 WebSocket"]
    O -->|Display| P["👤 User"]
    
    P -->|Download?| Q["📄 PDF/JSON Export"]
    
    style A fill:#ffecb3
    style F fill:#ffb74d
    style M fill:#a5d6a7
    style Q fill:#81c784
```

---

## Notes

- The interview process is fully asynchronous for real-time responsiveness
- Questions can adapt based on previous answers
- All interactions are stored in the database for analytics
- WebSocket ensures low-latency communication
- LLM calls are optimized with proper prompting

