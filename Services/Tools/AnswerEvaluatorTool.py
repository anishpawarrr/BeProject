from transformers import Tool
from huggingface_hub import InferenceClient
from os import getenv
from dotenv import load_dotenv
import re

load_dotenv()
class AnswerEvaluator(Tool):
    name = "AnswerEvaluator"
    description = '''This tool is expert in assessing the answers of the user to the questions,
                    This tool first analyses question, compares and assesses answer to the given question.
                '''

    inputs = {
        "question": {"type": "string", "description": "Question asked by the interviewer"},
        "answer": {"type": "string", "description": "Answer given by the user"}
    }
    input_type = "string"
    outputs = { 
       "evaluation": {"type": "int", "description": "Evaluated result of the answer"}
    }
    output_type = "string"

    def forward(self, question: str, answer: str) -> int:

        question = "Question:\n" + question
        answer = "Answer:\n" + answer

        client = InferenceClient(api_key=getenv("HF_LOGIN_TOKEN"))
        system_prompt = f'''Imagine yourself as an INTERVIEWER and your task is to first analyse the question and then assess the answer given by the user.
        You must give a score to the answer based on the question asked between range 0 to 10.
        Give you response delimited by triple backticks (```).
        eg.
        response: ```6```
        YOU MUST ALWAYS FOLLOW THE ABOVE FORMAT AND THE RESPONSE SHOULD BE A NUMBER BETWEEN 0 TO 10.
        DON'T ADD OTHER DETAILS, JUST GIVE THE FINAL ANSWER.
        '''
        
        print("=============Assessing Answer==============")
        print()
        print("Question: ", question)
        print()
        print("Answer: ", answer)
        print()
        messages = [
            ("system", system_prompt),
            ("user", f"{question}\n{answer}"),
        ]
        message = client.chat_completion(
            model=getenv("MODEL_MIXTRAL"),
            messages=messages,
            max_tokens=1000,
            temperature=0.5,
            stream=False
        )
        response = message.choices[0].message.content
        print("=============Assessment Done==============")
        print("Response: ", response)
        score = self.__ExtractScore(response)
        print("Score: ", score)
        print("===========================================")
        # with open("evaluation.txt", "w") as f:
        #     f.write(str(score))
        return score
        
    
    def __ExtractScore(self, response: str) -> int:
        pattern = r'```(.*?)```'
        match = re.search(pattern, response)
        if match:
            return int(match.group(1))
        else:
            return int(response.split('```')[1][0])