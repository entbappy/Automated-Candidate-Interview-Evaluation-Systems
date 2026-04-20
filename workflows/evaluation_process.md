# Evaluation Process Workflow

## High-Level Evaluation Process

```mermaid
graph TD
    A["📝 Candidate Answer Received"]
    
    A -->|Validate| B{Answer Valid?}
    B -->|No| C["❌ Reject - Ask for Clarification"]
    C -->|Send| D["🔌 WebSocket to User"]
    D -->|User Resubmits| A
    
    B -->|Yes| E["✅ Answer Accepted"]
    E -->|Prepare| F["Build Evaluation Prompt"]
    
    F -->|Include Context| G["Job Position & Level"]
    F -->|Include Context| H["Question Being Answered"]
    F -->|Include Context| I["Expected Answer Structure"]
    F -->|Include Context| J["Evaluation Criteria"]
    
    G & H & I & J -->|Compile| K["📤 LLM Request"]
    
    K -->|Call| L["🤖 OpenAI GPT-4o"]
    L -->|Return| M["Evaluation Response"]
    
    M -->|Parse| N["Score 0-10"]
    M -->|Parse| O["Feedback Text"]
    M -->|Parse| P["Strengths List"]
    M -->|Parse| Q["Improvements List"]
    
    N & O & P & Q -->|Structure| R["📊 Evaluation Object"]
    
    R -->|Store| S["💾 Database"]
    R -->|Format| T["JSON Response"]
    
    T -->|Send| D
    D -->|Display| U["👤 User Sees Feedback"]
    
    style A fill:#fff3e0
    style B fill:#ffecb3
    style C fill:#ffcccc
    style E fill:#a5d6a7
    style K fill:#ffe082
    style L fill:#c5e1a5
    style R fill:#a5d6a7
    style U fill:#e1f5ff
```

## Evaluation Prompt Construction

```mermaid
graph TD
    A["🛠️ Build Evaluation Prompt"]
    
    A -->|Part 1: System Instructions| B["You are an expert evaluator<br/>Rate on technical knowledge<br/>Communication clarity<br/>Problem-solving approach"]
    
    A -->|Part 2: Context| C["Job Position: Software Engineer"]
    A -->|Part 2: Context| D["Experience Level: Mid-Senior"]
    A -->|Part 2: Context| E["Question Category: System Design"]
    
    B & C & D & E -->|Combine| F["📝 System Prompt"]
    
    A -->|Part 3: Question| G["Question: Describe a system<br/>you've designed"]
    
    A -->|Part 4: Answer| H["Candidate Answer:<br/>..answer text..."]
    
    F & G & H -->|Form| I["📤 Complete Prompt"]
    
    I -->|With Parameters| J["temperature: 0.5"]
    I -->|With Parameters| K["max_tokens: 500"]
    I -->|With Parameters| L["model: gpt-4o"]
    
    J & K & L -->|Configure| M["🔧 LLM Configuration"]
    
    M -->|Send to| N["🤖 OpenAI API"]
    
    style A fill:#b3e5fc
    style F fill:#ffecb3
    style I fill:#ffe082
    style N fill:#c5e1a5
```

## Response Parsing & Structuring

```mermaid
graph TD
    A["📥 LLM Response Received"]
    
    A -->|Raw Response| B["Parse Response Text"]
    
    B -->|Extract| C["Score Extraction"]
    C -->|Regex| D["Find: 'Score: X/10'"]
    D -->|Validate| E{Valid Score?}
    E -->|No| F["Default to 5.0"]
    E -->|Yes| G["✅ Score Extracted"]
    
    F & G -->|Store| H["score: float"]
    
    B -->|Extract| I["Feedback Extraction"]
    I -->|Find| J["'Feedback: ...'"]
    J -->|Clean| K["feedback: string"]
    
    B -->|Extract| L["Strengths Extraction"]
    L -->|Find| M["'Strengths: ...'"]
    M -->|Split| N["strengths: List[str]"]
    
    B -->|Extract| O["Improvements Extraction"]
    O -->|Find| P["'Areas for Improvement: ...'"]
    P -->|Split| Q["improvements: List[str]"]
    
    B -->|Extract| R["Summary Extraction"]
    R -->|Find| S["'Summary: ...'"]
    S -->|Summarize| T["summary: string"]
    
    H & K & N & Q & T -->|Validate| U{All Fields Present?}
    U -->|No| V["Log Warning"]
    U -->|Yes| W["✅ All Data Valid"]
    
    V & W -->|Combine| X["🏗️ Structure Response"]
    
    X -->|Create| Y["Evaluation Object"]
    Y -->|include| Z1["score"]
    Y -->|include| Z2["feedback"]
    Y -->|include| Z3["strengths"]
    Y -->|include| Z4["improvements"]
    Y -->|include| Z5["summary"]
    
    style A fill:#fff3e0
    style C fill:#fff9c4
    style I fill:#fff9c4
    style L fill:#fff9c4
    style O fill:#fff9c4
    style R fill:#fff9c4
    style U fill:#ffecb3
    style X fill:#a5d6a7
    style Y fill:#81c784
```

