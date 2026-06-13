from utils.llm_handler import LLMHandler
import json


class CollaborativeObserver:
    def __init__(self, llm: LLMHandler):
        self.llm = llm

    def validate_plan(self, plan: dict, task: str):
        system_prompt = """You are a Collaborative Observer AI. Evaluate the strategic plan.
Respond ONLY with a valid JSON object.
Keys: "completeness_score" (0-1), "feasibility_score" (0-1), "clarity_score" (0-1), 
"symmetry_score" (0-1), "specific_issues" (list of strings), "improvement_suggestions" (list of strings)."""

        user_prompt = f"Task: {task}\nPlan: {json.dumps(plan)}\nEvaluate."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.llm.generate(messages, max_tokens=800, temperature=0.2)
        validation = self.llm.clean_json_response(response)
        validation["pi_pe_analysis"] = self._check_symmetry(plan)
        return validation

    def validate_code(self, code: str, plan: dict, constraints: list):
        lang = get_language_name(constraints)

        system_prompt = f"""You are a Code Validation AI specializing in {lang.title()} and Multi-Agent Systems.
Evaluate if the code matches the plan. 
CRITICAL: Check for Permutation Invariance (PI) and Permutation Equivariance (PE).
Does the code rely on hardcoded indices or specific ordering of inputs/agents? If so, it violates PI.
Respond ONLY with valid JSON.
Keys: "alignment_score" (0-1), "quality_score" (0-1), "completeness_score" (0-1), 
"pi_pe_compliance" (boolean), "specific_problems" (list), "fix_suggestions" (list)."""

        code_preview = code[:3000] + "\n... [truncated]" if len(code) > 3000 else code
        user_prompt = f"Plan: {json.dumps(plan)}\nCode:\n{code_preview}\nEvaluate."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.llm.generate(messages, max_tokens=800, temperature=0.2)
        return self.llm.clean_json_response(response)

    def _check_symmetry(self, plan: dict):
        plan_text = json.dumps(plan).lower()
        keywords = ["any order", "symmetric", "permutation", "independent", "unordered"]
        score = 0.5
        issues = []
        if any(k in plan_text for k in keywords):
            score = 0.9
        if "order" in plan_text and "independent" not in plan_text:
            score -= 0.2
            issues.append("Plan may have hidden ordering dependencies (violates PI).")
        return {"robustness_score": max(0.1, score), "issues": issues}


def get_language_name(constraints: list) -> str:
    from utils.code_executor import get_language_name

    return get_language_name(constraints)
