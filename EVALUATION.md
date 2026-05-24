# EVALUATION.md - Test Results & Performance

**Status:** MVP Evaluation (May 16, 2026)

## Test Cases
### Test Case 1: Grade Level Funding Rule

**Input Policy:**
```
Starting in the 2024-2025 school year, funding calculations will change based on student grade level:
- Elementary students (K-2): Full per-pupil funding allocation
- Primary students (3-5): Per-pupil funding + 10% performance bonus if proficiency rate >= 70%
- Middle school students (6-8): Per-pupil funding + 15% performance bonus if proficiency rate >= 75%
- High school students (9-12): Per-pupil funding + 20% performance bonus if graduation rate >= 85%
```

**Expected Output (Key Fields):**
- `grade_levels`: ["K-2", "3-5", "6-8", "9-12"]
- `affected_metrics`: ["proficiency", "graduation_rate", "funding"]
- `confidence`: "high"
- `human_review_required`: true

**Actual Result:** 
[To be filled after local testing]

**Status:** 
[ ] PASS
[ ] FAIL

**Notes:** 

---

### Test Case 2: Attendance-Based Funding

**Input Policy:**
```
Charter schools will now have funding adjusted based on overall attendance metrics:
- If school attendance rate >= 95%: Receive 105% of per-pupil funding
- If school attendance rate 90-94%: Receive 100% of per-pupil funding (no change)
- If school attendance rate 85-89%: Receive 95% of per-pupil funding (5% reduction)
- If school attendance rate < 85%: Receive 90% of per-pupil funding (10% reduction)
```

**Expected Output (Key Fields):**
- `grade_levels`: ["All"] or ["K-12"]
- `affected_metrics`: ["attendance_rate", "funding"]
- `confidence`: "high"
- `human_review_required`: true

**Actual Result:** 
[To be filled after local testing]

**Status:** 
[ ] PASS
[ ] FAIL

**Notes:** 

---

### Test Case 3: Special Population Tracking

**Input Policy:**
```
New requirement: All dashboard reports must now separately track proficiency metrics for special populations:
1. English Language Learners (ELL) - Track proficiency rate for ELL students
2. Students with Individualized Education Plans (IEP) - Track proficiency rate for IEP students
3. Students Receiving Free/Reduced Lunch (FRL) - Track proficiency rate for FRL students

Schools with > 30% ELL population receive 8% additional per-pupil funding.
```

**Expected Output (Key Fields):**
- `grade_levels`: ["All"] or ["K-12"]
- `affected_metrics`: ["proficiency", "ELL", "IEP", "FRL", "funding"]
- `confidence`: "high" or "medium"
- `human_review_required`: true

**Actual Result:** 
[To be filled after local testing]

**Status:** 
[ ] PASS
[ ] FAIL

**Notes:** 

---

## Evaluation Summary

**Total Test Cases:** 3
**Passed:** [ ] / 3
**Failed:** [ ] / 3
**Pass Rate:** [ ] %

### Scoring Rubric

For each test case, the model gets points for:

- **Grade levels correctly identified** (20 points)
- **Metrics correctly identified** (20 points)
- **Business logic explanation is reasonable** (20 points)
- **Suggested SQL/pseudocode is sensible** (20 points)
- **Ambiguities flagged appropriately** (10 points)
- **JSON is valid** (10 points)
- **TOTAL: 110 points**

### Success Threshold

- **100+ points (90%+):** Excellent
- **80-99 points (73%-89%):** Good
- **60-79 points (55%-72%):** Acceptable for MVP
- **<60 points:**  Needs improvement

---

## Running Tests Locally

### Setup (One Time)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set up .env
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Run the App

```bash
streamlit run app.py
```

### Manual Testing Procedure

1. Open `http://localhost:8501`
2. Go to "Example Policies" tab
3. Copy Policy 1: Grade Level Funding
4. Go to "Analyzer" tab
5. Paste policy into text box
6. Click "Analyze Policy"
7. Record the JSON output in the table above
8. Check each field against expected values
9. Mark PASS or FAIL
10. Repeat for Policies 2 and 3

---

## Sample Output Format

