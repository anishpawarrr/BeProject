from .Tools.QuestionGeneratorTool import QuestionGenerator
from .Tools.KeywordExtractorTool import KeywordExtractor
from .DTOs.returnDTO import ReturnDTO
from transformers.agents import ReactJsonAgent
from transformers import HfApiEngine
from huggingface_hub import login
from dotenv import load_dotenv
from os import getenv, path
from json import JSONDecodeError, loads

class GenerateQuestions:

    def __init__(self):

        load_dotenv()

        LOGIN_TOKEN = getenv("HF_LOGIN_TOKEN")
        login(LOGIN_TOKEN)

        LLM = getenv("MODEL_PHI")
        llm_engine = HfApiEngine(model=LLM)

        tools = [KeywordExtractor(), QuestionGenerator()]

        self.agent = ReactJsonAgent(tools=tools, llm_engine=llm_engine)

        self.questions_file_path = path.join(path.dirname(__file__), "questions.json")
    
    def generate_questions(self, resume: str) -> ReturnDTO:
                
        try:
            result = self.agent.run(f'''Extract keywords using KeywordExtractor tool from resume: <<<{resume}>>> and generate questions from them by passing all extracted keywords to QuestionGenerator tool.''')
        except:

            return ReturnDTO(status=False, message="Error in generating questions")
        
        try:

            with open(self.questions_file_path, "r") as f:
                questions = loads(f.read())

            return ReturnDTO(status=True, data=questions, message="Questions generated successfully")

        except FileNotFoundError:
            return ReturnDTO(status=False, message="Error in reading questions from file")
        except JSONDecodeError:
            return ReturnDTO(status=False, message="Error in JSON decoding")