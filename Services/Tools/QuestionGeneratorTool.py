from transformers import Tool
from huggingface_hub import InferenceClient
from os import getenv, path
from dotenv import load_dotenv
import json
import re
from ..Utils.llm_cache import LLMCache
from ..Utils.llm import LLM

load_dotenv()
class QuestionGenerator(Tool):
    name = "QuestionGenerator"
    description = '''This tool is expert in generating questions from keywords,
                    This tool asks questions for EVERY keyword present on 3 levels of difficulty starting from easy to intermediate to hard.
                '''

    inputs = {
        "keywords": {"type": "string", "description": "keywords present in resume in string format seperated by comma"}
    }
    # input_type = "string"
    # outputs = { 
    #    "questions": {"type": "string", "description": "Questions generated from keywords in string format seperated by comma"}
    # }
    output_type = "string"

    def forward(self, keywords: str) -> str:
        # questions = []
        keywords = keywords.split(",")
        llm = LLM(model = getenv("MODEL_PHI"), max_tokens=1000, tempature=0.5, llm_cache=LLMCache(cache_time_window=50))
        system_prompt = '''Imagine yourself as an INTERVIEWER and your task is to ask 3 questions for user query, these 3 questions should be of different difficulty levels starting from intermediate to intermidiate-hard to hard and must be skill specific.
        JUST GIVE THE QUESTIONS NOT ANSWERS.
        YOUR FINAL RESPONSE SHOULD BE IN THE FOLLOWING FORMAT: {```<insert question1 here>```, ```<insert question2 here>```, ```<insert question3 here>```}
        eg. response: ```what is your name```, ```what are your hobbies```, ```where do you live```
        refer to the above format and give the response. the above example is just for reference, you should give the questions based on the user query.
        
        Rules:
        1. DON'T ADD OTHER DETAILS, JUST GIVE THE FINAL RESPONSE.
        2. REMEMBER, YOU HAVE TO GIVE 3 QUESTIONS FOR EVERY USER QUERY.
        3. Each question should be inside triple backticks (```). eg. ```sample question```
        strictly stick to the format, each question must be inside triple backticks (```).
        '''
        
        print("=============generating questions==============")
        question_set = dict()
        for keyword in keywords:

            response = llm.generate_response(system_prompt = system_prompt, user_prompt = keyword)
            questions = self.__ExtractQuestions(response)
            if len(questions) != 0:
                question_set[keyword] = questions

        questions_file_path = path.join(path.dirname(__file__), "..","questions.json")
        with open(questions_file_path, "w") as f:
            json.dump(question_set, f, indent=4)
        print("=============questions generated==============")
        return "Questions generated successfully"
        # return question_set
    
    def __ExtractQuestions(self, text: str) -> str:
        questions = re.findall(r"```(.*?)```", text, re.DOTALL)
        return questions