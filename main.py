from transformers.agents import ReactJsonAgent
from transformers import HfApiEngine
from huggingface_hub import login
from QuestionGenerator import QuestionGenerator
from KeywordExtractor import KeywordExtractor
from ExtractPdf import extract_text_from_pdf
from dotenv import load_dotenv
from os import getenv


load_dotenv()
LOGIN_TOKEN = getenv("HF_LOGIN_TOKEN")
login(LOGIN_TOKEN)

LLM = getenv("MODEL_PHI")
llm_engine = HfApiEngine(model=LLM)

tools = [KeywordExtractor(), QuestionGenerator()]

agent = ReactJsonAgent(tools=tools, llm_engine=llm_engine)

resume = '''
Programming Languages: C++, Python, C#.
RDBMS: MySQL.
Core CS: DSA, DBMS, OS, OOP, CN.
Cloud: Azure Functions, Azure Service Bus, AWS S3.
Frameworks: .NET(WPF, ASP.NET), Flask, Streamlit.
AI: Machine Learning - Scikit learn, Deep Learning - TensorFlow, Large Language Models.
DevTools: VS Code, Git, GitHub.
'''

# resume = extract_text_from_pdf()

result = agent.run(f'''Extract keywords using KeywordExtractor tool from resume: <<<{resume}>>> and generate questions from them by passing all extracted keywords to QuestionGenerator tool.''')
print("---------------------------------------------------------")
print(result)
print("---------------------------------------------------------")