# ARCHITECTURE.md - System Design & Data Flow

**Document:** System Architecture  
**Project:** Policy Rule Interpreter for Educational Analytics  
**Created:** May 16, 2026  
**Purpose:** Explain HOW the system works (for understanding + maintainability)

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    POLICY RULE INTERPRETER                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐        ┌──────────────────┐        ┌────────────────┐
│   User Browser   │◄──────►│  Streamlit App   │◄──────►│  OpenAI API    │
│                  │        │  (Python)        │        │  (Cloud)       │
└──────────────────┘        └──────────────────┘        └────────────────┘
     HTTP                    Process policy             Parse + analyze
   Requests                  Display UI                 Return JSON


                    ┌─────────────────────────┐
                    │  Local File System      │
                    │ - .env (secrets)        │
                    │ - system_prompt.md      │
                    │ - example_policies/     │
                    └─────────────────────────┘
                          Read at startup
```

---

## 📦 Component Breakdown

### 1. Frontend: Streamlit UI (`app.py`)

**Responsibilities:**
- Render web interface
- Accept policy text from user
- Call LLM via llm_client.py
- Display results (JSON + formatted view)
- Show example policies
- Display system prompt (transparency)

**Key Components:**

```
app.py
├── Page Config
│   └── Set page title, layout, icon
├── Header & Sidebar
│   └── Project overview, setup instructions, rubric checklist
├── Tab 1: Analyzer
│   ├── Text input (policy text area)
│   ├── Submit button
│   ├── Loading spinner
│   ├── JSON output display
│   ├── Expandable breakdown (rule, grades, metrics, etc.)
│   ├── Download button (results as JSON)
│   └── Human review warning
├── Tab 2: Example Policies
│   ├── Load and display 3 example policies
│   └── Copy-to-analyzer buttons
└── Tab 3: System Prompt
    ├── Display current prompt (read-only)
    └── Explain prompt engineering techniques
```

**Technology:** Streamlit 1.28.0

**Why Streamlit?**
- Built-in widgets for forms, JSON display, buttons
- Automatic responsive UI
- Hot reload during development
- One-click deployment to Streamlit Cloud
- Perfect for data scientist-built tools

---

### 2. LLM Client: OpenAI Integration (`llm_client.py`)

**Responsibilities:**
- Load environment variables (API key)
- Load system prompt from file
- Initialize OpenAI client
- Send policy + system prompt to API
- Parse JSON response (error handling)
- Return structured data to app.py

**Key Functions:**

```
llm_client.py
├── PolicyAnalyzer class
│   ├── __init__()
│   │   ├── Load OPENAI_API_KEY from .env
│   │   ├── Load OPENAI_MODEL from .env
│   │   ├── Load system prompt from docs/system_prompt.md
│   │   └── Initialize OpenAI client
│   ├── analyze_policy(policy_text: str) → dict
│   │   ├── Create chat message [system, user]
│   │   ├── Call OpenAI API (temperature=0.3 for consistency)
│   │   ├── Extract response text
│   │   ├── Call _extract_json() for parsing
│   │   └── Return parsed dict or raise error
│   └── _extract_json(text: str) → dict
│       ├── Find first { and last } in text
│       ├── Extract substring
│       └── Parse as JSON (handles markdown code blocks)
```

**Technology:** OpenAI Python SDK v1.3.0

**Why OpenAI?**
- Reliable JSON parsing (GPT-4 handles structured output well)
- Fast responses (<1 sec)
- Affordable for MVP ($0.15 estimated cost)
- Production-ready API

---

### 3. System Prompt: Domain Instructions (`docs/system_prompt.md`)

**Responsibilities:**
- Tell the AI how to behave
- Define output format
- Ground in charter school domain
- Enforce safety guardrails

**Structure:**

```
docs/system_prompt.md
├── Role Definition
│   └── "You are an expert educational data analyst..."
├── Task Specification
│   ├── Step 1: Identify what changed
│   ├── Step 2: Extract affected data elements
│   ├── Step 3: Describe business logic
│   ├── Step 4: Suggest SQL/pseudocode
│   └── Step 5: Flag ambiguities
├── Output Format (JSON)
│   ├── rule_summary
│   ├── grade_levels
│   ├── affected_metrics
│   ├── business_logic_summary
│   ├── suggested_sql_update
│   ├── ambiguities
│   ├── confidence
│   └── human_review_required
├── Domain Context (Glossary)
│   ├── Key metrics: proficiency, attendance, graduation, funding
│   ├── Grade levels: K, 1-2, 3-5, 6-8, 9-12
│   └── Population categories: ELL, IEP, FRL
└── Safety Constraints
    └── "ALWAYS include human_review_required: true"