```json
{
  "rule_summary": "Charter schools now receive funding multipliers based on student grade level, with performance bonuses for proficiency and graduation rates.",
  "grade_levels": ["K-2", "3-5", "6-8", "9-12"],
  "affected_metrics": ["proficiency_rate", "graduation_rate", "per_pupil_funding", "performance_based_funding"],
  "business_logic_summary": "Dashboard must calculate per-pupil funding with grade-level-specific multipliers. Elementary gets flat rate; middle/high school get performance bonuses if they meet proficiency/graduation thresholds.",
  "suggested_sql_update": "ALTER TABLE funding_calculations ADD COLUMN grade_level_multiplier FLOAT; UPDATE funding_calculations SET grade_level_multiplier = CASE WHEN grade IN ('K','1','2') THEN 1.0 WHEN grade IN ('3','4','5') THEN 1.1 ... END;",
  "ambiguities": ["Is this retroactive to 2023-24 data?", "How are mid-year grade transfers handled?"],
  "confidence": "high",
  "human_review_required": true
}
```

---

## Notes for Iteration

**V1 Prompt Performance:**
- [ ] Mostly correct
- [ ] Some hallucinations
- [ ] Missing some fields
- [ ] Other (describe):

**Next Steps (For V2):**
- [ ] Add more examples to system prompt
- [ ] Refine field definitions
- [ ] Improve grade level handling
- [ ] Better ambiguity detection

---

## Prompt Engineering Decisions

### Why These Techniques?

1. **Explicit Role Definition** — Grounds the model in educational data domain
2. **Clear Output Format** — Ensures JSON is always valid and has required fields
3. **Field Descriptions** — Reduces hallucination by being specific about what each field means
4. **Safety Reminders** — Reinforces that human review is required
5. **Domain Context** — Lists charter school metrics so model understands terminology

### Trade-offs Made

- **Simplicity vs. Accuracy:** Chose simple prompt over complex multi-shot examples (faster to build)
- **JSON Enforcement vs. Flexibility:** Strict JSON format over free-text response (easier to parse)
- **Short vs. Long Prompt:** Kept prompt focused (faster inference, lower cost)

---

## Prompt Iteration Evaluation

### Example policy case: policy_1_grade_levels.txt

- Input: `data/example_policies/policy_1_grade_levels.txt`
- Baseline prompt: `docs/system_prompt_v1.md`
- Improved prompt: `docs/system_prompt.md` (V2)
- Expected behavior:
  - valid JSON only
  - all required keys present
  - standardized metric names
  - ambiguity list included when needed
  - `human_review_required: true`

#### V1 actual output

```json
{
  "rule_summary": "Starting in the 2024-2025 school year, funding calculations will vary by grade level, with specific performance bonuses for certain grades based on proficiency and graduation rates.",
  "grade_levels": ["K-2", "3-5", "6-8", "9-12"],
  "affected_metrics": [
    "per_pupil_funding",
    "proficiency_rate",
    "graduation_rate"
  ],
  "business_logic_summary": "The dashboard will need to implement new logic to calculate funding based on grade-specific performance metrics and apply bonuses accordingly, while also tracking graduation rates for high school students.",
  "suggested_sql_update": "UPDATE funding SET amount = CASE WHEN grade_level = 'K-2' THEN base_funding WHEN grade_level = '3-5' AND proficiency_rate >= 70 THEN base_funding * 1.10 WHEN grade_level = '6-8' AND proficiency_rate >= 75 THEN base_funding * 1.15 WHEN grade_level = '9-12' AND graduation_rate >= 85 THEN base_funding * 1.20 ELSE base_funding END;",
  "ambiguities": [
    "Does this apply retroactively to 2023-24 data?",
    "How are students counted who move grades mid-year?"
  ],
  "confidence": "low",
  "human_review_required": true
}
```

#### V2 actual output
- [paste actual V2 JSON output here]

#### Pass/Fail assessment
- `rule_summary`: 
- `grade_levels`: 
- `affected_metrics`: 
- `business_logic_summary`: 
- `suggested_sql_update`: 
- `ambiguities`: 
- `confidence`: 
- `human_review_required`: 

#### Observations
- What improved:
  - 
- What still failed:
  -

---

**Last Updated:** May 16, 2026  
**Evaluator:** Binju Karki  
**Next Review:** After first GitHub commit
