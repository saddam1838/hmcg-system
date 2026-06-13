import subprocess
import tempfile
import os
import sys


def get_language_extension(constraints: list) -> str:
    if not constraints:
        return ".py"
    text = " ".join(constraints).lower()
    if "java" in text and "javascript" not in text:
        return ".java"
    if "c++" in text or "cpp" in text:
        return ".cpp"
    if "c#" in text or "csharp" in text:
        return ".cs"
    if "javascript" in text or "js" in text:
        return ".js"
    if "typescript" in text or "ts" in text:
        return ".ts"
    if "solidity" in text or "sol" in text:
        return ".sol"
    if "go" in text or "golang" in text:
        return ".go"
    if "rust" in text:
        return ".rs"
    return ".py"


def get_language_name(constraints: list) -> str:
    ext = get_language_extension(constraints)
    mapping = {
        ".py": "python",
        ".java": "java",
        ".cpp": "cpp",
        ".cs": "csharp",
        ".js": "javascript",
        ".ts": "typescript",
        ".sol": "solidity",
        ".go": "go",
        ".rs": "rust",
    }
    return mapping.get(ext, "python")


def save_code_file(code: str, task: str, constraints: list, session_id: str) -> str:
    os.makedirs("generated_code", exist_ok=True)
    ext = get_language_extension(constraints)
    safe_task = (
        "".join(c if c.isalnum() or c in " _-" else "_" for c in task[:30])
        .strip()
        .replace(" ", "_")
    )
    filename = f"{session_id}_{safe_task}{ext}"
    filepath = os.path.join("generated_code", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    return filepath


def execute_code(code: str, constraints: list = None, timeout: int = 10):
    lang = get_language_name(constraints)
    if lang != "python":
        return {
            "success": True,  # It's a success because we generated the file correctly
            "output": "",
            "error": f"Auto-execution is only supported for Python. {lang.upper()} code was generated and saved successfully.",
        }

    with tempfile.NamedTemporaryFile(
        suffix=".py", delete=False, mode="w", encoding="utf-8"
    ) as f:
        f.write(code)
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "", "error": "Execution timed out."}
    except Exception as e:
        return {"success": False, "output": "", "error": str(e)}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
