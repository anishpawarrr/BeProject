from os import getenv
import re
from dotenv import load_dotenv
from ..Utils.llm import LLM
from .AnswerEvaluatorTool import AnswerEvaluator
from ..Utils.llm_cache import LLMCache

class FollowUpTool():
    """
    Class to perform follow-up operations with interviewee
    """

    def __init__(self, score_threshold: int = 6):
        """
        Initialize the FollowUpTool
        Args:
            score_threshold (int): The threshold score to accept the follow-up answer.
        """
        load_dotenv()
        self.__answer_evaluator = AnswerEvaluator()
        self.__score_threshold = score_threshold
        self.__llm = LLM(model = getenv("MODEL_MIXTRAL"),
                         max_tokens=1000,
                         tempature=0.5,
                         llm_cache=LLMCache(cache_time_window=50)
                         )

    def GetFollowUpQuestion(self, question: str, answer: str) -> str:

        """
        Generates a follow-up question based on the question and answer provided.
        Args:
            question (str): The question asked by the interviewer.
            answer (str): The answer given by the interviewee.
        Returns:
            str: The follow-up question.
        """

        question = "Question:\n" + question
        answer = "Answer:\n" + answer

        user_prompt = question + "\n" + answer

        system_prompt = '''Imagine yourself as an INTERVIEWER and your task is to first analyse the question, it's answer provided by interviewee.
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
        print("Question: ", question)
        print()
        print("Answer: ", answer)
        print()

        response = self.__llm.generate_response(system_prompt = system_prompt,
                                                user_prompt = user_prompt
                                                )
        print("Response: ", response)

        follow_up_question = self.__extract_question(response)
        return follow_up_question

    def __extract_question(self, response: str) -> str:

        """
        Extracts the follow-up question from the response using regex.
        Args:
            response (str): The response from the model.
        Returns:
            str: The follow-up question.
        """

        pattern = r'```(.*?)```'
        match = re.search(pattern, response, re.DOTALL)

        if match:
            return match.group(1)
        return "I don't have any follow-up question."

    def AssesFollowUpQuestion(self, question: str, answer: str, follow_up_question: str, follow_up_answer: str) -> int:

        """
        Evaluates the follow-up question based on the previous question and answer.
        Args:
            question (str): The previous question asked by the interviewer.
            answer (str): The previous answer given by the interviewee.
            follow_up_question (str): The follow-up question asked by the interviewer.
            follow_up_answer (str): The follow-up answer given by the interviewee.
        Returns:
            int: The score of the follow-up question.
        """

        context = f"Context of previous question:\nPrevious Question: {question}\nAnswer to Previous Question: {answer}\n\n"
        score = self.__answer_evaluator.get_score(question=follow_up_question,
                                                 answer=follow_up_answer,
                                                 context=context
                                                 )

        if score < self.__score_threshold:
            return 0

        return score
