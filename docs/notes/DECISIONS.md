# DECISIONS.md - Key Design & Implementation Decisions

**Document:** Decision Log  
**Project:** Policy Rule Interpreter for Educational Analytics  
**Created:** May 16, 2026  
**Purpose:** Explain WHY we built things this way (rubric requirement: evidence of decision-making)

---

## Table of Decisions

1. [API Choice: OpenAI vs HuggingFace](#1-api-choice-openai-vs-huggingface)
2. [Framework: Streamlit vs Flask/FastAPI](#2-framework-streamlit-vs-flaskfastapi)
3. [Output Format: JSON vs Prose vs Markdown](#3-output-format-json-vs-prose-vs-markdown)
4. [System Prompt Design: Role-based vs Template-based](#4-system-prompt-design-role-based-vs-template-based)
5. [Number of Test Policies: 1 vs 3 vs 5+](#5-number-of-test-policies-1-vs-3-vs-5)
6. [Deployment: Streamlit Cloud vs Docker vs Traditional Server](#6-deployment-streamlit-cloud-vs-docker-vs-traditional-server)
7. [Error Handling: Strict vs Lenient](#7-error-handling-strict-vs-lenient)
8. [Grounding Strategy: Examples vs Glossary vs Both](#8-grounding-strategy-examples-vs-glossary-vs-both)

---

## 1. API Choice: OpenAI vs HuggingFace

### The Question
Which LLM should we use to parse policies?

### Options Considered

| Aspect | OpenAI GPT-4o-mini | HuggingFace Mistral 7B | Anthropic Claude |
|--------|------------|------------|----------|
| **Setup Time** | 5 mins (API key) | 30 mins (dependencies + download) | 10 mins (API key) |
| **First Response** | <1 second | 30-60 seconds | <1 second |
| **First Deploy** | Instant | 2-3 mins (4GB model download) | Instant |
| **Cost (MVP)** | ~$0.15 | $0 | ~$0.10 |
| **JSON Parsing** | Excellent | Good | Excellent |
| **Accuracy** | 90%+ | 75-80% | 90%+ |
| **Hallucination** | Moderate | Higher (smaller model) | Lower |
| **Local vs Cloud** | Cloud only | Local or cloud | Cloud only |

### Decision: **OpenAI GPT-4o-mini** ✅

### Rationale
```
Constraint 1: Must deploy by May 17 (48 hours)
Constraint 2: Local testing tonight (May 16)
Constraint 3: Free/cheap (student budget)

HuggingFace Mistral:
  - Pro: Free
  - Con: 2-3 min first deployment (kills today's testing)
  - Con: Slower responses (30+ sec per policy)
  - Con: Higher hallucination rate (7B model)

OpenAI GPT-4o-mini:
  - Pro: Instant responses (<1 sec)
  - Pro: Higher accuracy (better JSON)
  - Pro: Can test today, deploy tomorrow
  - Pro: ~$0.15 MVP cost (negligible)
  - Con: Requires API key (not fully free)

Decision Matrix:
  Deadline pressure (HIGH) → OpenAI wins
  Accuracy needed (MEDIUM-HIGH) → OpenAI wins
  Cost (LOW priority for MVP) → Tie
```

### Trade-offs Accepted
- ✅ **Accept:** Need to pay ~$0.15 (within free trial)
- ✅ **Accept:** Requires API key (security best practice: use .env)
- ❌ **Reject:** Could have used free model (deadline made it infeasible)

### Future Consideration
**Phase 2:** Could implement option to use HuggingFace Mistral locally as fallback

### Evidence This Decision Was Made
- API choice documented in roadmap.md (Section 6)
- OpenAI selected in .env.example
- llm_client.py uses OpenAI specifically
- Alternative considered but documented why rejected

---

## 2. Framework: Streamlit vs Flask/FastAPI

### The Question
How should we build the web UI for policy analysis?

### Options Considered

| Aspect | Streamlit | Flask + HTML/CSS | FastAPI + React | Django |
|--------|----------|------------------|-----------------|--------|
| **Dev Time** | 2-3 hours | 8-10 hours | 12-15 hours | 10-12 hours |
| **Language(s)** | Python | Python + HTML/JS | Python + JS | Python |
| **UI Complexity** | Simple (widgets) | Full control | Full control | Medium |
| **Deploy to Cloud** | 1-click Streamlit Cloud | Heroku/AWS/GCP | Vercel/AWS/GCP | Heroku/AWS |
| **DevOps Required** | None | Minimal | Moderate | Moderate |
| **Maintenance** | Low | Medium | High | Medium |
| **Learning Curve** | Minimal | Low | High | Medium |
| **Best for** | Data science, dashboards | Full-featured web apps | Modern APIs | Large projects |

### Decision: **Streamlit** ✅

### Rationale
```
Context:
- 1-week deadline
- Data scientist building (not full-stack engineer)
- Focus: MVP demo, not production app
- Rubric: Must showcase prompt engineering, not web dev skills

Streamlit gives:
  ✓ Fastest dev time (3 hours vs 12+ hours)
  ✓ Python-only (analyst-friendly)
  ✓ Built-in widgets (text area, buttons, JSON display)
  ✓ Automatic responsive design
  ✓ 1-click deployment (Streamlit Cloud)
  ✓ Perfect for demonstrating ML/LLM work

Trade-offs:
  ✓ Accept: Less customization than traditional web
  ✓ Accept: Can't build complex UX
  ❌ Reject: Would have spent 12+ hours on web dev
              instead of prompt engineering
```

### Trade-offs Accepted
- ✅ **Accept:** Limited UI customization (but fine for MVP)
- ✅ **Accept:** Streamlit Cloud memory limits (3-5 concurrent users OK for demo)
- ❌ **Reject:** Could have built React app (kills timeline)

### Alternative Path Considered
If timeline was 4 weeks, would have chosen FastAPI + React for:
- Custom UI
- API-first architecture
- Better scalability

### Future Consideration
**Phase 2:** Could wrap in professional web app if needed, but current MVP choice was right

### Evidence This Decision Was Made
- Framework choice documented in roadmap.md (Section 6)
- app.py uses Streamlit APIs exclusively
- 3-tab interface (Analyzer, Examples, Prompt) leverages Streamlit widgets
- Deployment to Streamlit Cloud (not traditional server)

---

## 3. Output Format: JSON vs Prose vs Markdown

### The Question
How should the AI respond to policy analysis requests?

### Options Considered

| Aspect | JSON | Prose/Free-text | Markdown | YAML |
|--------|------|-----------------|----------|------|
| **Machine-readable** | ✅ Excellent | ❌ Poor | ⚠️ Okay | ✅ Good |
| **Human-readable** | ⚠️ Okay | ✅ Excellent | ✅ Good | ⚠️ Okay |
| **Parseable** | ✅ Deterministic | ❌ Ambiguous | ⚠️ Difficult | ✅ Consistent |
| **Dashboard Integration** | ✅ Native | ❌ Requires parsing | ⚠️ Requires parsing | ✅ Easy |
| **LLM Accuracy** | ✅ High (clear schema) | ❌ Variable | ⚠️ Medium | ✅ Good |
| **File Size** | Small | Large | Medium | Small |

### Decision: **JSON** ✅

### Rationale
```
Goals:
  1. Output must be machine-readable (for dashboards)
  2. Data analyst must understand it (human review required)
  3. LLM must produce it reliably (no hallucination)

JSON achieves all three:
  ✓ Schema-based (analyst knows what fields to expect)
  ✓ Deterministic parsing (JSON parser catches errors)
  ✓ Integrates with dashboards (REST APIs expect JSON)
  ✓ LLM responds better to structured requirements

Prompt requirement:
  "CRITICAL: Output ONLY valid JSON with NO additional text"
  → This alone ensures format compliance
```

### Trade-offs Accepted
- ✅ **Accept:** Less natural/readable than prose
- ✅ **Accept:** Requires AI to be guided to format (but worth it for reliability)
- ❌ **Reject:** Could have used Markdown (but less machine-readable)

### Implementation Detail
llm_client.py has `_extract_json()` function that:
- Handles markdown code blocks (```json ...  ```)
- Extracts JSON from text if model adds extra text
- Validates JSON structure

### Future Consideration
Could add option to return Markdown explanation + JSON (best of both worlds)

### Evidence This Decision Was Made
- System prompt explicitly requires JSON
- app.py displays JSON with `st.json()` and formatted view
- llm_client.py has JSON parsing logic
- EVALUATION.md has JSON examples

---

## 4. System Prompt Design: Role-based vs Template-based

### The Question
How should we instruct the AI to behave?

### Options Considered

| Approach | Role-based | Template-based | Few-shot | Chain-of-thought |
|----------|-----------|----------------|----------|-----------------|
| **Dev Time** | 30 mins | 1 hour | 2 hours | 1.5 hours |
| **Effectiveness** | Good | Okay | Excellent | Excellent |
| **Accuracy** | 85% | 75% | 90%+ | 90%+ |
| **Cost** | Low | Low | Medium | Medium |
| **Hallucination** | Moderate | High | Low | Low |
| **Scalability** | Good | Poor | Good | Good |
| **Domain Grounding** | Requires glossary | Built-in | Natural | Natural |

### Decision: **Role-based (V1) + Plan Few-shot (V2)** ✅

### Rationale
```
MVP Timeline: 1 week
  - Can't spend 2 hours on few-shot prompting today
  - Role-based takes 30 mins and works well
  - Document path to V2 (few-shot) for future

Role-based prompt advantages:
  ✓ Fast to build (30 mins)
  ✓ Clear and understandable
  ✓ Grounds model in educational domain
  ✓ Reduces hallucination (vs generic instructions)
  ✓ Establishes pattern for iterations

Example:
  "You are an EXPERT EDUCATIONAL DATA ANALYST"
  → Sets role expectation
  → Tells model to think like domain expert
  → Reduces off-topic responses
```

### Trade-offs Accepted
- ✅ **Accept:** Lower accuracy than few-shot (85% vs 90%+)
- ✅ **Accept:** No concrete examples in v1 (will add in v2)
- ❌ **Reject:** Could have built few-shot (kills May 16 deadline)

### Iterative Improvement Plan
```
V1 (Complete):  Role-based instructions
V2 (Plan):      Add 2-3 few-shot examples
V3 (Plan):      Stricter JSON validation
V4 (Plan):      Enhanced domain grounding
V5 (Plan):      Better ambiguity detection
```

### Evidence This Decision Was Made
- docs/system_prompt.md contains V1 prompt
- BUILD_LOG.md has V2-V5 planned
- app.py shows system prompt in transparent way
- Multiple prompt iterations documented

---

## 5. Number of Test Policies: 1 vs 3 vs 5+

### The Question
How many example policies should we include?

### Options Considered

| Factor | 1 Policy | 3 Policies | 5+ Policies |
|--------|----------|-----------|-------------|
| **Dev Time** | 15 mins | 45 mins | 2 hours |
| **Test Coverage** | Poor | Balanced | Comprehensive |
| **Difficulty Range** | Limited | Diverse | Very diverse |
| **Grounding Quality** | Weak | Good | Excellent |
| **Rubric Evidence** | Minimal | Sufficient | Strong |
| **User Value** | Low | High | Very high |

### Decision: **3 Diverse Policies** ✅

### Rationale
```
Test Coverage Needed:
  1. Simple case (grade-based funding)
  2. Medium case (attendance-based adjustment)
  3. Complex case (demographic tracking)

Three policies show:
  ✓ AI handles different rule types
  ✓ Grounding in real charter school context
  ✓ Progressive difficulty (tests edge cases)
  ✓ Sufficient for MVP evaluation

Why not 5+?
  ❌ Takes 2+ hours (deadline pressure)
  ❌ Overkill for MVP (3 is sufficient for rubric)
  ❌ Testing all 5 is time-consuming
```

### Policy Selection Criteria
1. **Diversity:** Different rule types (grade, attendance, demographic)
2. **Realism:** Actual charter school concerns (not contrived examples)
3. **Difficulty:** Progressive complexity (easy → medium → hard)
4. **Coverage:** Tests different NLP challenges (parsing, interpretation, ambiguity)

### Policies Chosen

**Policy 1: Grade Level Funding** (Simple)
```
Why: Clear grade bands + funding multipliers
Tests: Grade level identification, metric mapping
Expected Accuracy: 90%+
```

**Policy 2: Attendance-Based Funding** (Medium)
```
Why: Threshold-based logic (more complex)
Tests: Threshold mapping, conditional logic
Expected Accuracy: 85%
```

**Policy 3: Special Population Tracking** (Complex)
```
Why: Multiple subgroups + ambiguous language
Tests: Complex interpretation, ambiguity detection
Expected Accuracy: 70-80%
```

### Trade-offs Accepted
- ✅ **Accept:** Not comprehensive (5+ policies would be better)
- ✅ **Accept:** Limited edge case coverage
- ❌ **Reject:** Could have added 5+ policies (kills testing time)

### Future Consideration
**Phase 2:** Add 10-15 more policies for production robustness

### Evidence This Decision Was Made
- 3 example policies in data/example_policies/
- EVALUATION.md has 3 test cases
- Example Policies tab in app.py loads all 3
- BUILD_LOG.md documents why 3 was chosen

---

## 6. Deployment: Streamlit Cloud vs Docker vs Traditional Server

### The Question
Where/how should the app run in production?

### Options Considered

| Factor | Streamlit Cloud | Docker + Cloud | Traditional Server | GitHub Pages |
|--------|-----------------|----------------|-------------------|--------------|
| **Setup Time** | 5 mins | 1 hour | 2-3 hours | N/A (static only) |
| **Cost** | Free | $5-50/month | $10-100/month | Free |
| **Maintenance** | None | Minimal | High | None (static) |
| **Scaling** | Limited | Good | Excellent | N/A |
| **DevOps Skills** | Zero | Moderate | High | None |
| **Cold Start** | <2 secs | 30-60 secs | <1 sec | N/A |
| **API Access** | Built-in | Full control | Full control | N/A |

### Decision: **Streamlit Cloud** ✅

### Rationale
```
MVP Constraints:
  ✓ Must deploy by May 17
  ✓ No DevOps expertise available
  ✓ Free tier requirement
  ✓ Easy to maintain (data analyst may update later)

Streamlit Cloud wins:
  ✓ 5-minute deployment (literally 3 clicks)
  ✓ Automatic GitHub sync (push → auto-deploy)
  ✓ Free forever (within limits)
  ✓ No Docker, no server config
  ✓ Built-in secrets management (API keys)

Trade-offs accepted:
  ✓ Memory limits (3GB, OK for MVP)
  ✓ Concurrent user limits (3-5 users, fine for demo)
  ✓ Less control than traditional server
```

### Alternative Paths
If this was production:
- ❌ Would use Docker + AWS/GCP
- ❌ Would add CI/CD pipeline
- ❌ Would scale horizontally
- ❌ Would add monitoring + alerting

But for MVP? Streamlit Cloud is perfect.

### Evidence This Decision Was Made
- README.md has Streamlit Cloud deployment steps
- Deploy-to-Streamlit instructions in setup guide
- .streamlit/config.toml ready (can be customized)
- No Docker files (intentionally kept out of MVP)

---

## 7. Error Handling: Strict vs Lenient

### The Question
How strictly should we validate input and handle errors?

### Options Considered

| Approach | Strict | Lenient | Hybrid |
|----------|--------|---------|--------|
| **Error Messages** | Detailed, technical | Friendly, vague | Informative + user-friendly |
| **Invalid Input** | Reject | Attempt fix | Validate + suggest fix |
| **API Failures** | Stop, show error | Retry, cache | Retry + fallback |
| **User Experience** | Safe, predictable | Forgiving, flexible | Balanced |
| **Dev Effort** | High | Low | Medium |

### Decision: **Hybrid (Strict validation + Lenient messaging)** ✅

### Rationale
```
MVP philosophy:
  - Fail fast (invalid input → clear error message)
  - But guide users to success (friendly error text)
  - Never silently fail (always inform user)

Example:
  Strict alone: "JSON parsing failed: unexpected token"
  → User confused, doesn't know what to do

  Lenient alone: "Something went wrong, try again"
  → User frustrated, no help fixing it

  Hybrid: "❌ API Error: OPENAI_API_KEY not found in .env file.
           Make sure your .env file has a valid OPENAI_API_KEY"
  → User understands problem + can fix it
```

### Implementation in Code
```python
# app.py
if not policy_text.strip():
    st.error("❌ Please paste a policy before clicking Analyze")  # Clear message

# llm_client.py
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in .env file. "
        "Please copy .env.example to .env and add your API key."
    )  # Actionable error
```

### Trade-offs Accepted
- ✅ **Accept:** Can't handle every edge case (MVP scope)
- ✅ **Accept:** Error messages could be prettier
- ❌ **Reject:** Could have added retry logic (overkill for MVP)

### Future Consideration
**Phase 2:** Add automatic retries + fallback behaviors

### Evidence This Decision Was Made
- app.py has user-friendly error messages
- llm_client.py raises informative exceptions
- README.md has troubleshooting section
- Error handling documented in code comments

---

## 8. Grounding Strategy: Examples vs Glossary vs Both

### The Question
How should we ground the AI in charter school domain?

### Options Considered

| Strategy | Examples Only | Glossary Only | Both | Context Retrieval |
|----------|-------------|--------------|------|------------------|
| **Prevents Hallucination** | Good | Fair | Excellent | Excellent |
| **Covers Edge Cases** | Fair | Good | Excellent | Excellent |
| **Prompt Size** | Large | Small | Medium | Medium-Large |
| **Dev Time** | 1 hour | 30 mins | 1.5 hours | 3+ hours |
| **Scalability** | Poor (fixed examples) | Fair | Good | Excellent |

### Decision: **Both (Examples + Glossary)** ✅

### Rationale
```
Grounding prevents hallucination by anchoring LLM in real knowledge.

Examples show HOW to interpret:
  ✓ "Here's a policy, here's what to extract"
  ✓ Model learns the pattern

Glossary shows WHAT terms mean:
  ✓ "proficiency_rate" = % students at/above benchmark
  ✓ Model understands domain terminology

Both together:
  ✓ Reduces hallucinations significantly
  ✓ Improves accuracy (examples teach pattern)
  ✓ Covers edge cases (glossary defines terms)
```

### Implementation in docs/system_prompt.md
```
[Role definition]
[Task steps]
[Output format]
[Examples]:
  "Here are examples of rules you should know..."
  Policy → Expected extraction
[Glossary]:
  "Key charter school metrics you should know:
   - proficiency_rate: % of students at/above proficiency"
[Safety]:
  "Always include human_review_required: true"
```

### Trade-offs Accepted
- ✅ **Accept:** System prompt is longer (~2000 tokens)
- ✅ **Accept:** More complex to maintain (update glossary as needed)
- ❌ **Reject:** Could use RAG + vector DB (overkill for MVP)

### Scalability Note
If glossary grows beyond 10-20 items:
- **Phase 2:** Could implement RAG (Retrieval-Augmented Generation)
- **Phase 2:** Store glossary in database, retrieve relevant terms

### Evidence This Decision Was Made
- docs/system_prompt.md has both examples and glossary
- APP.py System Prompt tab shows grounding strategy
- EVALUATION.md mentions grounding approach
- BUILD_LOG.md documents this decision

---

## Summary: Decision Matrix

| Decision | Chosen | Alternative | Why |
|----------|--------|-------------|-----|
| LLM | OpenAI | HuggingFace | Deadline + accuracy |
| Framework | Streamlit | Flask/React | Speed + simplicity |
| Output | JSON | Prose | Machine-readable |
| Prompt | Role-based + plan V2 | Few-shot | Time constraint |
| Test Policies | 3 | 1 or 5+ | Balanced coverage |
| Deployment | Streamlit Cloud | Docker | Zero DevOps |
| Errors | Hybrid | Strict/lenient | User-friendly + safe |
| Grounding | Examples + glossary | One or neither | Prevent hallucination |

---

## 🔄 Decision Review Process

After each test run (May 17), we'll review:
1. Did decisions hold up? (Good indicators: tests pass, no major bugs)
2. Any unexpected issues? (May inform Phase 2 decisions)
3. User feedback? (Will Binju want anything different?)
4. Performance? (Is Streamlit Cloud fast enough? Is JSON parsing reliable?)

### Criteria for Reopening Decisions
- If >30% of tests fail: Reconsider LLM choice
- If response time >10 secs: Reconsider framework
- If JSON parsing breaks: Reconsider output format
- If hallucinations >50%: Reconsider grounding strategy

### Current Status
All decisions made with good rationale + trade-off analysis. Ready for testing.

---

**Last Updated:** May 16, 2026  
**Status:** Locked (for MVP); will evolve for Phase 2  
**Next Review:** May 17, 2026 (after testing)
