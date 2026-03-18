from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, NotRequired
from dotenv import load_dotenv

# load end
load_dotenv()

# initial state
class Initial_state(TypedDict):
    input:str
    output:str
    blog:str
    score:NotRequired[int]

# generate prompt 
prompt_template=PromptTemplate(template="kindly give the detail about {topic_input}",input_variables=["topic_input"])

second_prompt_template=PromptTemplate(template="generate summary in 5 point only for given topic {topic_input}",input_variables=["topic_input"])

generate_score_template=PromptTemplate(template="give score between 1 to 5 where 1 is very bad and 5 is very good  {blog}",input_variables=["blog"])


# create model
model=ChatOpenAI()

# create graph
graph=StateGraph(Initial_state)

# generate blog from input topic
def generate_blog(state:Initial_state)->Initial_state:
    prompt=prompt_template.invoke({"topic_input":state["input"]})
    response=model.invoke(prompt).content
    state["blog"]=str(response) #avoid type error in typeDict hence converted to str
    return state
# generate blog with output 
def generate_output_with_blog_summary(state:Initial_state)->Initial_state:
    prompt=second_prompt_template.invoke({"topic_input":state["blog"]})
    response=model.invoke(prompt).content
    state["output"]=str(response) #avoid type error in typeDict hence converted to str
    return state
# generate score

def generate_score(state:Initial_state)->Initial_state:
    prompt=generate_score_template.invoke({"blog":state["blog"]})
    score=model.invoke(prompt).content
    state["score"]=score #avoid type error in typeDict hence converted to str

    return state
# add node
graph.add_node("generate_blog",generate_blog)
graph.add_node("generate_output_with_blog_summary",generate_output_with_blog_summary)
graph.add_node("generate_score",generate_score)

# add edges
graph.add_edge(START,"generate_blog")
graph.add_edge("generate_blog","generate_output_with_blog_summary")
graph.add_edge("generate_output_with_blog_summary","generate_score")
graph.add_edge("generate_score",END)

# compile workflow

workflow=graph.compile()

# invoke workflow
user_input=input("Enter your topic:- \n")



response=workflow.invoke({"input":user_input})

print(response)