```

**Why This Structure?**
- Role definition grounds model in correct domain
- Explicit steps reduce hallucination
- JSON format ensures deterministic output
- Glossary prevents inventing metrics
- Safety reminder ensures compliance

---

### 4. Example Policies: Ground Truth (`data/example_policies/`)

**Responsibilities:**
- Provide realistic test cases
- Ground AI in actual charter school policies
- Show what "good" analysis looks like

**Structure:**

```
data/example_policies/
├── policy_1_grade_levels.txt
│   └── Grade-based funding rule (simple case)
├── policy_2_attendance_funding.txt
│   └── Attendance-based adjustment (medium case)
└── policy_3_demographics.txt
    └── Special population tracking (complex case)
```

**Usage:**
- Loaded in app.py (Tab 2: Example Policies)
- User can copy/paste for testing
- Ground the system prompt (shows domain examples)
- Serve as test cases (EVALUATION.md)

---

## 🔄 Data Flow: Policy → Analysis → Output

### Sequence 1: User Submits Policy

```
1. User opens http://localhost:8501
   ├─ Streamlit loads app.py
   ├─ Reads system_prompt.md from disk
   ├─ Loads example policies from data/example_policies/
   └─ Renders UI

2. User enters policy text in text area
   └─ Text stored in Streamlit session state

3. User clicks "Analyze Policy" button
   └─ Triggers analyze_button action
```

### Sequence 2: Processing Pipeline

```
1. app.py validates input
   └─ If empty: Show error "Please paste a policy"
   └─ If valid: Proceed to next step

2. app.py instantiates PolicyAnalyzer
   ├─ Reads .env file
   ├─ Loads OPENAI_API_KEY
   ├─ Loads OPENAI_MODEL
   └─ Loads system_prompt.md

3. app.py calls analyzer.analyze_policy(policy_text)
   ├─ llm_client creates OpenAI message
   │   ├─ system: Load system_prompt.md
   │   └─ user: The policy text
   └─ API call sent to OpenAI:
       POST https://api.openai.com/v1/chat/completions
       {
         "model": "gpt-4o-mini",
         "temperature": 0.3,
         "max_tokens": 500,
         "messages": [
           {"role": "system", "content": "<system_prompt>"},
           {"role": "user", "content": "<policy_text>"}
         ]
       }

4. OpenAI returns response (usually 2-5 seconds)
   └─ Response text contains JSON object

5. llm_client._extract_json() parses response
   ├─ Find first { and last }
   ├─ Extract substring
   ├─ Parse as JSON
   └─ Return dict or raise error

6. app.py receives dict
   └─ {
        "rule_summary": "...",
        "grade_levels": [...],
        "affected_metrics": [...],
        "business_logic_summary": "...",
        "suggested_sql_update": "...",
        "ambiguities": [...],
        "confidence": "high/medium/low",
        "human_review_required": true
      }

7. app.py displays result
   ├─ st.json(result) - Full JSON display
   ├─ Expandable sections for each field
   ├─ Download button (export as JSON)
   └─ Human review warning (IMPORTANT)
