from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,NotRequired
# load entire env file
# create parallal workflow without LLM Required
load_dotenv()

# create chat model
# model=ChatOpenAI()

# define prompt
# prompt=PromptTemplate(template="generate detail overview about given topic {topic}",input_variables=["topic"])
# define intial state class

class Initial_state(TypedDict):
    runs:int
    strike_rate:NotRequired[float]
    total_fours:int
    total_sixes:int
    boundary_ball_percentage:NotRequired[float]
    total_balls_played:int
    summary:NotRequired[str]

score_card:Initial_state={
    "runs":98,
    "total_fours":10,
    "total_sixes":5,
    "total_balls_played":120

}

def strike_rate(state:Initial_state):
     strike_rate=(state["runs"]/state["total_balls_played"])*100
     state["strike_rate"]=strike_rate
     return {"strike_rate":round(strike_rate,2)}

def boundary_percentage(state:Initial_state):
    boundarysPercent=((state["total_fours"]*4 + state["total_sixes"]*6)/state["runs"])*100
    state["boundary_ball_percentage"]=boundarysPercent
    return {"boundary_ball_percentage":round(boundarysPercent,3)}

def summary(state:Initial_state):
    summary=f"this is summary total runs {state['runs']} with strike rate {state['strike_rate']}"#type:ignore
    state["summary"]=summary
    return {"summary":summary}
# create graph

graph=StateGraph(Initial_state)

# create node
graph.add_node("strike_rate",strike_rate)
graph.add_node("boundary_percentage",boundary_percentage)
graph.add_node("summary",summary)

# create edges

graph.add_edge(START,"strike_rate")
graph.add_edge(START,"boundary_percentage")
graph.add_edge("boundary_percentage","summary")
graph.add_edge("strike_rate","summary")
graph.add_edge("summary",END)

# compile the graph

parallel_workflow=graph.compile()

response=parallel_workflow.invoke(score_card)

print(response)