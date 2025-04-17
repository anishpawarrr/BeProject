"""
This Module contains the controller class to generate questions from a resume.
"""

from os import getenv, path
from json import JSONDecodeError, loads
from transformers.agents import ReactJsonAgent
from transformers import HfApiEngine
from huggingface_hub import login
from dotenv import load_dotenv
from .Tools.QuestionGeneratorTool import QuestionGenerator
from .Tools.KeywordExtractorTool import KeywordExtractor
from .DTOs.returnDTO import ReturnDTO

class GenerateQuestions:

    """
    Controller class to generate questions from a resume.
    """

    def __init__(self):
        """Initializes the ```ReactJsonAgent``` class"""

        load_dotenv()

        LOGIN_TOKEN = getenv("HF_LOGIN_TOKEN")
        login(LOGIN_TOKEN)

        LLM = getenv("MODEL_PHI")
        llm_engine = HfApiEngine(model=LLM)

        tools = [KeywordExtractor(), QuestionGenerator()]
        self.agent = ReactJsonAgent(tools=tools, llm_engine=llm_engine)

        self.questions_file_path = path.join(path.dirname(__file__), "questions.json")

    def generate_questions(self, resume: str) -> ReturnDTO:

        """
        Generates questions from a resume.
        Args:
            resume (str): The resume from which questions are to be generated.
        Returns:
            ReturnDTO:
            status (bool): The status of the operation. True if successful, False if failed.
            data (dict): The questions generated in the form of <skill:list[questions]>. None if failed.
            message (str): The message of the operation. Contains the error message if failed.
        """

        try:
            result = self.agent.run(f'''Extract keywords using KeywordExtractor tool from resume: <<<{resume}>>> and generate questions from them by passing all extracted keywords to QuestionGenerator tool.''')
        except:

            return ReturnDTO(message="Error in generating questions")

        try:

            with open(self.questions_file_path, "r") as f:
                questions = loads(f.read())

            return ReturnDTO(status = True,
                             data = questions,
                             message = "Questions generated successfully"
                             )

        except FileNotFoundError:
            return ReturnDTO(message = "Error in reading questions from file")
        except JSONDecodeError:
            return ReturnDTO(message = "Error in JSON decoding")
