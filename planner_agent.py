
from typing import TypedDict, List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


class ResearchPlan(BaseModel):
    tasks: List[str] = Field(
        description="Three to five specific research tasks"
    )


class ResearchState(TypedDict):
    question: str
    tasks: List[str]
    status: str


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

planner_llm = llm.with_structured_output(
    ResearchPlan,
    method="json_mode"
)


def create_plan(state: ResearchState):
    question = state["question"].strip()

    if not question:
        raise ValueError("Research question cannot be empty")

    prompt = (
    "You are BrowserMind's research planning agent.\n"
    "Return ONLY a valid JSON object with a 'tasks' key.\n"
    "The 'tasks' value must contain 3 to 5 specific "
    "research task strings.\n"
    "Do not include explanations or Markdown.\n"
    "Example format: "
    '{"tasks": ["Find official documentation", '
    '"Compare capabilities", "Verify findings"]}\n\n'
    f"Research question: {question}"
)

    plan = planner_llm.invoke(prompt)

    if not plan.tasks:
        raise ValueError("The AI returned an empty plan")

    return {
        "tasks": plan.tasks,
        "status": "planned"
    }


builder = StateGraph(ResearchState)
builder.add_node("planner", create_plan)
builder.add_edge(START, "planner")
builder.add_edge("planner", END)

research_graph = builder.compile()


if __name__ == "__main__":
    question = input("Enter your research question: ")

    result = research_graph.invoke({
        "question": question,
        "tasks": [],
        "status": "pending"
    })

    print("\nBrowserMind AI Research Plan")
    print("-" * 40)

    for index, task in enumerate(result["tasks"], start=1):
        print(f"{index}. {task}")

    print(f"\nStatus: {result['status']}")
