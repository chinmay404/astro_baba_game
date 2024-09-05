import os
import json
from flask import session
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Response_format(BaseModel):
    PREDICTIONS: str = Field(description="Your Predictions  ")
    IMAGE_DESCRIPTION: str = Field(
        description="Your Image Description")


class AIResponse(object):
    def __init__(self):
        os.environ["GROQ_API_KEY"] = "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"
        self.full_prediction = []
        self.parser = JsonOutputParser(pydantic_object=Response_format)
        self.history = ChatMessageHistory()
        self.name = None
        self.predictions = ""
        self.image_description = ""
        self.date_of_birth = None
        self.birth_place = None
        self.gender = None
        self.period = None
        self.fields = None
        self.llm = ChatGroq(
            model="llama-3.1-70b-versatile",
            temperature=0.9,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def get_response(self, session):
        # Access values from the session
        self.period = session.get('period', '3 Months')
        self.fields = session.get('fields', 'Health, Career, Relationship')
        self.name = session.get('name', None)
        self.date_of_birth = session.get('dob', None)
        self.birth_place = session.get('birthplace', None)
        self.gender = session.get('gender', None)

        if self.name and self.date_of_birth and self.birth_place and self.gender:
            if True:
                prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            """
                            
                            
                            You are an astrologist. Your job is to predict the future of the user based on the following fields:
                            {fields}.
                            **PREDICTION INSTRUCTIONS**
                            - Your prediction period must be the next {period}.
                            - Give Your Predictions Without Any Bias.
                            - Dont add Lines like this "Based on the provided birth details, here are the predictions for the next...."
                            
                            **IMAGE INSTRUCTIONS** : 
                            - Give A Picture description as your all Predictions should club into one picture.
                            - With Symbolic Of All your prediction as if anyone sees the image it could guess your predictions even if blind person could also imagine it. 
                            - Picture Must Description must be very Detailed.
                            - Dont Add Username Or Any details into description.
                            - You dont have to genrate ANy Image Just Have To describe it in very detailed manner.
                            - Dont Point Any Description to your predictions like this 
                            exmaple: 
                            "this image is subtle and in the background, indicating that these issues will not be severe."
                            it should be only : 
                            "this image is subtle and in the background,"
                            
                            **STRICTLY**:  
                            - give your response format no text outside this format
                            - {format_instructions}

                            below are user details : 
                            Name: {name}
                            Date of Birth: {date_of_birth}
                            Birthplace: {birth_place}
                            Gender: {gender}
                            
                            
                            """,
                        ),
                        ("human", "go ahed"),
                    ]
                )
                chain = prompt | self.llm | self.parser
                ai_response = chain.invoke(
                    {
                        "period": self.period,
                        "fields": self.fields,
                        "name": self.name,
                        "date_of_birth": self.date_of_birth,
                        "birth_place": self.birth_place,
                        "gender": self.gender,
                        "history": self.history,
                        "format_instructions": self.parser.get_format_instructions(),
                    }
                )
                self.predictions = ai_response.get('PREDICTIONS', None)
                self.image_description = ai_response.get(
                    'IMAGE_DESCRIPTION', None)
                print(self.predictions)
                session['PREDICTIONS'] = self.predictions
                session['IMAGE_DESCRIPTION'] = self.image_description
                return [self.predictions, self.image_description]
            else:
                return "You have hidden your dates or name. Is there something wrong? Please fill in the missing information <a href=''></a>"

    def chat_chain(self, session, human_message):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """     
                            
                            You are an astrologist named "BABA ASTRO". Your job is to converse with humans as you have already provided their
                            future predictions.
                            keep your humour level full , add some slangs and make coversation like a astrolgist form fairy tale.
                            Use "Chin Tapak Dum Dum " as funny memes which is trending now in your reponse where you can use it at start or where you feel comfitable.
                            Previous Prediction: {prediction}
                            
                            Human Details (if needed): 
                            Name: {name}
                            Date of Birth: {date_of_birth}
                            Birthplace: {birth_place}
                            Gender: {gender}
                            
                            Your Previous Chat With USer : 
                            {history}
                            
                            Below is Human Question : 
                            {human_message}
                            
                            """,
                ),
            ]
        )
        print(self.history)
        print(human_message)
        chain = prompt | self.llm
        ai_response = chain.invoke(
            {
                "prediction": self.predictions,
                "name": self.name,
                "date_of_birth": self.date_of_birth,
                "birth_place": self.birth_place,
                "gender": self.gender,
                "history": self.history,
                "human_message":human_message,
            }
        )
        self.history.add_user_message(human_message)
        self.history.add_ai_message(ai_response.content)
        self.full_prediction.append(ai_response.content)
        return ai_response.content
