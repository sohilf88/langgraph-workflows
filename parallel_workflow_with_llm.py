from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import TypedDict,NotRequired,Annotated,cast
import operator
# load env file
load_dotenv()

# create template

# template=PromptTemplate(template="generate good feedback about given eassy {eassy}",input_variables=["eassy"])

essay="""Artificial Intelligence Type-1 Narrow AI (weak AI): This is designed to perform a specific task with intelligence. It is termed as weak AI because it cannot perform beyond its limitations. It is trained to do a specific task. Some examples of Narrow AI are facial recognition (Siri in Apple phones), speech, and image recognition. IBM’s Watson supercomputer, self-driving cars, playing chess, and solving equations are also some of the examples of weak AI. General AI (AGI or strong AI): This type of system can handle almost all cognitive tasks as effectively as humans. Its key feature is the ability to think independently, similar to how humans do. Developing such systems is a long-term goal for many researchers. Super AI: Super AI refers to systems with intelligence that exceeds human capabilities, allowing them to perform any cognitive task better than humans. The defining traits of super AI include independent thinking, reasoning, problem-solving, judgment, planning, and communication. Creating super AI could become one of the most significant milestones in human history. Artificial Intelligence Type-2 Reactive Machines: These machines are the basic types of AI. Such AI systems focus only on current situations and react as per the best possible action. They do not store memories for future actions. IBM’s deep blue system and Google’s Alpha go are the examples of reactive machines. Limited Memory: These machines can store data or past memories for a short period of time. Examples are self-driving cars. They can store information to navigate the road, speed, and distance of nearby cars. Theory of Mind: These systems understand emotions, beliefs, and requirements like humans. These kinds of machines are still not invented and it’s a long-term goal for the researchers to create one. Self-Awareness: Self-awareness AI is the future of artificial intelligence. These machines can outsmart the humans. If these machines are invented then it can bring a revolution in human society. Conclusion Artificial Intelligence is set to spark a major transformation in human history. By enhancing human intelligence with AI, civilisation can thrive, provided that we ensure the technology remains advantageous."""
# generate prompt 
# prompt=template.invoke({"eassy":eassy})

# invoke model with structure output
model=ChatOpenAI(model="gpt-4o-mini",temperature=0.5)

# structure schema for LLM model

class StructureOutputSchema(BaseModel):
    feedback: str = Field(
        description=(
            "Provide clear, constructive feedback on the essay. "
            "Include strengths, weaknesses, and specific suggestions for improvement "
            "in areas like grammar, structure, clarity, and argument quality."
        )
    )
    score: int = Field(
        description="Score must be between 1 and 10",
        ge=1,
        le=10
    )

# LLM with structure output

strctureOutputModel=model.with_structured_output(StructureOutputSchema)



# initial state
class EssayEvaluationState(TypedDict):
    grammerFeedback:NotRequired[str]
    analysisFeedback:NotRequired[str]
    thoughtFeedback:NotRequired[str]
    essay:str
    individualScores:NotRequired[Annotated[list[int],operator.add]]
    avarageScore:NotRequired[float]
    finalFeedback:NotRequired[str]
    


# create graph
graph=StateGraph(EssayEvaluationState)

# grammer feedback node function
def grammerFeedback(state:EssayEvaluationState):
    essay=state["essay"]
    template=PromptTemplate(template="generate good feedback about given eassy's grammer and mark score between 1 to 10 {essay}",input_variables=["essay"])
    prompt=template.invoke({"essay":essay})
    response=cast(StructureOutputSchema,strctureOutputModel.invoke(prompt))
    # print(response)
    return {
        "grammerFeedback":response.feedback,
        "individualScores":[response.score]
    }

def analysisFeedback(state:EssayEvaluationState):
     essay=state["essay"]
     template=PromptTemplate(template="perform analysis and share your feedback on input {essay} and mark between 1 to 10",input_variables=["essay"])
     prompt=template.invoke({"essay":essay})
     response=cast(StructureOutputSchema,strctureOutputModel.invoke(prompt))
     return {
         "analysisFeedback":response.feedback,
         "individualScores":[response.score]
     }

def thoughtFeedback(state:EssayEvaluationState):
     essay=state["essay"]
     template=PromptTemplate(template="please share your thoughts of depth on given essay -{essay} and mark between 1 to 10 ",input_variables=["essay"])
     prompt=template.invoke({"essay":essay})
     response=cast(StructureOutputSchema,strctureOutputModel.invoke(prompt))
     return {
         "thoughtFeedback":response.feedback,
         "individualScores":[response.score]
     }


def avarageScoreFunction(state:EssayEvaluationState):
    individualScores=state["individualScores"] #type:ignore
    # print(state)
    avarage=sum(individualScores)/len(individualScores)
    return {
        "avarageScore":avarage
    }

def finalFeedback(state:EssayEvaluationState):
   
     template = PromptTemplate(
        template=(
            "Please provide final feedback based on the following:\n\n"
            "Grammar Feedback: {grammarFeedback}\n"
            "Analysis Feedback: {analysisFeedback}\n"
            "Thought Feedback: {thoughtFeedback}\n"
            "Essay: {essay}"
        ),
        input_variables=["grammarFeedback", "analysisFeedback", "thoughtFeedback", "essay"]
    )

     prompt=template.invoke({
        "grammarFeedback": state.get("grammarFeedback", ""),
        "analysisFeedback": state.get("analysisFeedback", ""),
        "thoughtFeedback": state.get("thoughtFeedback", ""),
        "essay": state["essay"]
    })

     response = model.invoke(prompt).content
     return {
         "finalFeedback":response
     }

  
# add nodes

graph.add_node("grammerFeedback",grammerFeedback)
graph.add_node("analysisFeedback",analysisFeedback)
graph.add_node("thoughtFeedback",thoughtFeedback)
graph.add_node("avarageScore",avarageScoreFunction)
graph.add_node("finalFeedback",finalFeedback)

# add edges

graph.add_edge(START,"grammerFeedback")
graph.add_edge(START,"analysisFeedback")
graph.add_edge(START,"thoughtFeedback")


graph.add_edge("grammerFeedback","avarageScore")
graph.add_edge("analysisFeedback","avarageScore")
graph.add_edge("thoughtFeedback","avarageScore")


graph.add_edge("avarageScore","finalFeedback")

graph.add_edge("finalFeedback",END)

# complie graph
parallalWorkflow=graph.compile()

# invoke workflows


result=parallalWorkflow.invoke({"essay":essay})

print(result)
# EssayWorkflowState
