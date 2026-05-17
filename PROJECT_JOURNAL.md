# PROJECT_JOURNAL.md - Chronological Development Notes
**Project:** Policy Rule Interpreter for Educational Analytics  
**Student:** Binju Karki  
**Course:** Generative AI (Master's in Data Science & Analytics)  
**Institution:** GVSU (Grand Valley State University)

---

## 📅 Daily Progress Log

### Day 1: Wednesday, May 16, 2026

#### Morning Session: Discovery & Scoping (8:00 AM - 9:00 AM)

**Notes:**
- Met with Binju to understand pain point in Charter Schools Office role
- Problem identified: Manually updating dashboard code when policies change (tedious, error-prone, time-consuming)
- Five initial areas of interest were narrowed down through questioning
- Focus selected: **Educational analytics + policy parsing**

**Key Insights:**
- Rules arrive in Word docs and spreadsheets
- Different grade levels have different requirements
- Funding is performance-based
- Changes happen frequently but manually implemented slowly
- Data analyst (not software engineer) is the user

**Decision Made:** Use GenAI to parse policy → suggest SQL/dashboard changes

**Output:** Clear problem statement + user persona

---

#### Mid-Morning Session: Project Design (9:00 AM - 10:15 AM)

**Activities:**
1. Created comprehensive 18-section roadmap.md
2. Outlined MVP scope (1 week, beginner-friendly)
3. Made key tech stack decisions

**Tech Stack Decisions:**

| Decision | Option A | Option B | Chosen | Rationale |
|----------|----------|----------|--------|-----------|
| **LLM** | OpenAI GPT-4o-mini | HuggingFace Mistral 7B | OpenAI | Faster responses, better JSON, $0.15 cost |
| **Framework** | Streamlit | Flask/FastAPI/React | Streamlit | One-language, instant deploy, 1-click Streamlit Cloud |
| **Deployment** | Streamlit Cloud | Vercel/Docker | Streamlit Cloud | Free, automatic GitHub deploys |
| **Hosting** | Free tier | Paid | Free tier | MVP budget conscious |
| **Language** | Python | Node.js/TypeScript | Python | Data analyst friendly |

**Why These Choices:**
- **Speed:** Can deploy working app in 3 hours instead of weeks
- **Simplicity:** Single Python codebase, no DevOps
- **Cost:** ~$0 for hosting + ~$0.15 for API (MVP test)
- **Rubric:** Meets all 9 requirements with minimal overhead

---

#### Afternoon Session: MVP Implementation (1:00 PM - 4:30 PM)

**Major Activities:**

1. **Project Structure (30 mins)**
   - Created folders: docs/, data/example_policies/
   - Initialized .gitignore (security best practice)
   - Set up requirements.txt with exact versions

2. **System Prompt Engineering - V1 (1 hour)**
   - Designed role-based prompt: "expert educational data analyst"
   - Defined 6-step task: identify, extract, describe, suggest, flag, output JSON
   - Added charter school domain glossary
   - Included safety guardrails: "human_review_required": true
   - Documented prompt design decisions

   **Key Prompt Features:**
   - Explicit role definition (grounds model)
   - Numbered steps (reduces ambiguity)
   - JSON format specification (ensures parseable output)
   - Domain context (prevents hallucination)
   - Safety constraints (ethical AI reminder)

3. **LLM Integration Module (1 hour)**
   - Created llm_client.py with PolicyAnalyzer class
   - Implemented:
     - Environment variable loading (.env)
     - OpenAI API client initialization
     - System prompt loading from file
     - API call logic (temperature=0.3 for consistency)
     - JSON extraction (handles markdown code blocks)
     - Error handling with helpful messages
   - Documented with docstrings + inline comments (beginner-friendly)

4. **Streamlit Frontend (1.5 hours)**
   - Created app.py with 400+ lines
   - Implemented 3 tabs:
     - **Analyzer:** Policy input → AI analysis → JSON output
     - **Example Policies:** Pre-loaded test cases (copy/paste)
     - **System Prompt:** Transparent view of AI instructions
   - Features:
     - Text area for policy input (with placeholder)
     - Submit button with loading spinner
     - JSON display + expandable detailed breakdown
     - Download button for results
     - Critical warning: "Human review required"
     - Sidebar with setup instructions + rubric checklist

5. **Example Policies (45 mins)**
   - Created 3 realistic, diverse policy examples:
     1. **Policy 1: Grade Level Funding** (grade-based rule change)
        - 4 grade bands with different multipliers
        - Tests: grade level identification, funding metrics
     2. **Policy 2: Attendance-Based Funding** (performance adjustment)
        - 4 attendance thresholds with funding impacts
        - Tests: metric identification, threshold mapping
     3. **Policy 3: Special Population Tracking** (demographic metrics)
        - 3 subgroups (ELL, IEP, FRL) with funding impact
        - Tests: complex interpretation, ambiguity detection

   **Design Rationale:**
   - Progressive difficulty (simple → complex)
   - Real-world relevance (actual charter school concerns)
   - Diverse rule types (grade-based, attendance-based, demographic)
   - Good test coverage (will show what the model can/can't do)

6. **Documentation (1 hour)**
   - Comprehensive README.md (150+ lines)
     - Project overview + problem statement
     - Features list
     - Local setup instructions (step-by-step)
     - Tech stack explanation
     - Rubric alignment table
     - Deployment guide (Streamlit Cloud)
     - Limitations + disclaimers
   - EVALUATION.md with test case templates
   - BUILD_LOG.md (this file started)
   - Inline comments throughout code (explaining concepts)

---

#### Evening Session: Documentation & Planning (5:00 PM - 6:30 PM)

**Activities:**

1. **Documentation Structure Created**
   - BUILD_LOG.md - Prompt engineering iterations + project progress
   - PROJECT_JOURNAL.md (this file) - Chronological notes
   - docs/system_prompt.md - System prompt v1 + explanation
   - docs/prompts/ - Ready for future iterations
   - docs/notes/DECISIONS.md - Key decisions + rationale
   - docs/architecture/ - System design documentation

2. **Prompt Engineering Documentation**
   - Documented V1 baseline prompt with design goals
   - Listed 5 techniques used: role definition, task specification, JSON format, domain context, safety guardrails
   - Sketched V2-V5 improvements (few-shot, validation, grounding, ambiguity detection)
   - Explained trade-offs and expected accuracy

3. **Rubric Coverage Analysis**
   - Mapped all 9 rubric items to deliverables
   - Verified each item has evidence
   - Identified what's ready vs. in-progress
   - Status: 6/9 complete ✅ | 3/9 tomorrow (deploy + test)

4. **Testing Plan Outlined**
   - 3 test cases ready (example policies)
   - Scoring rubric defined (110 points per test)
   - Success threshold: 60%+ pass rate (MVP acceptable)
   - Test schedule: Tonight (May 16) → Tomorrow AM (results) → Tomorrow PM (submit)

---

### Day 2: Tomorrow (May 17, 2026) - Planned

#### Morning: Local Testing & Results (9:00 AM - 11:00 AM)
- [ ] Set up Python venv locally
- [ ] Install requirements.txt
- [ ] Run `streamlit run app.py`
- [ ] Test all 3 example policies
- [ ] Record results in EVALUATION.md
- [ ] Fix any bugs
- [ ] Verify rubric items 1-6 complete

#### Midday: GitHub & Deployment (11:00 AM - 12:30 PM)
- [ ] Create GitHub repo
- [ ] Make 7 meaningful commits:
  1. `init: create streamlit app structure`
  2. `docs: add system prompt v1`
  3. `feat: integrate openai api`
  4. `feat: add example policies`
  5. `test: add 3 policy test cases`
  6. `docs: add README and evaluation`
  7. `deploy: prepare for streamlit cloud`
- [ ] Push to GitHub

#### Afternoon: Streamlit Cloud Deployment (1:00 PM - 2:00 PM)
- [ ] Deploy to Streamlit Cloud
- [ ] Add OPENAI_API_KEY as secret
- [ ] Test public URL
- [ ] Document deployment steps

#### Late Afternoon: Final Submission (2:00 PM - 4:00 PM)
- [ ] Fill EVALUATION.md with test results
- [ ] Verify all 9 rubric items ✅
- [ ] Create final project summary
- [ ] Submit with:
  - GitHub repo link
  - Live demo URL
  - BUILD_LOG.md (documenting everything)
  - README.md (setup + deployment)
  - Evidence of prompt engineering

---

## 🤔 Design Decisions & Rationale

### Decision 1: OpenAI vs HuggingFace
**Context:** Need LLM for policy parsing  
**Options:**
- Option A: OpenAI GPT-4o-mini ($0.15 for MVP, instant responses)
- Option B: HuggingFace Mistral 7B (free, but 30+ seconds per response)

**Decision:** OpenAI  
**Rationale:**
- Deadline pressure: Must deploy tomorrow
- HuggingFace would have 2-3 min first deployment (model download)
- GPT-4o-mini is faster, more reliable JSON parsing
- Cost: $5 free trial covers ~33,000 test runs

**Trade-offs:**
- ✅ Pro: Faster iteration, better accuracy
- ❌ Con: Requires API key (not fully free)

**Would I choose again?** YES - Deadline made OpenAI essential

---

### Decision 2: Streamlit over Traditional Web Stack
**Context:** Need web UI for policy input/output  
**Options:**
- Option A: Streamlit (Python, 1-click deploy, instant Streamlit Cloud)
- Option B: Flask + React (more control, but 5x more complexity)
- Option C: FastAPI + Vue (professional, but overkill for MVP)

**Decision:** Streamlit  
**Rationale:**
- Single Python codebase (no JavaScript)
- Automatic responsive UI
- Built-in widgets (text area, buttons, JSON display)
- One-click deploy to Streamlit Cloud (no Docker, no environment setup)
- Perfect for 1-week MVP timeline

**Trade-offs:**
- ✅ Pro: Speed of development
- ✅ Pro: Easy for data analysts to maintain
- ❌ Con: Less customization than traditional web apps
- ❌ Con: Streamlit Cloud has memory/compute limits

**Would I choose again?** YES - Best for MVP speed

---

### Decision 3: 3 Example Policies vs More/Fewer
**Context:** Need test cases to demonstrate AI parsing capability  
**Options:**
- Option A: 1 simple policy (quick, but insufficient testing)
- Option B: 3 diverse policies (balanced, comprehensive)
- Option C: 5+ policies (thorough, but time-consuming)

**Decision:** 3 diverse policies  
**Rationale:**
- Tests progressive difficulty (simple → complex)
- Shows different rule types (grade, attendance, demographic)
- Covers different metrics (proficiency, funding, special populations)
- Achievable within 1-week timeline
- Satisfies rubric requirement for grounding

**Expected Coverage:**
- Policy 1: 90%+ pass rate (straightforward grade-based rules)
- Policy 2: 85%+ pass rate (moderate complexity, threshold mapping)
- Policy 3: 70-80% pass rate (complex, ambiguous language)

**Would I choose again?** YES - Sweet spot for MVP

---

### Decision 4: System Prompt Design (Role-based vs Template-based)
**Context:** How to instruct the AI to behave correctly?  
**Options:**
- Option A: Role-based ("You are an expert analyst")
- Option B: Template-based ("Here is the format to follow")
- Option C: Few-shot ("Here are examples")

**Decision:** Role-based (v1) + plan for few-shot (v2)  
**Rationale:**
- Role-based grounds model in domain (less hallucination)
- Fast to implement (5 mins vs. 30 mins for few-shot)
- Establishes pattern for iterations (v1 → v2 → v3)
- Clear, readable, maintainable

**Next Iteration (v2):**
- Add 2-3 concrete examples of policy → JSON
- Expected improvement: +5-10% accuracy

**Would I choose again?** YES - Pragmatic for MVP deadline

---

### Decision 5: JSON Output vs Free-text Response
**Context:** How should the AI respond?  
**Options:**
- Option A: Strict JSON (deterministic, parseable, structured)
- Option B: Free-text prose (flexible, natural)
- Option C: Markdown (readable, semi-structured)

**Decision:** Strict JSON  
**Rationale:**
- Machine-readable (can be piped to other systems)
- Deterministic (same input usually = same fields)
- Validates data integrity (JSON parsers catch errors)
- Easier to integrate with dashboards
- Clear output contract (defined schema)

**Trade-offs:**
- ✅ Pro: Reliability, machine-readability
- ❌ Con: Slightly less natural/readable
- ❌ Con: Model must be guided to format correctly

**Implementation:**
- System prompt includes "CRITICAL: Output ONLY valid JSON"
- llm_client.py has JSON extraction logic (handles markdown)
- Error messages if JSON is invalid

**Would I choose again?** YES - Essential for dashboard integration

---

## 🎯 Success Criteria Met So Far

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Real problem identified | ✅ | Policy change friction documented |
| User interviewed | ✅ | Binju's pain points captured |
| MVP scoped for 1 week | ✅ | 12-15 hour estimate viable |
| Tech stack chosen | ✅ | Python + Streamlit + OpenAI |
| Code written | ✅ | 9 files, 500+ lines total |
| Prompts engineered | ✅ | V1 system prompt designed |
| Examples created | ✅ | 3 realistic policies |
| Documentation written | ✅ | README + BUILD_LOG + this file |
| Deployment plan | ✅ | Streamlit Cloud steps outlined |
| Rubric alignment verified | ✅ | 6/9 items complete, 3 tomorrow |

---

## ⚠️ Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| OpenAI API key issues | Blocks testing | Low | Pre-test API access |
| JSON parsing fails | Invalid output | Low | Extensive error handling |
| Streamlit Cloud deploy fails | No public URL | Low | Test locally first |
| Example policies too simple | Test cases don't challenge model | Medium | Included diverse difficulty |
| Time runs out | Incomplete submission | Low | 3-hour buffer built in |

---

## 📚 Lessons Learned / Aha Moments

1. **Prompt Engineering is Iterative**
   - V1 won't be perfect
   - Plan iterations BEFORE building (V2-V5 sketched)
   - Document trade-offs (accuracy vs. speed vs. cost)

2. **Grounding Prevents Hallucination**
   - Including example policies helps model understand domain
   - Domain glossary (charter school metrics) reduces false positives
   - Real-world context beats generic instructions

3. **User Interview Changes Everything**
   - Initial 5 ideas narrowed down through questioning
   - Real friction discovered (manual code updates)
   - Solution now directly addresses user's pain point

4. **Documentation IS Part of the Product**
   - Rubric requires visible thinking process
   - BUILD_LOG + README = demonstrating AI understanding
   - Comments in code help maintainability

5. **MVP Scope is Critical**
   - Temptation to add: PDF parsing, database, auth, real-time updates
   - Saying NO to these saved 20+ hours
   - 1-week timeline demands ruthless prioritization

---

## 🔮 Vision for Next Phases (Post-MVP)

### Phase 2: Production Hardening (Week 2-3)
- Add database to store analysis history
- Implement user authentication
- Improve error handling
- Add logging + monitoring

### Phase 3: Advanced Features (Week 4+)
- PDF/Word parsing (currently text-only)
- Batch policy analysis
- Dashboard integration (auto-update SQL)
- API endpoint (vs. just web UI)

### Phase 4: Domain Expansion
- Multi-language support
- Integration with real GVSU data
- Audit trail + compliance tracking
- Multi-tenant support (multiple charter school networks)

**Current Focus:** Stay in MVP scope. Don't build phase 2 unless user asks.

---

## 📞 Contact & Questions

**If this were a real project:**
- Stakeholder check-ins: 2x weekly with Charter Schools Office
- Feedback loops: After each policy run
- Bug reports: Submitted via GitHub Issues
- Feature requests: Prioritized backlog

**For this course:**
- Questions → Binju (student)
- Technical issues → TA/Professor
- Rubric feedback → Professor after submission

---

**Last Updated:** May 16, 2026, 6:30 PM (UTC)  
**Next Update:** Tomorrow after testing + deployment  
**Version:** 1.0-MVP (In Development)

---

## 📎 Quick Reference: Files Created This Session

```
✅ app.py                     (400+ lines, commented)
✅ llm_client.py              (120+ lines, documented)
✅ requirements.txt           (4 dependencies)
✅ .env.example               (API key template)
✅ .gitignore                 (security)
✅ README.md                  (150+ lines)
✅ EVALUATION.md              (test templates)
✅ BUILD_LOG.md               (prompt engineering tracking)
✅ PROJECT_JOURNAL.md         (this file, notes)
✅ docs/system_prompt.md      (v1 prompt)
✅ data/example_policies/     (3 realistic policies)
```

**Total:** 11 files + 1 directory structure created
**Lines of Code:** ~500+
**Lines of Documentation:** ~800+
**Time Invested:** 5 hours
**Remaining:** 2 hours (testing) + 2 hours (deployment + submission)
