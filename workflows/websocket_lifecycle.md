# WebSocket Lifecycle Workflow

## WebSocket Connection Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Unconnected
    
    Unconnected -->|User initiates interview| Connecting
    
    Connecting -->|Server accepts| Connected
    Connecting -->|Connection rejected| Error
    
    Connected -->|User active| Active
    Connected -->|Idle timeout| TimedOut
    
    Active -->|Send answer| Processing
    Active -->|No activity| Idle
    
    Processing -->|Evaluation complete| Active
    Processing -->|Error in evaluation| Error
    
    Idle -->|User sends data| Active
    Idle -->|Timeout exceeded| TimedOut
    
    Error -->|Retry| Connecting
    Error -->|Give up| Closed
    
    TimedOut -->|Reconnect| Connecting
    TimedOut -->|Close| Closed
    
    Active -->|User ends interview| Complete
    Complete -->|Save results| Closed
    
    Closed -->|[End]| [*]
    
    style Unconnected fill:#e1f5ff
    style Connecting fill:#fff3e0
    style Connected fill:#fff9c4
    style Active fill:#a5d6a7
    style Processing fill:#ffecb3
    style Idle fill:#ffe082
    style Error fill:#ffcccc
    style TimedOut fill:#ffb74d
    style Complete fill:#81c784
    style Closed fill:#bcaaa4
```

## Detailed Connection Sequence

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant Browser as 🌐 Browser
    participant Server as 🚀 Server
    participant Handler as 📨 Handler
    participant Team as 🤖 AutoGen Team

    User->>Browser: Click "Start Interview"
    Browser->>Server: POST /interview/start
    Server->>Server: Create session
    Server-->>Browser: {interview_id: "123"}
    
    Browser->>Browser: Create WebSocket
    Browser->>Server: WebSocket /ws/123
    
    Server->>Handler: Accept connection
    Handler->>Handler: Create handler instance
    Handler->>Team: Initialize agents
    Team-->>Handler: Ready
    
    Handler-->>Browser: ✅ Connected
    Browser->>User: Ready for interview
    
    activate Browser
    Browser->>User: Listen for events
    
    Server->>Handler: Start interview
    Handler->>Team: Generate first question
    Team-->>Handler: Question
    Handler-->>Browser: {type: "question", content: "..."}
    Browser->>User: Display question
    deactivate Browser
    
    User->>Browser: Type answer
    activate Browser
    Browser->>Server: {type: "answer", text: "..."}
    Server->>Handler: Receive message
    Handler->>Team: Forward answer to evaluator
    Team-->>Handler: Evaluation result
    Handler-->>Browser: {type: "feedback", ...}
    Browser->>User: Display feedback
    deactivate Browser
    
    loop More Questions
        Server->>Handler: Send next question
        Handler-->>Browser: {type: "question", ...}
        Browser->>User: Display question
        User->>Browser: Type answer
        Browser->>Server: Send answer
        Server->>Handler: Process
        Handler-->>Browser: Send feedback
    end
    
    User->>Browser: Click "End Interview"
    Browser->>Server: {type: "end", ...}
    Server->>Handler: Close handler
    Handler->>Team: Finalize interview
    Team-->>Handler: Final report
    Handler-->>Browser: {type: "complete", report: {...}}
    Browser->>User: Display results
    
    Browser->>Server: Close connection
    Server->>Handler: Cleanup
    Handler->>Handler: Save state
    Server->>Browser: Connection closed
    Browser->>User: Interview ended
```

## Message Flow During Active Interview

```mermaid
graph TD
    subgraph Client["🌐 Client Side (Browser)"]
        U["👤 User"]
        UI["UI Interface"]
        WS_Client["WebSocket Client"]
    end
    
    subgraph Server["🚀 Server Side"]
        WS_Handler["WebSocket Handler"]
        Input["Input Handler"]
        Queue["Message Queue"]
        Team["AutoGen Team"]
    end
    
    subgraph Question["Question Generation"]
        Team -->|Generates| Q["Question"]
        Q -->|Sends| WS_Handler
        WS_Handler -->|Sends| WS_Client
        WS_Client -->|Displays| UI
        UI -->|Shows| U
    end
    
    subgraph Answer["Answer Submission"]
        U -->|Types| UI
        UI -->|Sends| WS_Client
        WS_Client -->|Sends| WS_Handler
        WS_Handler -->|Validates| Input
        Input -->|Forwards| Queue
        Queue -->|To Evaluator| Team
    end
    
    subgraph Feedback["Feedback Reception"]
        Team -->|Evaluates| FB["Feedback"]
        FB -->|Sends| WS_Handler
        WS_Handler -->|Sends| WS_Client
        WS_Client -->|Displays| UI
        UI -->|Shows| U
    end
    
    style Client fill:#e1f5ff
    style Server fill:#f3e5f5
    style Question fill:#c8e6c9
    style Answer fill:#fff9c4
    style Feedback fill:#ffccbc
```

