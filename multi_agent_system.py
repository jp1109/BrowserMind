
import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from planner_agent import research_graph
from multi_research import collect_research
from research_analyst import analyze_research
from verification_agent import verify_research


class AgentState(TypedDict):
    question: str
    tasks: list[str]
    sources: list[dict]
    analysis: str
    verdict: str


URLS = [
    "https://docs.langchain.com/oss/python/langgraph/overview",
    "https://docs.crewai.com/"
]


def planner_node(state: AgentState):
    result = research_graph.invoke({
        "question": state["question"],
        "tasks": [],
        "status": "pending"
    })

    return {"tasks": result["tasks"]}


def browser_node(state: AgentState):
    sources = collect_research(URLS)

    Path("browsermind_report.json").write_text(
        json.dumps({
            "question": state["question"],
            "tasks": state["tasks"],
            "sources": sources
        }, indent=4),
        encoding="utf-8"
    )

    return {"sources": sources}


def analyst_node(state: AgentState):
    analyze_research()

    result = json.loads(
        Path("research_analysis.json").read_text(
            encoding="utf-8"
        )
    )

    return {"analysis": result["analysis"]}


def verifier_node(state: AgentState):
    verify_research()

    result = json.loads(
        Path("verification_result.json").read_text(
            encoding="utf-8"
        )
    )

    return {"verdict": result["verdict"]}


builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)
builder.add_node("browser", browser_node)
builder.add_node("analyst", analyst_node)
builder.add_node("verifier", verifier_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "browser")
builder.add_edge("browser", "analyst")
builder.add_edge("analyst", "verifier")
builder.add_edge("verifier", END)

agent_graph = builder.compile()


if __name__ == "__main__":
    question = input("Enter research question: ")

    result = agent_graph.invoke({
        "question": question,
        "tasks": [],
        "sources": [],
        "analysis": "",
        "verdict": "pending"
    })

    print("\nBROWSERMIND FINAL REPORT")
    print("=" * 45)
    print("\nQuestion:", result["question"])
    print("\nAI Research Plan:")

    for task in result["tasks"]:
        print("-", task)

    print("\nResearch Analysis:")
    print(result["analysis"])

    print("\nVerification:", result["verdict"])
