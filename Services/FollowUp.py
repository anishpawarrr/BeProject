from .Tools.FollowUpTool import FollowUpTool
from .DTOs.returnDTO import ReturnDTO

class FollowUp():
    
    def __init__(self):
        self.follow_up_tool = FollowUpTool()
    
    def get_follow_up_question(self, question: str, answer: str) -> ReturnDTO:

        try:
            follow_up_question = self.follow_up_tool.GetFollowUpQuestion(Question=question, Answer=answer)
            return ReturnDTO(status=True, data=follow_up_question, message="Follow-up question generated successfully")
        except Exception as e:
            return ReturnDTO(status=False, message="Error in generating follow-up question: " + str(e))

    def asses_follow_up_question(self, question: str, answer: str, follow_up_question: str, follow_up_answer: str) -> ReturnDTO:

        try:
            score = self.follow_up_tool.AssesFollowUpQuestion(Question=question, Answer=answer, FollowUpQuestion=follow_up_question, FollowUpAnswer=follow_up_answer)
            return ReturnDTO(status=True, data=score, message="Follow-up question evaluated successfully")
        except Exception as e:
            return ReturnDTO(status=False, message="Error in evaluating follow-up question: " + str(e) )