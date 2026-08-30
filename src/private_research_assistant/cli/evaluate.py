import json

from private_research_assistant.config import get_settings
from private_research_assistant.evaluation import evaluate_sample, results_as_dict
from private_research_assistant.query import ResearchAssistant


def main() -> None:
    settings = get_settings()
    samples = json.loads((settings.evaluation_dir / "questions.json").read_text(encoding="utf-8"))
    assistant = ResearchAssistant(settings)
    results = []
    for sample in samples:
        result = evaluate_sample(sample, assistant.ask(sample["question"]))
        results.append(result)
        print(f"{'PASS' if result.passed else 'FAIL'} {result.id}: {result.detail}", flush=True)
    payload = {"summary": {"passed": sum(result.passed for result in results), "total": len(results)}, "results": results_as_dict(results)}
    payload["summary"]["score"] = payload["summary"]["passed"] / payload["summary"]["total"]
    output = settings.evaluation_dir / "results.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Groundedness score: {payload['summary']['passed']}/{payload['summary']['total']}")
    print(f"Report written to {output}")


if __name__ == "__main__":
    main()
