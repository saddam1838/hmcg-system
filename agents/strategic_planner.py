from utils.llm_handler import LLMHandler


class StrategicPlanner:
    def __init__(self, llm: LLMHandler):
        self.llm = llm

    def plan(self, task: str, constraints: list):
        system_prompt = """You are a Strategic Planning AI. Create a detailed strategic plan for a programming task.
You MUST respond ONLY with a valid JSON object. No markdown, no explanations.
The JSON must have these exact keys:
- "problem_decomposition": list of strings
- "strategy_rationale": string
- "agent_roles": list of strings
- "coordination_strategy": string
- "expected_challenges": list of strings
- "success_criteria": list of strings
"""
        user_prompt = f"Task: {task}\nConstraints: {', '.join(constraints)}\nGenerate the JSON plan now."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.llm.generate(messages, max_tokens=1024, temperature=0.3)
        plan = self.llm.clean_json_response(response)

        if "error" in plan:
            plan = {
                "problem_decomposition": [
                    "Analyze requirements",
                    "Write code",
                    "Add tests",
                ],
                "strategy_rationale": "Standard approach",
                "agent_roles": ["Developer", "Tester"],
                "coordination_strategy": "Sequential",
                "expected_challenges": ["Edge cases"],
                "success_criteria": ["Code runs without errors"],
            }
        return plan