```

### Sequence 3: User Actions with Results

```
User can:
├─ View full JSON
├─ View expanded breakdown (rule, grades, metrics, etc.)
├─ Download JSON file
├─ Copy policy to try again
├─ View system prompt (understand how AI was instructed)
└─ Generate new analysis with different policy
```

---

## 📊 Data Structures

### Input: Policy Text
```
Type: String (plain text)
Example:
  "Starting 2024-25, Grade 6-8 students count toward funding
   if they score at/above proficiency on state assessments."
```

### System Prompt: Instructions
```
Type: String (markdown file)
Location: docs/system_prompt.md
Size: ~2000 tokens
Purpose: Tell AI how to behave (role, task, format, constraints)
```

### Output: Parsed Analysis
```
Type: JSON dict
Schema:
{
  "rule_summary": string,              # 1-sentence summary
  "grade_levels": string[],            # ["K-2", "3-5", "6-8", "9-12"]
  "affected_metrics": string[],        # ["proficiency", "funding"]
  "business_logic_summary": string,    # 1-2 sentences explaining impact
  "suggested_sql_update": string,      # SQL or pseudocode suggestion
  "ambiguities": string[],             # List of unclear points
  "confidence": "high" | "medium" | "low",
  "human_review_required": true
}
```

---

## 🔐 Security & Environment

### Secrets Management

```
.env (local, never committed)
├── OPENAI_API_KEY = "sk-..."
└── OPENAI_MODEL = "gpt-4o-mini"

.env.example (template, safe to commit)
├── OPENAI_API_KEY = "sk-your-api-key-here"
└── OPENAI_MODEL = "gpt-4o-mini"

