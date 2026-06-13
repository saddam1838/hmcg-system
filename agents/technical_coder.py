from utils.llm_handler import LLMHandler
from utils.code_executor import get_language_name


class TechnicalCoder:
    def __init__(self, llm: LLMHandler):
        self.llm = llm

    def generate(self, plan: dict, task: str, constraints: list):
        target_lang = get_language_name(constraints)
        print(f"🎯 Instructing LLM to write {target_lang.title()} code...")

        system_prompt = f"""You are an expert {target_lang.title()} Developer. 
        Write COMPLETE, RUNNABLE, and BUG-FREE {target_lang.title()} code based on the plan.
        RULES:
        1. DO NOT truncate the code. Write the FULL implementation.
        2. Include all necessary imports/includes.
        3. Include error handling.
        4. Include a main function/block with test cases.
        5. Output ONLY the {target_lang.title()} code inside a ```{target_lang} ... ``` block. No explanations."""

        user_prompt = f"""Task: {task}
        Constraints: {", ".join(constraints)}
        Plan: {plan}
        
        Generate the complete {target_lang.title()} code now."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.llm.generate(messages, max_tokens=4096, temperature=0.1)
        code = self.llm.extract_code(response, target_lang)
        return code
