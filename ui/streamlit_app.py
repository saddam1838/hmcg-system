import streamlit as st
import sys
import os
import json
import plotly.graph_objects as go
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.metacognitive_orchestrator import MetacognitiveOrchestrator
from utils.code_executor import get_language_extension, get_language_name

st.set_page_config(page_title="HMCG System", page_icon="🧠", layout="wide")
st.title("🧠 Hierarchical Metacognitive Code Generation (HMCG)")
st.markdown("**Proactive Planning • Collaborative Validation • Reactive Debugging**")

if "results" not in st.session_state:
    st.session_state.results = None


def render_radar_chart(validation):
    categories = ["Completeness", "Feasibility", "Clarity", "Symmetry"]
    values = [
        validation.get("completeness_score", 0),
        validation.get("feasibility_score", 0),
        validation.get("clarity_score", 0),
        validation.get("symmetry_score", 0),
    ]
    values.append(values[0])  # Close the circle

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values, theta=categories, fill="toself", name="Validation Scores"
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        height=300,
        margin=dict(t=30, b=30, l=60, r=60),
    )
    st.plotly_chart(fig, use_container_width=True)


with st.sidebar:
    st.header("⚙️ Configuration")
    task = st.text_area(
        "Task Description", "Create a sorting algorithm with test cases."
    )
    constraints_text = st.text_area(
        "Constraints (one per line)",
        "Use Python\nInclude error handling\nAdd test cases",
    )
    constraints = [c.strip() for c in constraints_text.split("\n") if c.strip()]

    st.info(
        "💡 **Specify language in constraints:**\n- Use Python → .py\n- Use Java → .java\n- Use C++ → .cpp\n- Use Solidity → .sol"
    )

    if st.button("🚀 Run HMCG Pipeline", type="primary", use_container_width=True):
        st.session_state.results = None
        try:
            with st.status("Running HMCG Pipeline...", expanded=True) as status:
                orchestrator = MetacognitiveOrchestrator()

                st.write("Step 1: Proactive Strategic Planning...")
                plan = orchestrator.planner.plan(task, constraints)

                st.write("Step 2: Collaborative Validation (Plan)...")
                plan_val = orchestrator.observer.validate_plan(plan, task)

                st.write("Step 3: Technical Code Generation...")
                code = orchestrator.coder.generate(plan, task, constraints)

                st.write("Step 4: Collaborative Validation (Code)...")
                code_val = orchestrator.observer.validate_code(code, plan, constraints)

                st.write("Step 5: Reactive Debugging...")
                debug_res = orchestrator.debugger.debug_and_execute(code, constraints)

                final_code = debug_res.get("final_code", code)
                from utils.code_executor import save_code_file

                code_path = save_code_file(
                    final_code,
                    task,
                    constraints,
                    f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                )

                res = {
                    "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "task": task,
                    "constraints": constraints,
                    "plan": plan,
                    "plan_validation": plan_val,
                    "generated_code": code,
                    "code_validation": code_val,
                    "execution": debug_res,
                    "success": debug_res["success"],
                    "code_file_path": code_path,
                    "final_code": final_code,
                    "timestamp": datetime.now().isoformat(),
                }
                st.session_state.results = res

                if debug_res["success"]:
                    status.update(
                        label="✅ Pipeline Completed Successfully!",
                        state="complete",
                        expanded=False,
                    )
                else:
                    status.update(
                        label="⚠️ Pipeline Completed with Errors.",
                        state="error",
                        expanded=False,
                    )
            st.rerun()
        except Exception as e:
            st.error(f"Pipeline failed: {e}")

if st.session_state.results:
    res = st.session_state.results
    lang = get_language_name(res.get("constraints", []))
    ext = get_language_extension(res.get("constraints", []))

    col1, col2, col3 = st.columns(3)
    col1.metric("Execution Success", "✅" if res.get("success") else "❌")
    col2.metric("Debug Iterations", res.get("execution", {}).get("iterations", 0))
    col3.metric("Language Generated", lang.upper())

    st.divider()

    if res.get("code_file_path"):
        st.success(f"✅ **Code file saved:** `{res['code_file_path']}`")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 Plan", "👁️ Validation", "💻 Code", "🐞 Debug", "💾 Export"]
    )

    with tab1:
        st.subheader("Strategic Plan")
        st.json(res.get("plan"))

    with tab2:
        st.subheader("Plan Validation Scores")
        render_radar_chart(res.get("plan_validation", {}))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Plan Critique")
            st.json(res.get("plan_validation", {}))
        with col2:
            st.subheader("Code Validation (PI/PE)")
            st.json(res.get("code_validation", {}))

    with tab3:
        st.subheader(f"Generated {lang.upper()} Code")
        st.code(res.get("final_code", ""), language=lang)

        if res.get("code_file_path") and os.path.exists(res["code_file_path"]):
            with open(res["code_file_path"], "r", encoding="utf-8") as f:
                file_content = f.read()
            st.download_button(
                label=f"📥 Download {ext.upper()} File",
                data=file_content,
                file_name=os.path.basename(res["code_file_path"]),
                mime="text/plain",
            )

    with tab4:
        st.subheader("Execution Output")
        if res.get("success"):
            st.success("✅ Code executed successfully!")
            if res.get("execution", {}).get("output"):
                st.text_area("Output:", res["execution"]["output"], height=200)
        else:
            st.error("❌ Execution failed.")
            st.code(res.get("execution", {}).get("error", ""), language="text")

    with tab5:
        st.subheader("Export Options")
        json_str = json.dumps(res, indent=2, default=str)
        st.download_button(
            "📥 Download JSON Metadata",
            json_str,
            f"{res['session_id']}.json",
            "application/json",
        )

        md_str = f"# HMCG Task Report\n**Task:** {res['task']}\n**Success:** {res['success']}\n\n## Code\n```{lang}\n{res.get('final_code', '')}\n```"
        st.download_button(
            "📥 Download Markdown Report",
            md_str,
            f"{res['session_id']}.md",
            "text/markdown",
        )
else:
    st.info(
        "👈 Enter a task and constraints in the sidebar, then click 'Run HMCG Pipeline'."
    )
