# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import PromptTemplate
# from langgraph.graph import StateGraph,START,END
# from typing import TypedDict,NotRequired
# from dotenv import load_dotenv

# # load env file

# load_dotenv()

# # create initial state

# class Initial_state(TypedDict):
#     input:str
#     output:NotRequired[str]

# #call openAI LLM
# template=PromptTemplate(template="give me detail information about {input}", input_variables=["input"])
# user_intput=input("enter your detail \n")
# prompt=template.invoke({"input":user_intput})

# print(prompt)
# model=ChatOpenAI()

# def callingAI(state:Initial_state)->Initial_state:
#     response=model.invoke(prompt).content
#     print(type(response))
#     state["output"]=response
#     return state
    


# # create graph
# graph=StateGraph(Initial_state)

# # add node
# graph.add_node("ai_calling",callingAI)


# # add edge

# graph.add_edge(START,"ai_calling")
# graph.add_edge("ai_calling",END)
# # compile
# workflow=graph.compile()

# "invoke it"

# response=workflow.invoke({"input":"icream"})

# print(response)


from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, NotRequired
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define Graph State
class GraphState(TypedDict):
    input: str
    output: NotRequired[str]

# Initialize LLM
model = ChatOpenAI()

# Prompt template
prompt_template = PromptTemplate(
    template="Give detailed information about {input}",
    input_variables=["input"]
)

# Node function
def call_llm(state: GraphState) -> GraphState:

    prompt = prompt_template.invoke({"input": state["input"]})
    
    response = model.invoke(prompt)

    return {
        "output": response.content
    }

# Create Graph
graph = StateGraph(GraphState)

# Add node
graph.add_node("llm_call", call_llm)

# Add edges
graph.add_edge(START, "llm_call")
graph.add_edge("llm_call", END)

# Compile graph
workflow = graph.compile()

# User input
user_input = input("Enter your topic: ")

# Run workflow
result = workflow.invoke({"input": user_input})

print("\nResponse:\n")
print(result["output"])
