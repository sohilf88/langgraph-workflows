from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict
# load entire env file

load_dotenv()

# create chat model
model=ChatOpenAI()

# define prompt
prompt=PromptTemplate(template="generate detail overview about given topic {topic}",input_variables=["topic"])
# define intial state class

class Initial_state(TypedDict):
    pass

# create graph

graph=StateGraph(Initial_state)

# create node

# create edges