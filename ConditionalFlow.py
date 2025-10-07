from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

class QAState(TypedDict):
    question: str
    answer: str
    qtype: str


load_dotenv()

llm_fast = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

llm_reasoning = ChatOpenAI(model="gpt-4o", temperature=0.7)


def get_question(state):
    # In real app, this can come from user input
    return {"question": "Why is the sky blue?"}


def classify_question(state):
    q = state["question"].lower()
    # Simple classification logic
    if q.startswith(("what", "who", "when", "where")):
        qtype = "factual"
    else:
        qtype = "reasoning"
    print(f" Classified as: {qtype}")
    return {"qtype": qtype}


def factual_answer(state):
    q = state["question"]
    res = llm_fast.invoke(f"Answer briefly in 1 line: {q}")
    print(" Factual Answer:", res.content)
    return {"answer": res.content}

def reasoning_answer(state):
    q = state["question"]
    res = llm_reasoning.invoke(f"Explain step by step: {q}")
    print(" Reasoning Answer:", res.content)
    return {"answer": res.content}

def decide_next(state):
    if state["qtype"] == "factual":
        return "factual_answer"
    else:
        return "reasoning_answer"
    

graph = StateGraph(QAState)

graph.add_node("get_question", get_question)
graph.add_node("classify_question", classify_question)
graph.add_node("factual_answer", factual_answer)
graph.add_node("reasoning_answer", reasoning_answer)

graph.set_entry_point("get_question")

graph.add_edge("get_question", "classify_question")

graph.add_conditional_edges(
    "classify_question",
    decide_next,
    {
        "factual_answer": "factual_answer",
        "reasoning_answer": "reasoning_answer"
    }
)

graph.add_edge("factual_answer", END)
graph.add_edge("reasoning_answer", END)

app = graph.compile()
final_state = app.invoke({})