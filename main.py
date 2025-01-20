from transformers.agents import ReactJsonAgent
from transformers import HfApiEngine
from huggingface_hub import login
from QuestionGenerator import QuestionGenerator
from KeywordExtractor import KeywordExtractor
from AnswerEvaluator import AnswerEvaluator
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
Frameworks: .NET(WPF, ASP.NET), Flask, Streamlit.
AI: Machine Learning - Scikit learn, Deep Learning - TensorFlow, Large Language Models.
'''

## resume = extract_text_from_pdf()

result = agent.run(f'''Extract keywords using KeywordExtractor tool from resume: <<<{resume}>>> and generate questions from them by passing all extracted keywords to QuestionGenerator tool.''')
print("---------------------------------------------------------")
print(result)
print("---------------------------------------------------------")

# agent = ReactJsonAgent(tools=[AnswerEvaluator()], llm_engine=llm_engine)

# question = "What is the purpose of the 'override' keyword in C# and under what circumstances would you use it?"
# answer = "The override keyword in C# is used to provide a new implementation for a method, property, indexer, or event that is defined as virtual or abstract in a base class. It allows a derived class to modify or extend the behavior of the base class method. You use override when you need polymorphism, enabling the derived class to offer a specific implementation that differs from the base class. This is essential when inheriting from an abstract class, as you must implement its abstract methods, or when you want to change the behavior of a virtual method in the base class."

# score = agent.run(f'''Assess the answer to the question: <<<{question}>>> and answer: <<<{answer}>>> using AnswerEvaluator tool.''')
# print()
# print()
# print(score)