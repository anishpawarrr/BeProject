"""
This file contains the controller class to evaluate the answer given by the user based on the question asked.
"""

from .Tools.AnswerEvaluatorTool import AnswerEvaluator
from .DTOs.returnDTO import ReturnDTO

class EvaluateAnswer():

    """
    Controller class to evaluate the answer given by the user based on the question asked.
    """
    
    def __init__(self):
        """Initializes the ```AnswerEvaluator``` class"""
        self.answer_evaluator = AnswerEvaluator()
    
    def evaluate_answer(self, question: str, answer: str) -> ReturnDTO:
        
        """
        Evaluates the answer given by the interviewee based on the question asked.
        Args:
            question (str): The question asked by the interviewer.
            answer (str): The answer given by the interviewee.
        Returns:
            ReturnDTO:
                status (bool): The status of the operation. True if successful, False if failed.
                data (int): The score of the answer. None if failed.
                message (str): The message of the operation. Contains the error message if failed.
        """
        
        try:
            score = self.answer_evaluator.get_score(question, answer)
            return ReturnDTO(status=True, data=score, message="Answer evaluated successfully")
        except Exception as e:
            return ReturnDTO(message=str(e))
