from langgraph.graph import START,StateGraph,END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from typing import TypedDict,Annotated
# from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.runnables import RunnableConfig
load_dotenv()
import time

# create initial State

class ChatbotState(TypedDict):
   
    message:Annotated[list[BaseMessage],add_messages]
# create AI model

model=ChatOpenAI()
DB_URI = "postgresql://sohil:$ohil789SF@localhost:5432/langgraph-db?sslmode=disable"

# create graph
def chatbot(state:ChatbotState):
   message=state['message']
   response=model.invoke(message)
#    print(state)
   
   return {'message':[response]}
graph=StateGraph(ChatbotState)


# define checkpoint

# checkpointer=MemorySaver()

# create node
graph.add_node('chatbot',chatbot)
# create edge
graph.add_edge(START,"chatbot")
graph.add_edge('chatbot',END)

# compile graph
with PostgresSaver.from_conn_string(DB_URI) as checkpointer_postgres:
    checkpointer_postgres.setup() # creates the tables; needed the first time
    workflow=graph.compile(checkpointer=checkpointer_postgres)
    while True:
        thread=1
        config:RunnableConfig={"configurable":{"thread_id":thread}}
        user_input=input("Enter your question.... \n")
        EXIT_WORDS = {"exit", "quit", "stop", "abort","bye","quite"}
    
        if user_input.lower() in EXIT_WORDS:
            print("shuting down now bye .....")
            break

        initial_state:ChatbotState={'message':[HumanMessage(content=user_input)]}

    # response = workflow.invoke(initial_state,config=config)
    # added streaming in chatbot

        response = workflow.stream(initial_state,config=config,stream_mode='messages')
    # print("AI Response:- "+ response['message'][-1].content)
        for message_chunk,metadata in response:
            if isinstance(message_chunk, BaseMessage) and isinstance(message_chunk.content, str):
                print(message_chunk.content, end="", flush=True)
        print("\n")
    time.sleep(2)






