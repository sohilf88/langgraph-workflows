from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import TypedDict,NotRequired,Annotated,cast
import operator
from langsmith import traceable
import os
# load env file
load_dotenv()

os.environ["LANGCHAIN_PROJECT"]="LangGraph-Tracing"

# create template

# template=PromptTemplate(template="generate good feedback about given eassy {eassy}",input_variables=["eassy"])

essay="""The internet has transformed how humanity communicates, learns, and works, connecting billions of people across the globe in an instant. What began as a tool for sharing research among scientists has evolved into the backbone of modern life — powering commerce, education, entertainment, and social connection.

Its benefits are immense. Information that once required a trip to the library is now available within seconds. Businesses reach customers worldwide without physical storefronts. Remote work, online education, and telemedicine have become possible, breaking down geographical barriers that once limited opportunity. Social media and messaging apps keep families and friends connected regardless of distance.

Yet the internet also brings real challenges. Misinformation spreads as quickly as truth, and distinguishing reliable sources from unreliable ones has become a critical skill. Privacy concerns grow as personal data is collected and traded. Excessive screen time and social media use have been linked to anxiety, reduced attention spans, and a decline in face-to-face interaction. Cybercrime, from scams to data breaches, poses ongoing risks to individuals and institutions alike.

Ultimately, the internet is a tool — its impact depends on how it is used. Used thoughtfully, it empowers education, innovation, and connection on a scale once unimaginable. Used carelessly, it can mislead, isolate, or harm. As society continues to integrate the internet deeper into daily life, cultivating digital literacy and healthy habits around its use will matter as much as the technology itself.."""
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
@traceable(name="grammer feedback")
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
@traceable(name="Analysis Feedback")
def analysisFeedback(state:EssayEvaluationState):
     essay=state["essay"]
     template=PromptTemplate(template="perform analysis and share your feedback on input {essay} and mark between 1 to 10",input_variables=["essay"])
     prompt=template.invoke({"essay":essay})
     response=cast(StructureOutputSchema,strctureOutputModel.invoke(prompt))
     return {
         "analysisFeedback":response.feedback,
         "individualScores":[response.score]
     }
@traceable(name="Thought Feedback")
def thoughtFeedback(state:EssayEvaluationState):
     essay=state["essay"]
     template=PromptTemplate(template="please share your thoughts of depth on given essay -{essay} and mark between 1 to 10 ",input_variables=["essay"])
     prompt=template.invoke({"essay":essay})
     response=cast(StructureOutputSchema,strctureOutputModel.invoke(prompt))
     return {
         "thoughtFeedback":response.feedback,
         "individualScores":[response.score]
     }

@traceable(name="individualScores")
def avarageScoreFunction(state:EssayEvaluationState):
    individualScores=state["individualScores"] #type:ignore
    # print(state)
    avarage=sum(individualScores)/len(individualScores)
    return {
        "avarageScore":avarage
    }
@traceable(name="final feedback")
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

# print(result)
print("************** grammer feedback ***********************\n")
print(result["grammerFeedback"])

print("**************** analysis Feedback ********************\n")
print(result["analysisFeedback"])
print("**************** thought Feedback **********************\n")
print(result["thoughtFeedback"])

print("****************  Scores ***********\n")
print("individual  Scores\n")
print(result["individualScores"])
print("Avarage  Scores\n")
print(result["avarageScore"])

print("##################### FINAL Feedback #####################")

print(result["finalFeedback"])
print("overall  Scores\n")
print(result["avarageScore"])

 