## Message Format Specifications

```mermaid
graph TD
    A["📨 WebSocket Messages"]
    
    A -->|Client to Server| B["Answer Message"]
    B -->|Structure| C["<br/>{'type': 'answer',<br/>'interview_id': '123',<br/>'answer_text': '...',<br/>'timestamp': '...'<br/>}"]
    
    A -->|Server to Client| D["Question Message"]
    D -->|Structure| E["<br/>{'type': 'question',<br/>'content': '...',<br/>'question_number': 1,<br/>'timestamp': '...'<br/>}"]
    
    A -->|Server to Client| F["Feedback Message"]
    F -->|Structure| G["<br/>{'type': 'feedback',<br/>'evaluation': '...',<br/>'score': 8.5,<br/>'strengths': [...],<br/>'improvements': [...],<br/>'timestamp': '...'<br/>}"]
    
    A -->|Server to Client| H["System Message"]
    H -->|Status| I["'interview_complete'"]
    H -->|Status| J["'system_turn:user'"]
    H -->|Status| K["'error'"]
    
    C & E & G & I & J & K -->|Format| L["JSON"]
    
    style A fill:#b3e5fc
    style B fill:#fff3e0
    style D fill:#fff9c4
    style F fill:#ffecb3
    style H fill:#ffe082
    style L fill:#a5d6a7
```

## Error Handling During WebSocket Session

```mermaid
graph TD
    A["🔴 WebSocket Error Detected"]
    
    A -->|Type| B{Error Category}
    
    B -->|Connection Error| C["Lost connection"]
    C -->|Action| D["Attempt Reconnect"]
    D -->|Retry| E{Reconnect Success?}
    E -->|Yes| F["Resume Session"]
    E -->|No| G["Close Connection"]
    
    B -->|Timeout Error| H["No data received"]
    H -->|Action| I["Send Ping"]
    I -->|Response| J{Server Alive?}
    J -->|Yes| K["Continue"]
    J -->|No| G
    
    B -->|Invalid Message| L["Malformed data"]
    L -->|Action| M["Log Error"]
    M -->|Notify| N["👤 User"]
    N -->|Message| O["Ask to retry"]
    
    B -->|Server Error| P["500 Internal Error"]
    P -->|Action| Q["Log Details"]
    Q -->|Notify| N
    N -->|Message| R["Apology message"]
    R -->|Option| S["Save progress"]
    S -->|Close| G
    
    B -->|Validation Error| T["Invalid input"]
    T -->|Action| U["Send error message"]
    U -->|User corrects| V["Resubmit"]
    V -->|Continue| K
    
    F -->|Resume| W["Continue Interview"]
    G -->|Cleanup| X["Release resources"]
    K -->|Resume| W
    
    style A fill:#ffcccc
    style B fill:#ffecb3
    style D fill:#ffe082
    style G fill:#ff8a80
    style W fill:#a5d6a7
    style X fill:#bcaaa4
```

## Reconnection Strategy

