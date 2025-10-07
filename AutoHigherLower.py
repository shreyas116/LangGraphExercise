from typing import TypedDict
from langgraph.graph import StateGraph, END
import random
""""This program uses LangGraph to create an automated number guessing game where the system repeatedly guesses until it finds the correct target number, demonstrating state transitions and looping logic."""
class GameState(TypedDict):
   GuessCount: int
   TargetNumber: int
   UserGuess: int


def get_initial_state(state: GameState) -> GameState:
    return {
        "GuessCount": 0,
        "TargetNumber": 7,
        "UserGuess": 0
    }

def make_guess(state: GameState) -> GameState:
    guess = random.randint(1, 15)
    print(f"User guesses: {guess}")
    state["UserGuess"] = guess
    state["GuessCount"] += 1

    if guess < state["TargetNumber"]:
        print(" Low!")
    elif guess > state["TargetNumber"]:
        print(" High!")
    else:
        print(f"Perfect! {state}")  # ✅ FIXED

    return state

def should_continue(state: GameState) -> str:
    if state["UserGuess"] == state["TargetNumber"]:
        print(f"Correct! , should_continue {state}")
        return "END"
    elif state["UserGuess"] > state["TargetNumber"]:
        print(f"Too High! , should_continue {state}")
        return "continue"
    else:
        print(f"Too Low! , should_continue {state}")
        return "continue"
    
graph = StateGraph(GameState)


graph.add_node("setup", get_initial_state)
graph.add_node("guess", make_guess)

graph.add_edge("setup", "guess")
graph.add_conditional_edges("guess", should_continue, {
    "continue": "guess",
    "END": END
})

graph.set_entry_point("setup")
app = graph.compile()
result= app.invoke({}, config={"recursion_limit": 100})