## Scoring Methodology

```mermaid
graph TD
    A["📊 Scoring Components"]
    
    A -->|Component 1| B["Technical Accuracy"]
    B -->|Weight| C["40%"]
    B -->|Criteria| D["Correct concepts<br/>Proper terminology<br/>Sound logic"]
    
    A -->|Component 2| E["Communication"]
    E -->|Weight| F["25%"]
    E -->|Criteria| G["Clarity<br/>Organization<br/>Completeness"]
    
    A -->|Component 3| H["Problem-Solving"]
    H -->|Weight| I["20%"]
    H -->|Criteria| J["Creativity<br/>Optimization<br/>Edge Cases"]
    
    A -->|Component 4| K["Depth of Knowledge"]
    K -->|Weight| L["15%"]
    K -->|Criteria| M["Trade-offs<br/>Alternatives<br/>Best Practices"]
    
    C & F & I & L -->|Calculate| N["🧮 Weighted Score"]
    
    N -->|Formula| O["Score = (C*0.4 + E*0.25<br/>+ H*0.2 + K*0.15)"]
    
    O -->|Range| P["0.0 - 10.0"]
    
    P -->|Grade| Q{Final Score}
    Q -->|9.0-10.0| R["⭐ Excellent"]
    Q -->|8.0-8.9| S["👍 Very Good"]
    Q -->|7.0-7.9| T["✅ Good"]
    Q -->|6.0-6.9| U["📝 Fair"]
    Q -->|Below 6.0| V["❌ Needs Improvement"]
    
    style A fill:#b3e5fc
    style N fill:#ffe082
    style O fill:#ffcc80
    style P fill:#ffb74d
    style R fill:#81c784
    style S fill:#a5d6a7
    style T fill:#c5e1a5
    style U fill:#ffecb3
    style V fill:#ffcccc
```

## Multi-Question Evaluation Aggregation

```mermaid
graph TD
    A["📋 Multiple Questions"]
    
    A -->|Q1| B["Question 1: Technical"]
    B -->|Answer 1| C["Score: 8.5"]
    C -->|Store| D["DB: Q1 Evaluation"]
    
    A -->|Q2| E["Question 2: Design"]
    E -->|Answer 2| F["Score: 7.2"]
    F -->|Store| G["DB: Q2 Evaluation"]
    
    A -->|Q3| H["Question 3: Behavioral"]
    H -->|Answer 3| I["Score: 8.8"]
    I -->|Store| J["DB: Q3 Evaluation"]
    
    D & G & J -->|Aggregate| K["📊 Calculate Overall Score"]
    
    K -->|Formula| L["Overall = (8.5 + 7.2 + 8.8) / 3"]
    L -->|Result| M["Overall Score: 8.17/10"]
    
    K -->|Aggregate| N["🔍 Combine Strengths"]
    N -->|Result| O["Strengths List:<br/>- Problem solving<br/>- Communication<br/>- Technical depth"]
    
    K -->|Aggregate| P["📈 Combine Improvements"]
    P -->|Result| Q["Improvements:<br/>- System design<br/>- Scalability thinking"]
    
    M & O & Q -->|Create| R["📄 Final Report"]
    
    R -->|Include| S["Interview Summary"]
    R -->|Include| T["Category Breakdown"]
    R -->|Include| U["Recommendations"]
    
    style A fill:#b3e5fc
    style C fill:#fff9c4
    style F fill:#fff9c4
    style I fill:#fff9c4
    style K fill:#ffecb3
    style M fill:#ffb74d
    style R fill:#a5d6a7
```

## Feedback Generation Flow

