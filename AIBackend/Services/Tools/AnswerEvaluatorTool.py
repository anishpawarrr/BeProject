from os import getenv
import re
from dotenv import load_dotenv
from ..Utils.llm_cache import LLMCache
from ..Utils.llm import LLM

load_dotenv()
class AnswerEvaluator():
    """
    Class to evaluate the answer given by the user based on the question asked.
    """

    def get_score(self, question: str, answer: str, context: str = "") -> int:
        """
        Assess the answer given by the user based on the question asked and the context.
        Args:
            question (str): The question asked by the interviewer.
            answer (str): The answer given by the user.
            context (str): The context / previous discussion of the question and answer.
        Returns:
            int: The score given to the answer based on the question asked.
        """
        question = "Question:\n" + question
        answer = "Answer:\n" + answer

        llm = LLM(model = getenv("MODEL_MIXTRAL"),
                  max_tokens=1000,
                  tempature=0.1,
                  llm_cache=LLMCache(cache_time_window=50)
                  )

        system_prompt = '''Imagine yourself as an INTERVIEWER and your task is to first analyse the question and then assess the answer given by the user.
        You must give a score to the answer based on the question asked between range 0 to 10.
        Give you response delimited by triple backticks (```).
        eg.
        response: ```6``` <ADDITIONAL COMMENTS>

        Rules:
        1. YOU MUST ALWAYS FOLLOW THE ABOVE FORMAT AND THE RESPONSE SHOULD BE A NUMBER BETWEEN 0 TO 10.
        2. DON'T ADD ADDITIONAL INFORMATION BETWEEN TRIPLE BACKTICKS, ALWAYS FOLLOW THR FORMAT: ```INT```.
        3. ALWAYS STICK TO THE FORMAT, OTHERWISE THE SYSTEM WILL NOT BE ABLE TO EVALUATE THE RESPONSE.
        '''
        print("=============Assessing Answer==============")
        print()
        print("Context: ", context)
        print()
        print("Question: ", question)
        print()
        print("Answer: ", answer)
        print()

        user_query = f"{question}\n{answer}"

        response = llm.generate_response(system_prompt = system_prompt,
                                         user_prompt = user_query,
                                         context = context
                                         )

        score = self.__ExtractScore(response)

        print("=============Assessment Done==============")
        print("Response: ", response)
        print("Score: ", score)
        print("===========================================")

        return score

    def __ExtractScore(self, response: str) -> int:
        """
        Regex operation to extract the score from the response.
        Args:
            response (str): The response from the model.
        Returns:
            int: The score extracted from the response.
        """
        pattern = r'```(.*?)```'
        match = re.search(pattern, response)
        if match:
            return int(match.group(1))
        return int(response.split('```')[1][0])
