import argparse
from agents.metacognitive_orchestrator import MetacognitiveOrchestrator


def main():
    parser = argparse.ArgumentParser(description="HMCG CLI")
    parser.add_argument("--task", type=str, required=True, help="Task description")
    parser.add_argument(
        "--constraints",
        type=str,
        nargs="*",
        default=["Use Python", "Add tests"],
        help="Constraints",
    )
    args = parser.parse_args()

    print(f"🚀 Starting HMCG for task: {args.task}")
    orchestrator = MetacognitiveOrchestrator()
    results = orchestrator.run_pipeline(args.task, args.constraints)

    print("\n" + "=" * 50)
    if results["success"]:
        print("✅ SUCCESS!")
        if results["execution"].get("output"):
            print("Output:", results["execution"]["output"])
    else:
        print("❌ FAILED!")
        print("Error:", results["execution"].get("error", ""))
    print(f"Code saved to: {results.get('code_file_path')}")
    print("=" * 50)


if __name__ == "__main__":
    main()
