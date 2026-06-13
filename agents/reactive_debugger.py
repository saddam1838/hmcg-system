from utils.llm_handler import LLMHandler
from utils.code_executor import execute_code, get_language_name


class ReactiveDebugger:
    def __init__(self, llm: LLMHandler):
        self.llm = llm
        self.max_iterations = 3

    def debug_and_execute(self, code: str, constraints: list = None):
        current_code = code
        history = []
        target_lang = get_language_name(constraints)

        for i in range(self.max_iterations):
            result = execute_code(current_code, constraints)
            history.append({"iteration": i + 1, "code": current_code, "result": result})

            if result["success"] or "Auto-execution is only supported" in result.get(
                "error", ""
            ):
                return {
                    "success": True,
                    "final_code": current_code,
                    "output": result["output"],
                    "error": result["error"],
                    "iterations": i + 1,
                    "history": history,
                }

            fix_prompt = f"""Fix the {target_lang.title()} code.
            Code:
            {current_code}
            
            Error:
            {result["error"]}
            
            Output ONLY the corrected, COMPLETE {target_lang.title()} code inside ```{target_lang} ... ```."""

            messages = [
                {
                    "role": "system",
                    "content": f"You are a debugging expert. Fix the {target_lang.title()} code.",
                },
                {"role": "user", "content": fix_prompt},
            ]

            response = self.llm.generate(messages, max_tokens=4096, temperature=0.1)
            current_code = self.llm.extract_code(response, target_lang)

        return {
            "success": False,
            "final_code": current_code,
            "error": result["error"],
            "iterations": self.max_iterations,
            "history": history,
        }