.gitignore (prevents accidental commits)
├── .env
├── venv/
├── __pycache__/
└── .streamlit/
```

### API Key Protection

**Local:**
```
1. User copies .env.example to .env
2. Adds actual OpenAI API key
3. Python's python-dotenv loads it at runtime
4. Never exposed in code or logs
```

**Streamlit Cloud:**
```
1. User deploys to Streamlit Cloud
2. Adds OPENAI_API_KEY as "Secret" in settings
3. Streamlit Cloud encrypts + injects at runtime
4. Never visible in GitHub or logs
```

---

## 🚀 Deployment Architecture

### Local Development

```
Developer Machine
├── Git repo (local)
├── Python venv (isolated environment)
├── .env (local secrets)
├── app.py + llm_client.py (running)
└── Browser (http://localhost:8501)
```

### Production: Streamlit Cloud

```
GitHub Repository (Source of Truth)
├── all code files
├── all docs files
└── .gitignore (keeps secrets out)
       ↓
    GitHub Webhook Triggered
       ↓
Streamlit Cloud (Container)
├── Clones repo
├── Installs requirements.txt
├── Injects OPENAI_API_KEY secret
├── Starts Streamlit server
└── Public URL: https://policy-rule-interpreter.streamlit.app
       ↓
User Browser (anywhere)
└── Accesses public URL, uses app
```

### File Locations in Streamlit Cloud

```
Container filesystem:
/app/
├── app.py
├── llm_client.py
├── requirements.txt
├── .env (injected from secrets)
├── docs/
│   ├── system_prompt.md
│   └── prompts/
├── data/
│   └── example_policies/
└── (other files)
```

---

## 📈 Performance Characteristics

### Response Times

```
Local Machine (WSL2 + RTX GPU):
├── App startup: ~2 seconds
├── First policy analysis: ~5 seconds (1st API call)
├── Subsequent analyses: ~3-5 seconds
└── JSON parsing: <100ms

Streamlit Cloud (First Deploy):
├── App startup: ~10 seconds (cold start)
├── First policy analysis: ~5-7 seconds
└── Subsequent analyses: ~3-5 seconds
```

### Resource Usage

```
Memory:
├── Streamlit process: ~300-500 MB
├── Python + libraries: ~200 MB
├── Per-user session: ~50 MB
└── Streamlit Cloud limit: 3 GB (plenty)

Storage:
├── Code + docs: ~500 KB
├── Models (local): None (uses OpenAI API)
├── Cache: None (stateless)
└── Database: None (MVP doesn't persist)
```

---

## 🔄 State Management

### Session State (Per User)
```python
st.session_state:
├── policy_text: str (current input)
├── analysis_result: dict (last JSON output)
└── (Streamlit auto-manages, no persistence)
```

### No Persistence
- Responses not saved to database
- User closes browser → state lost
- Each analysis is independent
- Perfect for MVP (simplicity)

### Future: Phase 2 Persistence
```
Could add:
├── SQLite database (local file)
├── PostgreSQL (cloud)
├── Audit log (who analyzed what, when)
└── History view (see past analyses)
```

---

## 🧪 Testing Architecture

### Unit Testing (Not in MVP, but designed for)

```
Could test:
├── llm_client.py
│   ├── _extract_json() function
│   ├── Error handling (invalid API key)
│   └── Timeout handling
├── System prompt quality
│   ├── Does it produce valid JSON?
│   ├── Does it identify grade levels?
│   └── Does it hallucinate?
└── UI validation (Streamlit doesn't unit-test well)
```

### Integration Testing (Manual, in MVP)

```
EVALUATION.md:
├── Test Case 1: Policy 1 (grade levels)
├── Test Case 2: Policy 2 (attendance)
└── Test Case 3: Policy 3 (demographics)

Scoring:
├── Grade levels identified: 20 pts
├── Metrics identified: 20 pts
├── Business logic: 20 pts
├── SQL suggestion: 20 pts
├── Ambiguities flagged: 10 pts
└── Total: 100 pts (90% = excellent)
```

---

## 📚 System Constraints & Limits

### Design Constraints
```
├── 1-week MVP timeline (no time for over-engineering)
├── Data analyst as user (not software engineer)
├── Budget constraint (~$0-5 for API)
└── Free hosting (Streamlit Cloud)
```

### Runtime Constraints
```
├── API response time: 3-7 seconds (user acceptable)
├── Memory: 3 GB limit (plenty for MVP)
├── Concurrent users: 3-5 (for demo)
├── Input size: No limit (but >10K chars gets slow)
└── Session duration: ~30 mins (Streamlit default)
```

### Functional Constraints
```
├── Text policies only (no PDF/Word parsing)
├── English language only
├── No real-time updates
├── No database persistence
├── No multi-user collaboration
└── No audit logging (Phase 2)
```

---

## 🎯 Why This Architecture?

### Simplicity
- Minimal components (Streamlit + LLM + files)
- No databases, queues, caching layers
- Perfect for 1-week MVP

### Maintainability
- Single Python codebase
- Easy for data analyst to update
- System prompt separated (easy to iterate)

### Deployment
- One-click to Streamlit Cloud
- Automatic GitHub sync
- No DevOps needed

### Extensibility
- Can add database (Phase 2)
- Can add authentication (Phase 2)
- Can add PDF parsing (Phase 2)
- Can add API endpoint (Phase 2)

---

## 📋 Component Checklist

- ✅ app.py (Streamlit UI)
- ✅ llm_client.py (OpenAI integration)
- ✅ system_prompt.md (Domain instructions)
- ✅ example_policies/ (Test cases + grounding)
- ✅ requirements.txt (Dependencies)
- ✅ .env.example (Secrets template)
- ✅ .gitignore (Security)
- ❌ Database (Phase 2)
- ❌ Authentication (Phase 2)
- ❌ PDF parsing (Phase 2)
- ❌ API endpoint (Phase 2)

---

**Last Updated:** May 16, 2026  
**Status:** MVP Architecture Complete  
**Next Review:** May 17, 2026 (after deployment)
