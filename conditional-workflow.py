from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

# State schema
class ChatbotSupport(TypedDict):
    question: int
    answer: str

# Take input
userInput = int(input("Enter option:\n1. Internet issue\n2. Billing issue\n3. Customer support\n"))

# Step 1: Store question
def userQuestion(state: ChatbotSupport):
    state["question"] = userInput
    return state

# Step 2: Router (decision node)
def router(state: ChatbotSupport) -> Literal["internetSupport", "billingIssue", "customerSupport"]:
    if state["question"] == 1:
        return "internetSupport"
    elif state["question"] == 2:
        return "billingIssue"
    else:
        return "customerSupport"

# Step 3: Handlers
def internetSupport(state: ChatbotSupport):
    state["answer"] = "You selected Internet Support"
    return state

def billingIssue(state: ChatbotSupport):
    state["answer"] = "You selected Billing Issue"
    return state

def customerSupport(state: ChatbotSupport):
    state["answer"] = "You selected Customer Support"
    return state

# Build graph
graph = StateGraph(ChatbotSupport)

graph.add_node("userQuestion", userQuestion)
graph.add_node("internetSupport", internetSupport)
graph.add_node("billingIssue", billingIssue)
graph.add_node("customerSupport", customerSupport)

# Flow
graph.add_edge(START, "userQuestion")
graph.add_conditional_edges("userQuestion", router)

graph.add_edge("internetSupport", END)
graph.add_edge("billingIssue", END)
graph.add_edge("customerSupport", END)

# Compile
app = graph.compile()

# Run
response = app.invoke({"question": 0, "answer": ""})

print(response)
