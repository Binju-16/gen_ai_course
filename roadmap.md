# Policy Rule Interpreter for Educational Analytics — MVP Roadmap

## 1. Project Context
**Course:** Generative AI Course (Master's in Data Science and Analytics)  
**Creator:** Binju Karki, GVSU Charter Schools Office Data Analyst GA  
**Real Problem:** Manually updating dashboard code every time charter school regulations or funding rules change.  
**GenAI Solution:** Build a prototype that parses policy/rule changes from Word docs or spreadsheets and suggests dashboard code updates.

---

## 2. Problem Statement
- **Current State:** Policy updates arrive in Word/spreadsheet → Manual code rewrite → Slow, error-prone updates
- **Friction:** Different grade levels have different requirements; funding rules are performance-based; rules change frequently
- **Why it matters:** Dashboard becomes stale, stakeholders get outdated information, time wasted on manual rewrites
- **GenAI Angle:** Use LLM to extract structured rules from unstructured documents and suggest code/logic changes

---

## 3. Target User
- **Primary:** Binju (and other data analysts at Charter Schools Office)
- **Use case:** Receives a policy update → Pastes it into the tool → Gets a structured interpretation + suggested dashboard logic
- **Skill level:** Data analyst comfortable with SQL/Python, not a software engineer

---

## 4. MVP Scope for This Week
**Goal:** A working web prototype deployed to a public URL with evidence of all 9 rubric items.

### What's Included:
- **Frontend:** Simple web form (HTML/CSS/JS or React)
  - Text box to paste policy/rule text
  - Optional file upload for Word/spreadsheet (basic text extraction)
  - Submit button
  
- **Backend:** Node.js/Python API that:
  - Takes policy text as input
  - Sends it to an LLM with a carefully crafted system prompt
  - Returns structured output: rule summary, affected metrics, suggested SQL/pseudocode
  
- **LLM Integration:**
  - Use OpenAI API (GPT-4 or GPT-4o mini for cost)
  - Grounding: Include example policies/rules in system prompt + context window
  - Evidence of prompt engineering: multiple iterations documented in README
  
- **Deployment:**
  - Deploy backend to **Render.com** (free tier) or **Vercel** (for Node.js)
  - Deploy frontend to **Vercel** or same platform
  - Public URL = ✓
  
- **GitHub:**
  - Create repo with meaningful commit messages
  - Document prompts, iterations, decisions in README/CHANGELOG
  - Include example policies as test cases
  
- **Testing/Evaluation:**
  - 3-5 test cases: past rule changes you've handled + expected output
  - Simple pass/fail checklist: "Did the AI extract the grade level requirement? Did it identify the funding formula?"

---

## 5. Out-of-Scope Items for the Draft
- ❌ Integration with actual dashboard (reference docs only)
- ❌ Database updates or automatic code deployment
- ❌ Complex file parsing (just plain text + basic CSV/spreadsheet text extraction)
- ❌ Multi-language support
- ❌ Production-grade error handling
- ❌ Authentication or user management
- ❌ Real-time policy feeds
- ❌ GenAI-generated code that runs automatically (human review always required)

---

## 6. Recommended Tech Stack
### Simplest Path (Recommended):
- **Frontend:** React + Vite (or vanilla JS + Tailwind)
- **Backend:** Node.js + Express (lightweight, easy to deploy)
- **LLM:** OpenAI API (GPT-4o mini for cost efficiency)
- **Deployment:** Vercel (both frontend and backend Node.js)
- **Version Control:** GitHub
- **Environment:** Windows/WSL2 + Git + VS Code

### Alternative (If you prefer Python):
- **Frontend:** Streamlit (easiest for quick prototypes)
- **Backend:** FastAPI or Flask
- **Deployment:** Streamlit Cloud (free) or Render.com
- **LLM:** OpenAI API

**Recommendation:** Go with **Streamlit** for MVP—faster to build, easier to iterate, one-click deployment to Streamlit Cloud.

---

## 7. Hosting/Deployment Plan
### Option A: Streamlit Cloud (Easiest)
1. Create `app.py` with Streamlit UI
2. Push to GitHub
3. Link repo to Streamlit Cloud
4. Public URL instant ✓
5. Re-deploys on every git push

### Option B: Vercel (Frontend + Node.js Backend)
1. Frontend: React app on Vercel
2. Backend: Node.js API on Vercel serverless functions
3. Connect via API calls
4. More control, slightly more setup

**For this MVP, recommend Option A (Streamlit).** You'll have a deployed working demo in 1-2 hours.

---

## 8. System Prompt Design
The system prompt is where "policy parsing magic" happens. Structure it like this:

```
You are an expert educational data analyst assistant. 
Your job is to interpret charter school policy and funding rule changes.

When given a policy or rule update, you MUST:
1. Identify what changed (old rule vs. new rule)
2. Extract affected data elements (grade levels, student demographics, funding metrics)
3. Describe the business logic impact (which dashboards/reports are affected)
4. Suggest SQL or pseudocode changes
5. Flag any ambiguities that need human clarification

Format output as structured JSON with these fields:
{
  "rule_name": "...",
  "affected_grade_levels": [...],
  "affected_metrics": [...],
  "business_logic_summary": "...",
  "suggested_sql_pseudocode": "...",
  "ambiguities_needing_clarification": [...],
  "confidence_score": 0-1,
  "human_review_required": true/false
}

ALWAYS include a warning: "This is AI-generated guidance. A human data analyst MUST review and validate before deploying."
```

---

## 9. Prompt Engineering Techniques to Use

### Iteration Plan (Document Each):
1. **Baseline Prompt** (v1): Simple instructions (Document in commit `docs/prompts/v1-baseline.txt`)
2. **Few-Shot Examples** (v2): Add 2-3 examples of policy changes → expected output (Commit: `prompt-engineering: add few-shot examples`)
3. **Structured Output** (v3): Enforce JSON format + field validation (Commit: `prompt-engineering: enforce structured JSON output`)
4. **Grounding + Context** (v4): Include real policy snippets from Charter Schools Office in system prompt (Commit: `prompt-engineering: add domain context`)
5. **Refinement** (v5): Based on test failures, refine ambiguity detection (Commit: `prompt-engineering: improve ambiguity detection`)

### Techniques to Showcase:
- **System prompt design** → Clear instructions, role definition
- **Few-shot learning** → Examples in the prompt
- **Structured output** → JSON enforcement
- **Grounding** → Real policy snippets as context
- **Iterative refinement** → Documented tests and fixes

---

## 10. Grounding Strategy
**How to anchor the LLM to your specific domain:**

1. **Include real policy snippets in system prompt:**
   ```
   Here are examples of rule changes you may encounter:
   
   Example 1: "Starting 2024-25, Grade 6-8 students count toward 
   funding if they score at/above proficiency on state assessments."
   
   Extract: grade_levels=[6,7,8], metric="proficiency_score", 
   funding_dependent=true
   ```

2. **Create a "Policy Context" document:**
   - List common metrics: proficiency_score, attendance_rate, graduation_rate, etc.
   - List grade level groupings: [K-2], [3-5], [6-8], [9-12]
   - List funding categories: per_pupil, performance_based, weighted

3. **Upload example policies to GitHub:**
   - `data/example_policies/policy_grade_levels.txt`
   - `data/example_policies/policy_funding_formula.txt`
   - `data/example_policies/policy_performance_metrics.txt`

4. **Store and reference in system prompt:**
   - System prompt retrieves these examples at runtime
   - Or: Include them directly in the prompt text for MVP

---

## 11. Coding Plan

### Phase 1: Setup (30 mins)
```
1. Create GitHub repo: policy-rule-interpreter
2. Initialize Streamlit app structure
3. Create .env file for OpenAI API key
4. Set up requirements.txt
```

### Phase 2: Frontend (45 mins)
```
1. Streamlit text area for policy input
2. Example policy dropdown (load from data/examples/)
3. Submit button
4. Display output section (for results)
5. Add sidebar with system prompt viewer (for transparency)
```

### Phase 3: LLM Integration (1 hour)
```
1. Create openai_client.py module
2. Load system prompt from file (docs/system_prompt.md)
3. Send user input + system prompt to GPT-4o mini
4. Parse JSON response
5. Display formatted output
```

### Phase 4: Grounding + Examples (45 mins)
```
1. Create data/example_policies/ directory
2. Add 3-5 real or realistic policy examples
3. Load examples in frontend dropdown
4. Store policy context in system prompt
```

### Phase 5: Testing + Evaluation (1 hour)
```
1. Create test_cases.json with 3-5 test policies + expected outputs
2. Build simple test harness (manual or automated)
3. Document results in EVALUATION.md
```

### Phase 6: Deployment (30 mins)
```
1. Push to GitHub
2. Deploy to Streamlit Cloud (connect repo → instant URL)
3. Test public URL
4. Document in README
```

---

## 12. Test Harness / Evaluation Plan

### Simple Evaluation Framework:
Create `EVALUATION.md` with a test table:

```
| Test Case | Input Policy | Expected: Grade Levels | Expected: Metrics | AI Output | Pass/Fail | Notes |
|-----------|--------------|------------------------|-------------------|-----------|-----------|-------|
| Rule 1    | "Grade 6-8 proficiency..." | [6,7,8] | [proficiency] | ✓ | PASS | Correct |
| Rule 2    | "Funding depends on..." | all | [multiple] | Partial | FAIL | Missed one metric |
| Rule 3    | ... | ... | ... | ... | PASS | ... |
```

### Success Criteria (for each test case):
- ✓ Correctly identified affected grade levels
- ✓ Correctly identified affected metrics
- ✓ Business logic summary is accurate
- ✓ Suggested SQL/pseudocode is sensible
- ✓ Ambiguities flagged appropriately
- ✓ Human review warning is present

### Acceptable MVP Standard:
- 3+ test cases, 60%+ pass rate = acceptable
- 4+ test cases, 75%+ pass rate = good
- 5+ test cases, 90%+ pass rate = excellent

---

## 13. Success Metrics

### Rubric Alignment:
1. ✓ **Public deployed URL** → Streamlit Cloud live link
2. ✓ **GitHub repository** → Repo with commits, code, docs
3. ✓ **Evidence of prompt engineering** → Docs/prompts/ folder with versions
4. ✓ **Purposeful system prompt** → Clear, role-based, structured
5. ✓ **Grounding using policy text** → Example policies in data/ + system prompt
6. ✓ **Code with meaningful commits** → 10+ commits with clear messages
7. ✓ **README/build log** → Prompts, decisions, experiments documented
8. ✓ **Evidence of iteration and testing** → EVALUATION.md + test cases
9. ✓ **Basic evaluation showing "good"** → Test results + threshold

### Additional Success:
- Tool correctly parses at least 3 realistic policy changes
- Output is actionable (data analyst could use it)
- Prototype runs error-free for demo

---

## 14. Risks and Limitations

### Risks:
- **LLM hallucination:** AI invents metrics or rules not in policy
  - Mitigation: Always show confidence score + require human review
  
- **Policy ambiguity:** Poorly written rules confuse the AI
  - Mitigation: Flag ambiguities; suggest clarifying questions
  
- **Cost overruns:** OpenAI API calls add up
  - Mitigation: Use GPT-4o mini, monitor token usage, set budget limits
  
- **Deployment issues:** Streamlit or API goes down
  - Mitigation: Document local setup in README; include example outputs

### Limitations (Document Clearly):
- This is a **prototype, not production-ready**
- **Human review is mandatory**—AI output is guidance only
- Handles text policies; complex PDFs require manual text extraction
- Works best for English-language policies
- May not handle edge cases or novel rule types

---

## 15. GitHub Commit Plan

### Commit Strategy (Meaningful Messages):
```
Initial setup:
  - init: create streamlit app structure
  - docs: add project roadmap and setup instructions

Feature development:
  - feat: add policy text input form
  - feat: integrate openai api for rule parsing
  - feat: add example policies dropdown
  - feat: display structured json output

Prompt engineering (Document Each):
  - prompt-engineering: v1-baseline instructions
  - prompt-engineering: v2-add few-shot examples
  - prompt-engineering: v3-enforce json structure
  - prompt-engineering: v4-add domain grounding
  - prompt-engineering: v5-refine ambiguity detection

Testing & docs:
  - test: add 5 policy test cases
  - docs: add evaluation results
  - docs: add system prompt to README
  - docs: final cleanup and usage guide

Deployment:
  - deploy: prepare for streamlit cloud
  - docs: add deployment instructions
```

**Total: 15-20 meaningful commits**

---

## 16. README/Build Log Plan

### README.md Structure:
```
# Policy Rule Interpreter for Educational Analytics

## Project Overview
[1-2 paragraph description]

## Problem & Solution
[Why this project? What problem does it solve?]

## Demo
[Link to deployed URL]

## Features
- Parse charter school policy/rule changes
- Generate structured rule summaries
- Suggest dashboard logic updates
- Flag ambiguities needing human review

## Tech Stack
[List: Streamlit, OpenAI, Python, etc.]

## How to Use
[Step-by-step for users]

## Installation & Setup
[Clone, install deps, env vars, run locally]

## System Prompt & Prompt Engineering
[Show system prompt; document iterations v1-v5]

## Example Policies
[Link to data/example_policies/]

## Test Results & Evaluation
[Link to EVALUATION.md]

## Limitations & Disclaimers
[What it can't do; human review required]

## Future Enhancements
[Out-of-scope ideas]

## Author
Binju Karki, GVSU
```

### BUILD_LOG.md (Detailed Experiments):
```
## Prompt Engineering Iterations

### V1: Baseline (Commit: prompt-engineering-v1)
Prompt: "Extract rules from policy text"
Result: Too vague, hallucinated fields
Lesson: Need explicit field definitions

### V2: Few-Shot Examples (Commit: prompt-engineering-v2)
Prompt: Added 2 examples of policy → expected JSON
Result: Better structure, still missed some metrics
Lesson: Examples help, but need more domain context

### V3: Structured Output Enforcement (Commit: prompt-engineering-v3)
Prompt: "Output MUST be valid JSON with these exact fields: ..."
Result: JSON always valid, but sometimes too literal
Lesson: Structure helps; need semantic reasoning

### V4: Domain Grounding (Commit: prompt-engineering-v4)
Prompt: Added glossary of charter school terms + real policies
Result: Accuracy improved significantly
Lesson: Grounding + examples = best results

### V5: Ambiguity Detection (Commit: prompt-engineering-v5)
Prompt: "If you're unsure, list questions instead of guessing"
Result: Fewer hallucinations, more helpful
Lesson: Honesty from AI > False confidence
```

---

## 17. Questions I Need to Answer Before Coding

1. **OpenAI API Key Setup:**
   - Do you have an OpenAI account + API key?
   - Budget for this project? (estimate: $5-10 for MVP testing)

2. **Real Example Policies:**
   - Can you provide 2-3 real (or anonymized) policy changes you've dealt with?
   - Or should I create realistic synthetic examples?

3. **Dashboard Tech:**
   - What tool/language is your dashboard built in? (SQL? Power BI? Tableau? Custom?)
   - Does this affect the "suggested code" format? (SQL vs. pseudocode vs. DAX vs. ...)

4. **Deployment Preference:**
   - Streamlit Cloud (instant, free, simplest)?
   - Or do you prefer traditional Node.js + React on Vercel?

5. **Evaluation Threshold:**
   - What counts as "success"? 80% accuracy? 90%?
   - Or is it more qualitative: "Would a data analyst find this useful?"

6. **Local Development:**
   - Windows + WSL2 + Git + VS Code? Confirmed setup?
   - Any existing Python environment for this course?

---

## 18. Step-by-Step Task List for Building MVP

### Week 1 Execution Plan:

**Day 1-2: Planning & Setup (2-3 hours)**
- [ ] Answer questions in Section 17
- [ ] Create GitHub repo
- [ ] Set up local dev environment
- [ ] Create initial project structure
- [ ] Push initial commit

**Day 2-3: Frontend (2 hours)**
- [ ] Create Streamlit app skeleton
- [ ] Add text input area for policy
- [ ] Add example dropdown (with 3 sample policies)
- [ ] Add submit button
- [ ] Add output display area
- [ ] Test locally
- [ ] Commit: "feat: add policy input form"

**Day 3-4: LLM Integration (2-3 hours)**
- [ ] Create system prompt (docs/system_prompt.md)
- [ ] Set up OpenAI API client
- [ ] Test basic API call locally
- [ ] Parse JSON response
- [ ] Display formatted output in Streamlit
- [ ] Commit: "feat: integrate openai api"
- [ ] Commit: "docs: add system prompt v1"

**Day 4-5: Prompt Engineering (2 hours)**
- [ ] Run 2-3 test policies through current prompt
- [ ] Document results
- [ ] Refine prompt (add examples, grounding, structure)
- [ ] Re-test
- [ ] Make 2-3 prompt engineering commits
- [ ] Document iterations in BUILD_LOG.md

**Day 5-6: Testing & Evaluation (1.5 hours)**
- [ ] Create 5 formal test cases
- [ ] Run each through the system
- [ ] Document results in EVALUATION.md
- [ ] Mark pass/fail
- [ ] Commit: "test: add 5 policy test cases"
- [ ] Commit: "docs: add evaluation results"

**Day 6-7: Documentation & Deployment (1.5-2 hours)**
- [ ] Write comprehensive README
- [ ] Create EVALUATION.md
- [ ] Add deployment instructions
- [ ] Deploy to Streamlit Cloud
- [ ] Test public URL
- [ ] Final README touches
- [ ] Commit: "docs: finalize readme and build log"
- [ ] Commit: "deploy: streamlit cloud setup"

**Day 7: Demo Prep (30 mins)**
- [ ] Write usage walkthrough
- [ ] Prepare 1-2 live demo policies
- [ ] Create screenshot/screencast if possible
- [ ] Verify all rubric items are met

---

## Summary: MVP Scope

**What You'll Have:**
✓ Working prototype at public URL  
✓ GitHub repo with 15-20 meaningful commits  
✓ 5 versions of system prompt (documented)  
✓ 3-5 real/realistic example policies  
✓ 5 test cases with pass/fail results  
✓ Comprehensive README + EVALUATION.md  
✓ Clear evidence of prompt engineering + iteration  
✓ A tool that *actually works* for your use case  

**What It Does:**
- User pastes a policy or rule change
- AI parses it into structured format
- Suggests dashboard logic changes
- Flags ambiguities and requires human review
- All output is transparent (you can see the system prompt)

**What It Doesn't Do:**
- Generate production-ready code
- Auto-deploy to dashboards
- Handle PDFs or complex parsing
- Run without human review

**Time Estimate:** 12-15 hours over 7 days (1.5-2 hours/day)

---

## Next Steps

1. **Answer the 6 questions in Section 17**
2. **Gather 2-3 real policy examples** (or we'll create synthetic ones)
3. **Start Day 1: Set up GitHub repo and local environment**
4. **Begin with frontend (Streamlit form)**

Once you confirm you're ready, we'll start building. Pick a day/time and we'll code the MVP together.

---

**Last Updated:** May 16, 2026  
**Status:** Ready for implementation
