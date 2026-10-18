
import json
from datetime import datetime, timezone

from planner_agent import research_graph
from multi_research import collect_research

APPROVED_URLS = [
    "https://docs.langchain.com/oss/python/langgraph/overview",
    "https://docs.crewai.com/"
]


def run_research(question):
    print("\nPlanning research...")

    plan = research_graph.invoke({
        "question": question,
        "tasks": [],
        "status": "pending"
    })

    print("\nAI Research Plan:")
    for index, task in enumerate(plan["tasks"], 1):
        print(f"{index}. {task}")

    print("\nCollecting website evidence...")

    evidence = collect_research(APPROVED_URLS)

    report = {
        "question": question,
        "tasks": plan["tasks"],
        "sources": evidence,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    with open(
        "browsermind_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("\nResearch workflow completed!")
    print("Saved to browsermind_report.json")

    successful = sum(
        item["status"] == "success"
        for item in evidence
    )

    print(f"Sources collected: {successful}/{len(evidence)}")


if __name__ == "__main__":
    question = input("Enter your research question: ").strip()

    if not question:
        raise ValueError("Research question cannot be empty")

    run_research(question)
