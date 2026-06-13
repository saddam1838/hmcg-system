from .strategic_planner import StrategicPlanner
from .collaborative_observer import CollaborativeObserver
from .technical_coder import TechnicalCoder
from .reactive_debugger import ReactiveDebugger
from utils.llm_handler import LLMHandler
from utils.code_executor import save_code_file
import json
import os
from datetime import datetime


class MetacognitiveOrchestrator:
    def __init__(self):
        self.llm = LLMHandler()
        self.planner = StrategicPlanner(self.llm)
        self.observer = CollaborativeObserver(self.llm)
        self.coder = TechnicalCoder(self.llm)
        self.debugger = ReactiveDebugger(self.llm)

    def run_pipeline(self, task: str, constraints: list):
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 1. Proactive Strategic Planning
        plan = self.planner.plan(task, constraints)

        # 2. Collaborative Validation (Plan)
        plan_validation = self.observer.validate_plan(plan, task)

        # 3. Technical Code Generation
        code = self.coder.generate(plan, task, constraints)

        # 4. Collaborative Validation (Code)
        code_validation = self.observer.validate_code(code, plan, constraints)

        # 5. Reactive Debugging
        debug_result = self.debugger.debug_and_execute(code, constraints)

        # Save Code File
        final_code = debug_result.get("final_code", code)
        code_file_path = save_code_file(final_code, task, constraints, session_id)

        results = {
            "session_id": session_id,
            "task": task,
            "constraints": constraints,
            "plan": plan,
            "plan_validation": plan_validation,
            "generated_code": code,
            "code_validation": code_validation,
            "execution": debug_result,
            "success": debug_result["success"],
            "code_file_path": code_file_path,
            "final_code": final_code,
            "timestamp": datetime.now().isoformat(),
        }

        # Save Metadata
        os.makedirs("saved_tasks", exist_ok=True)
        filepath = os.path.join("saved_tasks", f"{session_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return results