```mermaid
graph TD
    A["✍️ Generate Feedback"]
    
    A -->|Analyze| B["Score Level"]
    B -->|High 8-10| C["Affirm Strengths"]
    C -->|Message| D["'Excellent work on...'"]
    
    B -->|Medium 6-8| E["Balance Feedback"]
    E -->|Message| F["'Good understanding of...<br/>Consider improving...'"]
    
    B -->|Low Below 6| G["Constructive Criticism"]
    G -->|Message| H["'Focus on understanding...<br/>Here are some resources...'"]
    
    D & F & H -->|Combine| I["📝 Personalized Feedback"]
    
    A -->|Add| J["Specific Examples"]
    J -->|Include| K["What was good"]
    J -->|Include| L["What could improve"]
    
    K & L -->|Enhance| I
    
    A -->|Add| M["Actionable Advice"]
    M -->|Include| N["Next Learning Topics"]
    M -->|Include| O["Practice Areas"]
    M -->|Include| P["Resource Links"]
    
    N & O & P -->|Enhance| I
    
    I -->|Format| Q["JSON Response"]
    Q -->|Include| R["feedback_text"]
    Q -->|Include| S["suggestions"]
    Q -->|Include| T["learning_resources"]
    
    R & S & T -->|Send| U["🔌 WebSocket"]
    U -->|Display| V["👤 User Feedback"]
    
    style A fill:#b3e5fc
    style I fill:#a5d6a7
    style Q fill:#81c784
    style V fill:#e1f5ff
```

## Evaluation Database Storage

```mermaid
graph TD
    A["💾 Store Evaluation Result"]
    
    A -->|Create Record| B["Evaluation Object"]
    B -->|Field| C["evaluation_id"]
    B -->|Field| D["interview_id"]
    B -->|Field| E["question_id"]
    B -->|Field| F["answer_id"]
    B -->|Field| G["score"]
    B -->|Field| H["feedback"]
    B -->|Field| I["strengths"]
    B -->|Field| J["improvements"]
    B -->|Field| K["timestamp"]
    
    C & D & E & F & G & H & I & J & K -->|Store| L["🗄️ SQLite Database"]
    
    L -->|Create Index| M["interview_id Index"]
    L -->|Create Index| N["question_id Index"]
    
    A -->|Vector| O["Store Embedding"]
    O -->|Create| P["Text Embedding"]
    P -->|Store| Q["Chroma DB"]
    
    Q -->|Enable| R["Semantic Search"]
    R -->|Query| S["Find Similar Answers"]
    
    L & Q -->|Together| T["Complete Evaluation<br/>Data Stored"]
    
    style A fill:#b3e5fc
    style B fill:#fff3e0
    style L fill:#a5d6a7
    style Q fill:#81c784
    style T fill:#66bb6a
```

## Quality Assurance in Evaluation

```mermaid
graph TD
    A["🔍 QA Check"]
    
    A -->|Verify| B["Score Validity"]
    B -->|Check| C{0.0 - 10.0?}
    C -->|No| D["Clamp to Range"]
    C -->|Yes| E["✅ Valid"]
    
    A -->|Verify| F["Feedback Content"]
    F -->|Check| G{Not Empty?}
    G -->|No| H["Generate Default"]
    G -->|Yes| I["✅ Valid"]
    
    A -->|Verify| J["Strengths Count"]
    J -->|Check| K{1-5 Items?}
    K -->|No| L["Adjust Count"]
    K -->|Yes| M["✅ Valid"]
    
    A -->|Verify| N["Improvements Count"]
    N -->|Check| O{1-3 Items?}
    O -->|No| P["Adjust Count"]
    O -->|Yes| Q["✅ Valid"]
    
    D & E & I & M & Q -->|If All Pass| R["✅ Evaluation Approved"]
    
    R -->|Send| S["🔌 WebSocket"]
    S -->|Store| T["💾 Database"]
    
    style A fill:#b3e5fc
    style R fill:#a5d6a7
    style B fill:#ffecb3
    style F fill:#ffecb3
    style J fill:#ffecb3
    style N fill:#ffecb3
```

---

## Notes

- Evaluations are stored immediately for data persistence
- Scores are normalized to 0-10 scale for consistency
- Feedback is personalized based on score level
- Multiple evaluations aggregated for final report
- Vector embeddings enable semantic search and analytics

