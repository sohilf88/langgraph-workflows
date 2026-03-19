from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import TypedDict

# load env file
load_dotenv()

# create template

template=PromptTemplate(template="generate good feedback about given eassy {eassy}",input_variables=["eassy"])

eassy="""Artificial Intelligence Type-1 Narrow AI (weak AI): This is designed to perform a specific task with intelligence. It is termed as weak AI because it cannot perform beyond its limitations. It is trained to do a specific task. Some examples of Narrow AI are facial recognition (Siri in Apple phones), speech, and image recognition. IBM’s Watson supercomputer, self-driving cars, playing chess, and solving equations are also some of the examples of weak AI. General AI (AGI or strong AI): This type of system can handle almost all cognitive tasks as effectively as humans. Its key feature is the ability to think independently, similar to how humans do. Developing such systems is a long-term goal for many researchers. Super AI: Super AI refers to systems with intelligence that exceeds human capabilities, allowing them to perform any cognitive task better than humans. The defining traits of super AI include independent thinking, reasoning, problem-solving, judgment, planning, and communication. Creating super AI could become one of the most significant milestones in human history. Artificial Intelligence Type-2 Reactive Machines: These machines are the basic types of AI. Such AI systems focus only on current situations and react as per the best possible action. They do not store memories for future actions. IBM’s deep blue system and Google’s Alpha go are the examples of reactive machines. Limited Memory: These machines can store data or past memories for a short period of time. Examples are self-driving cars. They can store information to navigate the road, speed, and distance of nearby cars. Theory of Mind: These systems understand emotions, beliefs, and requirements like humans. These kinds of machines are still not invented and it’s a long-term goal for the researchers to create one. Self-Awareness: Self-awareness AI is the future of artificial intelligence. These machines can outsmart the humans. If these machines are invented then it can bring a revolution in human society. Conclusion Artificial Intelligence is set to spark a major transformation in human history. By enhancing human intelligence with AI, civilisation can thrive, provided that we ensure the technology remains advantageous."""
# generate prompt 
prompt=template.invoke({"eassy":eassy})

# invoke model with structure output
model=ChatOpenAI(model="gpt-4o-mini",temperature=0.5)

# structure schema for LLM model

class Structure_output_schema(BaseModel):
    feedback:str=Field(description="generate good feedback about given eassy")
    score:int=Field(description="score must be in between 1 to 10 only",ge=0,le=10)

# LLM with structure output

structure_output_model=model.with_structured_output(Structure_output_schema)

response=structure_output_model.invoke(prompt)


# initial state
class Initial_state(TypedDict):
    feedback:str
    score:int
    

# create graph
graph=StateGraph(Initial_state)

# add nodes

# add edges

# complie graph

# invoke workflows
