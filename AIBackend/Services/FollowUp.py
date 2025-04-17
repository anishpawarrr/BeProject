"""
This Module contains the controller class to generate and evaluate follow-up questions.
"""

from .Tools.FollowUpTool import FollowUpTool
from .DTOs.returnDTO import ReturnDTO

class FollowUp():

    """
    Controller class to generate and evaluate follow-up questions.
    """

    def __init__(self):
        """Initializes the ```FollowUpTool``` class"""
        self.__follow_up_tool = FollowUpTool()

    def get_follow_up_question(self, question: str, answer: str) -> ReturnDTO:

        """
        Generate follow-up question based on the previous question and answer.
        Args:
            question (str): The previous question asked by the interviewer.
            answer (str): The previous answer given by the interviewee.
        Returns:
            ReturnDTO:
                status (bool): The status of the operation. True if successful, False if failed.
                data (str): The follow-up question generated. None if failed.
                message (str): The message of the operation. Contains the error message if failed.
        """

        try:
            follow_up_question = self.__follow_up_tool.GetFollowUpQuestion(question=question, answer=answer)
            return ReturnDTO(status=True,
                             data=follow_up_question,
                             message="Follow-up question generated successfully"
                             )
        except Exception as e:
            return ReturnDTO(message="Error in generating follow-up question: " + str(e))

    def asses_follow_up_question(self, question: str,
                                 answer: str,
                                 follow_up_question: str,
                                 follow_up_answer: str) -> ReturnDTO:

        """
        Assess the follow-up question based on the previous question, answer, follow-up question, and follow-up answer.
        Args:
            question (str): The previous question asked by the interviewer.
            answer (str): The previous answer given by the interviewee.
            follow_up_question (str): The follow-up question generated.
            follow_up_answer (str): The expected answer to the follow-up question.
        Returns:
            ReturnDTO:
                status (bool): The status of the operation. True if successful, False if failed.
                data (int): The score of the follow-up question. None if failed.
                message (str): The message of the operation. Contains the error message if failed.
        """
        try:
            score = self.__follow_up_tool.AssesFollowUpQuestion(question=question,
                                                                answer=answer,
                                                                follow_up_question=follow_up_question,
                                                                follow_up_answer=follow_up_answer
                                                                )
            return ReturnDTO(status=True,
                             data=score,
                             message="Follow-up question evaluated successfully"
                             )
        except Exception as e:
            return ReturnDTO(message="Error in evaluating follow-up question: " + str(e))
