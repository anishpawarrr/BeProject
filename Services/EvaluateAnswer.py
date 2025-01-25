from .Tools.AnswerEvaluatorTool import AnswerEvaluator
from .DTOs.returnDTO import ReturnDTO

class EvaluateAnswer():
    
    def __init__(self):
        self.answer_evaluator = AnswerEvaluator()
    
    def evaluate_answer(self, question: str, answer: str) -> ReturnDTO:
        
        try:
            score = self.answer_evaluator.forward(question, answer)
            return ReturnDTO(status=True, data=score, message="Answer evaluated successfully")
        except Exception as e:
            return ReturnDTO(status=False, message=str(e))