```mermaid
graph TD
    A["🔌 WebSocket Disconnected"]
    
    A -->|User Still Active?| B{Check Activity}
    B -->|Yes| C["Trigger Reconnection"]
    B -->|No| D["Silent Close"]
    
    C -->|Attempt 1| E["Immediate Retry"]
    E -->|Success?| F{Connected?}
    F -->|Yes| G["Restore Session"]
    F -->|No| H["Wait 1 second"]
    
    H -->|Attempt 2| I["Exponential Backoff Retry"]
    I -->|Success?| F
    F -->|No| J["Wait 2 seconds"]
    
    J -->|Attempt 3| K["Retry"]
    K -->|Success?| F
    F -->|No| L["Wait 4 seconds"]
    
    L -->|Attempt 4| M["Final Retry"]
    M -->|Success?| F
    F -->|No| N["Fail - Show Error"]
    
    F -->|Yes| O["Session State"]
    O -->|Retrieve| P["Pending Data"]
    O -->|Retrieve| Q["Last Question"]
    O -->|Retrieve| R["Partial Answers"]
    
    P & Q & R -->|Restore| G
    
    G -->|Resume From| S["Last Question"]
    S -->|Continue| T["Interview Proceeds"]
    
    N -->|Offer| U["Retry Manually"]
    U -->|Option| V["Save Progress"]
    V -->|Option| W["End Session"]
    
    T -->|Success| X["✅ Interview Continues"]
    W -->|Cleanup| Y["❌ Session Ends"]
    
    style A fill:#ffcccc
    style C fill:#ffe082
    style G fill:#a5d6a7
    style X fill:#81c784
    style Y fill:#bcaaa4
```

## Keep-Alive Mechanism

```mermaid
graph TD
    A["⏱️ Keep-Alive Timer"]
    
    A -->|Start| B["Set Ping Interval"]
    B -->|Interval| C["30 seconds"]
    
    C -->|Send| D["Ping Message"]
    D -->|Server Receives| E["Pong Response"]
    E -->|Client Receives| F{Pong OK?}
    
    F -->|Yes| G["✅ Connection Alive"]
    G -->|Reset Timer| C
    
    F -->|No| H["❌ No Response"]
    H -->|Trigger| I["Reconnection"]
    
    C -->|Timeout| J{Timer Expired?}
    J -->|No| K["Continue Waiting"]
    J -->|Yes| L["Force Reconnect"]
    
    K -->|New Data?| M{Message Received?}
    M -->|Yes| N["Reset Timer"]
    N -->|Continue| C
    M -->|No| C
    
    style A fill:#b3e5fc
    style G fill:#a5d6a7
    style H fill:#ffcccc
    style L fill:#ff8a80
```

## Session State Management

```mermaid
graph TD
    A["💾 Session State"]
    
    A -->|Store| B["interview_id"]
    A -->|Store| C["current_question"]
    A -->|Store| D["question_number"]
    A -->|Store| E["answers_submitted"]
    A -->|Store| F["evaluations_received"]
    A -->|Store| G["connection_status"]
    A -->|Store| H["last_activity_timestamp"]
    
    B & C & D & E & F -->|In| I["🗄️ Server Memory"]
    G & H -->|In| I
    
    I -->|When Disconnect| J["Persist to Database"]
    
    J -->|Save| K["Incomplete Session"]
    K -->|Store| L["💾 SQLite"]
    
    J -->|On Reconnect| M["Restore Session"]
    M -->|Load| N["Previous State"]
    N -->|Resume From| O["Last Known State"]
    
    O -->|Continue| P["Interview Resumes"]
    
    style A fill:#b3e5fc
    style I fill:#fff3e0
    style J fill:#ffe082
    style K fill:#ffecb3
    style M fill:#a5d6a7
    style P fill:#81c784
```

## Connection Closing Sequence

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant Browser as 🌐 Browser
    participant Server as 🚀 Server
    participant DB as 💾 Database

    User->>Browser: Click "End Interview"
    Browser->>Server: {type: "end"}
    
    Server->>Server: Mark as ending
    Server->>DB: Update status to "completed"
    Server->>DB: Save all evaluations
    Server->>DB: Generate final report
    
    DB-->>Server: ✅ Saved
    Server-->>Browser: {type: "complete", report: {...}}
    
    Browser->>User: Display final results
    
    User->>Browser: Read results
    Browser->>Server: Close WebSocket
    
    Server->>Server: Cleanup handler
    Server->>Server: Release resources
    Server->>DB: Final timestamp
    
    Server-->>Browser: Connection closed
    Browser->>Browser: Clear WebSocket
    User->>Browser: Interview complete
```

---

## Key Points

1. **Graceful Degradation**: Handles disconnections gracefully
2. **Auto-Reconnection**: Attempts to reconnect with exponential backoff
3. **State Persistence**: Session state saved for recovery
4. **Keep-Alive**: Regular pings prevent idle disconnects
5. **Message Acknowledgment**: Ensures reliable delivery
6. **Error Recovery**: Can resume from last checkpoint

