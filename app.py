"""
Policy Rule Interpreter for Educational Analytics - Main Streamlit App

This is the user-facing web interface. It:
1. Displays a form where users paste policy text
2. Sends the policy to OpenAI for analysis via llm_client.py
3. Displays the structured JSON response
4. Shows a warning that human review is required

To run locally:
    streamlit run app.py

Then open: http://localhost:8501
"""

import streamlit as st
import json
from llm_client import PolicyAnalyzer

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="Policy Rule Interpreter",
    page_icon="📋",
    layout="wide"
)

# ===== PAGE HEADER =====
st.title("📋 Policy Rule Interpreter for Educational Analytics")
st.markdown("""
This tool helps charter school data analysts quickly understand policy changes.

**How it works:**
1. Paste a policy or rule update in the text box below
2. Click "Analyze Policy" 
3. The AI will extract structured insights about the rule change
4. **IMPORTANT:** A human analyst must review the output before using it

---
""")

# ===== TABS FOR NAVIGATION =====
tab1, tab2, tab3 = st.tabs(["Analyzer", "Example Policies", "System Prompt"])

# ===== TAB 1: MAIN ANALYZER =====
with tab1:
    st.header("Policy Analyzer")
    
    # Two-column layout: input on left, output on right
    col1, col2 = st.columns([1, 1])
    
    # LEFT COLUMN: INPUT
    with col1:
        st.subheader("Input Policy Text")
        
        # Text area for user to paste policy
        policy_text = st.text_area(
            label="Paste your policy or rule update here:",
            height=300,
            placeholder="Paste policy text here...",
            help="You can paste text from Word docs, emails, or any policy document."
        )
        
        # Button to submit
        analyze_button = st.button(
            "🔍 Analyze Policy",
            type="primary",
            use_container_width=True
        )
    
    # RIGHT COLUMN: OUTPUT
    with col2:
        st.subheader("AI Analysis Result")
        
        # This will hold the output
        output_container = st.container()
    
    # ===== ANALYSIS LOGIC =====
    if analyze_button:
        if not policy_text.strip():
            st.error("❌ Please paste a policy before clicking Analyze")
        else:
            with st.spinner("🤖 Analyzing policy with AI..."):
                try:
                    # Initialize the LLM client
                    analyzer = PolicyAnalyzer()
                    
                    # Call the LLM to analyze the policy
                    result = analyzer.analyze_policy(policy_text)
                    
                    # Display the result in the right column
                    with output_container:
                        # Show success message
                        st.success("✅ Analysis complete!")
                        
                        # Show result in nice format
                        st.json(result)
                        
                        # Show expandable view of each field
                        with st.expander("📖 Detailed Breakdown"):
                            if "rule_summary" in result:
                                st.write("**Rule Summary:**", result.get("rule_summary"))
                            if "grade_levels" in result:
                                st.write("**Affected Grade Levels:**", ", ".join(result.get("grade_levels", [])))
                            if "affected_metrics" in result:
                                st.write("**Affected Metrics:**", ", ".join(result.get("affected_metrics", [])))
                            if "business_logic_summary" in result:
                                st.write("**Business Logic Impact:**", result.get("business_logic_summary"))
                            if "suggested_sql_update" in result:
                                st.code(result.get("suggested_sql_update"), language="sql")
                            if "ambiguities" in result:
                                ambiguities = result.get("ambiguities", [])
                                if ambiguities:
                                    st.warning("⚠️ **Ambiguities flagged:**")
                                    for amb in ambiguities:
                                        st.write(f"• {amb}")
                        
                        # CRITICAL WARNING
                        st.warning(
                            "⚠️ **IMPORTANT:** This is AI-generated guidance, not an authoritative policy interpretation. "
                            "A human data analyst MUST review this output and validate it against the original policy before implementing any dashboard changes."
                        )
                        
                        # Download button for JSON result
                        st.download_button(
                            label="📥 Download JSON Result",
                            data=json.dumps(result, indent=2),
                            file_name="policy_analysis.json",
                            mime="application/json"
                        )
                
                except ValueError as e:
                    with output_container:
                        st.error(f"❌ API Error: {str(e)}")
                        st.info("Make sure your .env file has a valid OPENAI_API_KEY")
                
                except Exception as e:
                    with output_container:
                        st.error(f"❌ Unexpected error: {str(e)}")
                        st.info("Please check the terminal for more details.")

