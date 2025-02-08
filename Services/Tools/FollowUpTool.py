from huggingface_hub import InferenceClient
from os import getenv
from dotenv import load_dotenv
import re
from .AnswerEvaluatorTool import AnswerEvaluator
from ..Utils.llm_cache import LLMCache

class FollowUpTool():

    def __init__(self, ScoreThreshold: int = 6):
        load_dotenv()
        self.llm_cache = LLMCache(cache_time_window=50)
        self.client = InferenceClient(api_key=getenv("HF_LOGIN_TOKEN"))
        self.answerEvaluator = AnswerEvaluator()
        self.ScoreThreshold = ScoreThreshold

    def GetFollowUpQuestion(self, Question: str, Answer: str) -> str:

        Question = "Question:\n" + Question
        Answer = "Answer:\n" + Answer

        system_prompt = f'''Imagine yourself as an INTERVIEWER and your task is to first analyse the question, it's answer provided by interviewee.
        You must ask a follow-up question based on the answer given by the user.
        Give you response delimited by triple backticks (```).
        eg.
        response: ```<Your follow-up question here>```

        Rules:
        1. YOU MUST ALWAYS FOLLOW THE ABOVE FORMAT AND THE RESPONSE SHOULD BE A NUMBER BETWEEN 0 TO 10.
        2. DON'T ADD OTHER DETAILS, JUST GIVE THE FOLLOW-UP QUESTION.
        3. Enclose your follow-up question within triple backticks (```).
        '''
        
        print("============= Generating Follow-Up Question ==============")
        print()
        print("Question: ", Question)
        print()
        print("Answer: ", Answer)
        print()
        messages = [
            ("system", system_prompt),
            ("user", f"{Question}\n{Answer}"),
        ]
        response = self.llm_cache.get_response(str(messages))

        if response is None:
            message = self.client.chat_completion(
                model=getenv("MODEL_MIXTRAL"),
                messages=messages,
                max_tokens=1000,
                temperature=0.5,
                stream=False
            )
            response = message.choices[0].message.content
            self.llm_cache.set_response(str(messages), response)
        
        print("Response: ", response)

        followUpQuestion = self.__ExtractQuestion(response)

        return followUpQuestion
    
    def __ExtractQuestion(self, response: str) -> str:
        pattern = r'```(.*?)```'
        match = re.search(pattern, response)
        if match:
            return match.group(1)
        else:
            return "I don't have any follow-up question."
        
    def AssesFollowUpQuestion(self, Question: str, Answer: str, FollowUpQuestion: str, FollowUpAnswer) -> int:
        
        context = f"Context of previous question:\nPrevious Question: {Question}\nAnswer to Previous Question: {Answer}\n\n"
        score = self.answerEvaluator.forward(question=FollowUpQuestion, answer=FollowUpAnswer, context=context)

        if score < self.ScoreThreshold:
            return 0

        return score