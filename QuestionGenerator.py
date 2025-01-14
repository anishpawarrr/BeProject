from transformers import Tool
from huggingface_hub import InferenceClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()
class QuestionGenerator(Tool):
    name = "QuestionGenerator"
    description = '''This tool is expert in generating questions from keywords,
                    This tool asks questions for EVERY keyword present on 3 levels of difficulty starting from easy to intermediate to hard.
                '''

    inputs = {
        "keywords": {"type": "string", "description": "keywords present in resume in string format seperated by comma"}
    }
    input_type = "string"
    outputs = { 
       "questions": {"type": "string", "description": "Questions generated from keywords in string format seperated by comma"}
    }
    output_type = "string"

    def forward(self, keywords: str) -> str:
        # questions = []
        keywords = keywords.split(",")
        client = InferenceClient(api_key="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")
        system_prompt = f'''Imagine yourself as an INTERVIEWER and your task is to ask 3 questions for user query, these 3 questions should be of different difficulty levels starting from intermediate to intermidiate-hard to hard.
        JUST GIVE THE QUESTIONS NOT ANSWERS.
        YOUR FINAL RESPONSE SHOULD BE IN THE FOLLOWING FORMAT: Q1, Q2, Q3
        DON'T ADD OTHER DETAILS, JUST GIVE THE FINAL ANSWER.
        '''
        
        print("=============generating questions==============")
        with open("questions.txt", "w") as f:
            pass
        for keyword in keywords:
            messages = [
                ("system", system_prompt),
                ("user", f"{keyword}"),
            ]
            message = client.chat_completion(
                model=getenv("MODEL_PHI"),
                messages=messages,
                max_tokens=1000,
                temperature=0.5,
                stream=False
            )
            with open("questions.txt", "a") as f:
                f.write(f"{keyword}: \n{message.choices[0].message.content}\n\n")
        print("=============questions generated==============")
        return "Questions generated successfully"