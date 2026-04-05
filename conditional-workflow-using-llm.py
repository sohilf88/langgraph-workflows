from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal,Annotated,NotRequired
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field,SecretStr
from dotenv import load_dotenv

import os
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
# building feedback system, which can take user review and check it's sentiment and replied based on feedback
print(OPENAI_API_KEY)
#create model
model=ChatOpenAI(model="gpt-4o-mini",temperature=0.5,api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None)


feedbackTemplate=PromptTemplate(template="based upon user review generate feedback for user {review}",input_variables=["review"])

class UserReview(BaseModel):
    review: Annotated[
        str,
        Field(
            description="Original user review text (must not be modified)"
        )
    ]

    feedback: Annotated[
        Literal["positive", "negative"],
        Field(
            description="Sentiment classification derived from the review"
        )
    ]

    issueType: Annotated[
        str,
        Field(
            description="Identified issue category from the review (e.g., delivery, quality, pricing)"
        )
    ]

    urgency: Annotated[
        Literal["low", "medium", "high"],
        Field(
            description="Urgency level inferred from the review; low for positive reviews"
        )
    ]

    userTone: Annotated[
        Literal["happy", "sad", "frustrated", "angry", "neutral"],
        Field(
            description="Emotional tone of the user inferred from the review"
        )
    ]


user_input=input("please share your feedback '\n")

structureOutput=model.with_structured_output(UserReview)

# response=structureOutput.invoke(user_input)

class userFeedback(TypedDict):
    userReview:dict
    finalFeedback:NotRequired[str]

# create graph

graph=StateGraph(userFeedback)

# 
def userReview(state:userFeedback)->userFeedback:
    response=structureOutput.invoke(user_input)
    print(response)
    state["userReview"]=response
    return state
    
def positiveFeedback(state:userFeedback):
    userReview=state["userReview"]
    prompt=feedbackTemplate.invoke({"review":userReview})
    response=model.invoke(prompt).content
    print(response)
    state["finalFeedback"]=response
    return state
    
  

def negatvieFeedback(state:userFeedback):
     userReview=state["userReview"]
     prompt=feedbackTemplate.invoke({"review":userReview})
     response=model.invoke(prompt).content
     print(response)
     state["finalFeedback"]=response
     return state
    
# find user feedback either postive or negative

def UserFeedbackRouter(state:userFeedback)->Literal["negatvieFeedback","postiveFeedback"]:
    feedback=state["userReview"]["feedback"]
    if(feedback=="positive"):
        return "postiveFeedback"
    else:
        return "negatvieFeedback"

# create nodes
graph.add_node("userReview",userReview)

graph.add_node("postiveFeedback",positiveFeedback)
graph.add_node("negatvieFeedback",negatvieFeedback)

# add edges

graph.add_edge(START,"userReview")
graph.add_conditional_edges("userReview",UserFeedbackRouter)
graph.add_edge("postiveFeedback",END)
graph.add_edge("negatvieFeedback",END)

workflow=graph.compile()

response=workflow.invoke({"userFeedback":user_input})

print(response)