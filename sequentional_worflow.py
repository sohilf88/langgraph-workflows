from langgraph.graph import StateGraph,START,END
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from typing import TypedDict


load_dotenv()
# create initial state

class initial_state(TypedDict):
    question:str
    answer:str

# create openAi model

open_AI_model=OpenAI()

template=PromptTemplate(template='generate detail summary abount topic \n {topic}',input_variables=['topic']

                        )
state:initial_state={
    'question':input("ask your question to AI :-")
}



# node functions
def get_answer(state:initial_state)->initial_state:
    prompt=template.invoke({'topic':state['question']})
    response=open_AI_model.invoke(prompt)
    # print(response)
    state['answer']=response
    # print(state)
    return state


# create graph
graph=StateGraph(initial_state)

# add nodes

graph.add_node("get_answer", get_answer)

# add edges

graph.add_edge(START,"get_answer")
graph.add_edge("get_answer",END)

workflow=graph.compile()


final_response=workflow.invoke(state)

print(final_response)