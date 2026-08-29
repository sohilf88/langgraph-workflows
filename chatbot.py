from langgraph.graph import START,StateGraph,END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
load_dotenv()
import time

# create initial State

class ChatbotState(TypedDict):
   
    message:Annotated[list[BaseMessage],add_messages]
# create AI model

model=ChatOpenAI()

# create graph
def chatbot(state:ChatbotState):
   message=state['message']
   response=model.invoke(message)
#    print(state)
   
   return {'message':[response]}
graph=StateGraph(ChatbotState)


# define checkpoint

checkpointer=MemorySaver()

# create node
graph.add_node('chatbot',chatbot)
# create edge
graph.add_edge(START,"chatbot")
graph.add_edge('chatbot',END)

# compile graph

workflow=graph.compile(checkpointer=checkpointer)






while True:
    thread=1
    config:RunnableConfig={"configurable":{"thread_id":thread}}
    user_input=input("Enter your question.... \n")
    EXIT_WORDS = {"exit", "quit", "stop", "abort"}
    
    if user_input.lower() in EXIT_WORDS:
        print("shuting down now bye .....")
        break
    initial_state:ChatbotState={'message':HumanMessage(content=user_input)}
    response = workflow.invoke(initial_state,config=config)
    print("AI Response:- "+ response['message'][-1].content)
    time.sleep(2)