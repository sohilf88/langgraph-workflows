# first workflow

# bmi calculator
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Optional

# define state
class Bmi(TypedDict):
    weight_kg:float
    height_m:float
    bmi: float
    ratio:Optional[str]


def calculate_bmi(state:Bmi) ->Bmi:
    weight = state['weight_kg']
    height=state['height_m']
    bmi=weight/(height**2)

    state["bmi"]=round(bmi,2)

    return state


# Underweight: Below 18.5
# Healthy Weight: 18.5–24.9
# Overweight: 25.0–29.9
# Obesity: 30.0 or higher
def bmi_ratio(state:Bmi) ->Bmi:
    if(state["bmi"]>25):
        state["ratio"]="over weight"
    if(state["bmi"]<25):
       state["ratio"]="under weight"
    return state




# define graph
graph=StateGraph(Bmi)


# add nodes to graph

graph.add_node("calculate_bmi",calculate_bmi)
graph.add_node("bmi_ratio",bmi_ratio)



# add edge to graph

graph.add_edge(START,"calculate_bmi")
graph.add_edge("calculate_bmi","bmi_ratio")
graph.add_edge("bmi_ratio",END)

# compile the graph
graph_workflow=graph.compile()


# execute the graph
response=graph_workflow.invoke({"weight_kg":90.5,"height_m":1.650})

print(response)