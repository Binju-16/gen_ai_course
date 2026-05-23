import streamlit as st
import json
from llm_client import PolicyAnalyzer

st.set_page_config(
    page_title="Policy Rule Interpreter",
    page_icon="📋",
    layout="wide"
)

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

if "policy_text" not in st.session_state:
    st.session_state["policy_text"] = ""

tab1, tab2, tab3 = st.tabs(["Analyzer", "Example Policies", "System Prompt"])

with tab1:
    st.header("Policy Analyzer")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Input Policy Text")
        policy_text = st.text_area(
            "Paste your policy or rule update here:",
            value=st.session_state["policy_text"],
            height=300,
            placeholder="Paste policy text here...",
            help="You can paste text from Word docs, emails, or any policy document.",
        )

        analyze_button = st.button(
            "🔍 Analyze Policy",
            type="primary",
            use_container_width=True,
        )

    with col2:
        st.subheader("AI Analysis Result")
        output_container = st.container()

    if analyze_button:
        if not policy_text.strip():
            st.error("❌ Please paste a policy before clicking Analyze")
        else:
            st.session_state["policy_text"] = policy_text
            with st.spinner("🤖 Analyzing policy with AI..."):
                try:
                    analyzer = PolicyAnalyzer()
                    result = analyzer.analyze_policy(policy_text)

                    with output_container:
                        st.success("✅ Analysis complete!")
                        st.json(result)

                        with st.expander("📖 Detailed Breakdown"):
                            st.write("**Rule Summary:**", result.get("rule_summary", "N/A"))
                            st.write(
                                "**Affected Grade Levels:**",
                                ", ".join(result.get("grade_levels", [])) or "N/A",
                            )
                            st.write(
                                "**Affected Metrics:**",
                                ", ".join(result.get("affected_metrics", [])) or "N/A",
                            )
                            st.write(
                                "**Business Logic Impact:**",
                                result.get("business_logic_summary", "N/A"),
                            )
                            if result.get("suggested_sql_update"):
                                st.code(result["suggested_sql_update"], language="sql")
                            if result.get("ambiguities"):
                                st.warning("⚠️ Ambiguities:")
                                for amb in result["ambiguities"]:
                                    st.write(f"- {amb}")

                        st.warning(
                            "⚠️ IMPORTANT: This is AI-generated guidance. "
                            "A human analyst must validate the output before implementation."
                        )

                        st.download_button(
                            label="📥 Download JSON Result",
                            data=json.dumps(result, indent=2),
                            file_name="policy_analysis.json",
                            mime="application/json",
                        )

                except ValueError as e:
                    with output_container:
                        st.error(f"❌ API Error: {str(e)}")
                        st.info("Make sure your .env file has a valid OPENAI_API_KEY")
                except Exception as e:
                    with output_container:
                        st.error(f"❌ Unexpected error: {str(e)}")
                        st.info("Check the terminal for more details.")

with tab2:
    st.header("Example Policies for Testing")
    st.markdown("Click a policy below to copy it into the analyzer input.")

    examples = [
        ("Policy 1: Grade Level Funding", "data/example_policies/policy_1_grade_levels.txt"),
        ("Policy 2: Attendance-Based Funding", "data/example_policies/policy_2_attendance_funding.txt"),
        ("Policy 3: Special Population Tracking", "data/example_policies/policy_3_demographics.txt"),
    ]

    for title, filepath in examples:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            st.warning(f"Example file not found: {filepath}")
            continue

        with st.expander(f"📄 {title}"):
            st.text(content)
            if st.button(f"Copy to Analyzer", key=filepath):
                st.session_state["policy_text"] = content
                st.success(f"Copied {title} to analyzer!")
                st.experimental_rerun()

with tab3:
    st.header("System Prompt")
    try:
        with open("docs/system_prompt.md", "r", encoding="utf-8") as f:
            prompt_content = f.read()
        st.text_area("System prompt", value=prompt_content, height=400, disabled=True)
    except FileNotFoundError:
        st.error("System prompt file not found: docs/system_prompt.md")