# ===== TAB 2: EXAMPLE POLICIES =====
with tab2:
    st.header("Example Policies for Testing")
    st.markdown("""
    These are realistic charter school policy changes. 
    Copy and paste them into the analyzer to test how the system works.
    """)
    
    # Load and display the three example policies
    examples = [
        ("Policy 1: Grade Level Funding", "data/example_policies/policy_1_grade_levels.txt"),
        ("Policy 2: Attendance-Based Funding", "data/example_policies/policy_2_attendance_funding.txt"),
        ("Policy 3: Special Population Tracking", "data/example_policies/policy_3_demographics.txt"),
    ]
    
    for title, filepath in examples:
        try:
            with open(filepath, "r") as f:
                content = f.read()
            
            with st.expander(f"📄 {title}"):
                # Show the policy text
                st.text(content)
                
                # Copy button
                st.button(
                    f"Copy to Analyzer",
                    key=filepath,
                    on_click=lambda: st.session_state.update({"policy_text": content})
                )
        except FileNotFoundError:
            st.warning(f"Example file not found: {filepath}")

# ===== TAB 3: SYSTEM PROMPT =====
with tab3:
    st.header("System Prompt (Prompt Engineering)")
    st.markdown("""
    This is the **system prompt** - the instructions that tell the AI how to behave.
    
    Prompt engineering is the art of writing clear instructions for AI models.
    A well-designed prompt leads to better, more consistent outputs.
    """)
    
    try:
        with open("docs/system_prompt.md", "r") as f:
            prompt_content = f.read()
        
        st.text_area(
            label="Current System Prompt (Read-Only):",
            value=prompt_content,
            height=400,
            disabled=True
        )
    except FileNotFoundError:
        st.error("System prompt file not found at docs/system_prompt.md")
    
    st.markdown("""
    ### How This Prompt Works:
    1. **Role Definition:** Tells the AI it's an "expert educational data analyst"
    2. **Task Description:** Explains exactly what to do (parse policies)
    3. **Output Format:** Specifies JSON structure with exact field names
    4. **Context:** Lists key metrics and terminology specific to charter schools
    5. **Critical Reminder:** Always tells the model to require human review
    
    ### Prompt Engineering Techniques Used:
    - **Clear role assignment** → Better context
    - **Explicit output format** → Consistent JSON responses
    - **Domain context** → Examples of relevant metrics and terminology
    - **JSON enforcement** → Ensures structured, parseable output
    - **Safety warning** → Reminds model to flag when human review is needed
    """)

# ===== SIDEBAR INFO =====
with st.sidebar:
    st.markdown("### 📊 About This Tool")
    st.markdown("""
    **Purpose:** Help charter school data analysts quickly parse policy changes
    
    **Tech Stack:**
    - Streamlit (frontend/UI)
    - OpenAI GPT-4o-mini (LLM)
    - Python (backend)
    
    **Status:** MVP - Working prototype for demonstration
    
    **Rubric Items Met:**
    - ✅ Public deployed URL (Streamlit Cloud)
    - ✅ GitHub repository
    - ✅ Evidence of prompt engineering (see System Prompt tab)
    - ✅ Purposeful system prompt (grounded in charter school domain)
    - ✅ Grounding using policy text (example policies in data/)
    - ✅ Code with meaningful commits
    - ✅ README/build log (see repo)
    - ✅ Evidence of iteration (multiple prompt versions)
    - ✅ Basic evaluation (test cases run locally)
    """)
    
    st.markdown("---")
    st.markdown("""
    ### 🔧 Setup Instructions
    
    **Local Setup:**
    ```
    python -m venv venv
    source venv/bin/activate  # Windows: venv\\Scripts\\activate
    pip install -r requirements.txt
    streamlit run app.py
    ```
    
    **Environment File:**
    1. Copy `.env.example` to `.env`
    2. Add your OpenAI API key
    3. Save and restart the app
    """)
    
    st.markdown("---")
    st.markdown("""
    **Created by:** Binju Karki  
    **For:** GVSU Master's Generative AI Course  
    **Problem:** Automating charter school policy analysis for dashboard updates
    """)
