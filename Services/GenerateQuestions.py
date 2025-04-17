"""
This Module contains the controller class to generate questions from a resume.
"""

import json
from os import getenv, path
from json import JSONDecodeError, loads
import re
import time
# from transformers.agents import ReactJsonAgent
# from transformers import HfApiEngine
# from smolagents import CodeAgent, HfApiModel, ToolCallingAgent
# from huggingface_hub import login
from dotenv import load_dotenv
# from .Tools.QuestionGeneratorTool import QuestionGenerator
# from .Tools.KeywordExtractorTool import KeywordExtractor
from .DTOs.returnDTO import ReturnDTO
from .Utils.llm import LLM

class GenerateQuestions:

    """
    Controller class to generate questions from a resume.
    """

    def __init__(self):
        """Initializes the ```ReactJsonAgent``` class"""

        load_dotenv()

        # LOGIN_TOKEN = getenv("HF_LOGIN_TOKEN")
        # login(LOGIN_TOKEN)

        # LLM_model = getenv("MODEL_PHI")
        # llm_engine = HfApiModel(model_id=LLM_model, token = LOGIN_TOKEN)

        self.__llm = LLM(model=getenv("MODEL_LLAMA"), tempature=0.5)

        # tools = [QuestionGenerator()]
        # # tools = [KeywordExtractor(), QuestionGenerator()]
        # self.agent = ToolCallingAgent(tools=tools, model=llm_engine)

        self.questions_file_path = path.join(path.dirname(__file__), "questions.json")

    def generate_questions(self, resume: str, company_name: str = "") -> ReturnDTO:

        """
        Generates questions from a resume.
        Args:
            resume (str): The resume from which questions are to be generated. w
        Returns:
            ReturnDTO:
            status (bool): The status of the operation. True if successful, False if failed.
            data (dict): The questions generated in the form of <skill:list[questions]>. None if failed.
            message (str): The message of the operation. Contains the error message if failed.
        """

        print("Generating questions from resume...")

        try:
            # result = self.agent.run(f'''Extract keywords using KeywordExtractor tool from resume: <<<{resume}>>> and generate questions from them by passing all extracted keywords to QuestionGenerator tool.''')
            # result = self.agent.run(f'''Extract keywords from resume: <<<{resume}>>> and generate questions from them by passing all extracted keywords to QuestionGenerator tool.''')
            fields = self.__extract_fields(resume)

            questions = self.__generate_questions(fields, company_name=company_name)
            
            return ReturnDTO(status = True,
                             data = questions,
                             message = "Questions generated successfully"
                             )

        except FileNotFoundError:
            return ReturnDTO(message = "Error in reading questions from file")
        except JSONDecodeError:
            return ReturnDTO(message = "Error in JSON decoding")
        except Exception as e:
            return ReturnDTO(message= str(e))

        
        

    def __generate_questions(self, keywords: list[str], company_name: str = "") -> dict:
        """
        Generates questions from keywords.
        Args:
            keywords (list[str]): The keywords from which questions are to be generated.
        Returns:
            dict: The questions generated in the form of <skill:list[questions]>.
        """

        system_prompt = '''Imagine yourself as an INTERVIEWER and your task is to ask 3 questions for user query, these 3 questions should be of different difficulty levels starting from intermediate to intermidiate-hard to hard and must be skill specific.
        JUST GIVE THE QUESTIONS NOT ANSWERS.
        YOUR FINAL RESPONSE SHOULD BE IN THE FOLLOWING FORMAT: {```<insert question1 here>```, ```<insert question2 here>```, ```<insert question3 here>```}
        eg. response: ```what is your name```, ```what are your hobbies```, ```where do you live```
        refer to the above format and give the response. the above example is just for reference, you should give the questions based on the user query.
        You must ask questions which are related to the user info passed in the query.
        
        Rules:
        1. DON'T ADD OTHER DETAILS, JUST GIVE THE FINAL RESPONSE.
        2. REMEMBER, YOU HAVE TO GIVE 3 QUESTIONS FOR EVERY USER QUERY.
        3. Each question should be inside triple backticks (```). eg. ```sample question```
        strictly stick to the format, each question must be inside triple backticks (```).
        '''

        question_set = dict()

        context = "Generate questions by keeping in mind that the user is applying for a job at " + company_name + ".\n Ask Questions which align with company's work and candidates info." if company_name != "" else ""

        for keyword in keywords:

            response = self.__llm.generate_response(system_prompt = system_prompt, user_prompt = keyword, context=context)
            time.sleep(1)
            questions = self.__ExtractQuestions(response)
            if len(questions) != 0:
                question_set[keyword] = questions

        questions_file_path = self.questions_file_path
        with open(questions_file_path, "w") as f:
            json.dump(question_set, f, indent=4)
        print("=============questions generated==============")
        return question_set
        # return question_set
    
    def __ExtractQuestions(self, text: str) -> str:
        questions = re.findall(r"```(.*?)```", text, re.DOTALL)
        return questions


    def __extract_fields(self, resume: str) -> list:
        """
        Extracts fields from a resume.
        Args:
            resume (str): The resume from which fields are to be extracted.
        Returns:
            list: The fields extracted from the resume.
        """

        system_prompt = """
        You are an expert interviewer and your task is to extract fields from the resume which are important so that questions can be generated from them.
        The fields can be:
        - Skills
        - Experience
        - Education
        - Projects
        - Certifications
        - Achievements
        - Interests
        - Languages
        - Awards
        - Publications
        - Extracurricular activities

        YOUR FINAL RESPONSE SHOULD BE IN THE FOLLOWING FORMAT: {```<insert field1:description_present_in_resume here>```, ```<insert field1:description_present_in_resume here>```, ```<insert field2:description_present_in_resume here>```}

        Rules:
        1. DON'T ADD OTHER DETAILS, JUST GIVE THE FINAL RESPONSE.
        2. Each field should be inside triple backticks (```). eg. ```<field_and_its_complete_description>```
        strictly stick to the format, each question must be inside triple backticks (```).
        3. Your task isn't to generate questions, just extract the fields from the resume.
        4. Include complete description of the field in the response.
        5. If a above mentioned field is not present in the resume, don't include it in the response.
        """

        user_prompt = "Resume:\n" + resume + "\n"

        response = self.__llm.generate_response(system_prompt = system_prompt, user_prompt = user_prompt)
        fields = self.__regex_extract_questions(response)

        return fields


        


    def __regex_extract_questions(self, text: str) -> list[str]:
        """
        Extracts questions from a text using regex.
        Args:
            text (str): The text from which questions are to be extracted.
        Returns:
            list[str]: The questions extracted from the text.
        """

        questions = re.findall(r"```(.*?)```", text, re.DOTALL)
        return questions

# resume = """
# Education
# Pune Institute of Computer Technology, Savitribai Phule Pune University | Pune, India June 2021 – June 2025
# ● Bachelor of Engineering - Information Technology 8.9 CGPA
# ● Bachelor of Engineering - Honors in Data Science
# Experience
# Cloud and Backend Developer Intern Oct 2023 - July 2024
# SmartAI PLS | Singapore
# ● Developed an AI-based Intelligent Document Processing system to automate invoice management and reconciliation,
# reducing processing time and increasing accuracy.
# ● Conducted comprehensive market research for 2 months and prepared surveys.
# ● Designed the product architecture, utilizing Azure cloud infrastructure for serverless backend of the application.
# Software Development Intern July 2023 - Jan 2024
# Intangles | Pune, India
# ● Updated Orchestra, a software which is used for boot and application loading, and simulation.
# ● Integrated it with AWS S3, Google Cloud Platform, developed a background process, and minimized manual labor.
# Projects
# Context-Aware Email Routing System - GenAI
# ● An intelligent email classification system that analyzes content, context, and sentiment to route emails to the
# appropriate departments and individuals with an accuracy of 87%.
# ● Enabled user feedback mechanism on email routing, ensuring adaptability to any organizational structure.
# ● Implemented a scalable solution using Python, RabbitMQ, IMAP, SMTP, Haystack, Hugging Face, Mixtral 8x7B LLM,
# Retrieval Augmented Generation, and encryption for efficient processing, and secure routing.
# DriveSync - Process Automation
# ● Used by 20+ production line machines to Synchronize code updates directly from a Google Drive folder, eliminating
# manual deployments on production line machines by 100% using .NET, C#, Python, Google Cloud Platform.
# ● Designed a user-friendly interface for production line personnel that leverages Google Drive, multithreading, Depth
# First Search to minimize runtime and cloud resources.
# Skills
# Programming Languages: C++, Python, C#.
# RDBMS: MySQL.
# Core CS: DSA, DBMS, OS, OOP, CN.
# Cloud: Azure Functions, Azure Service Bus, AWS S3.
# Frameworks: .NET(WPF, ASP.NET), Flask, Streamlit.
# AI: Machine Learning - Scikit learn, Deep Learning - TensorFlow, Large Language Models.
# DevTools: VS Code, Git, GitHub.
# Achievements
# Barclays Hack-O-Hire - Barclays, Pune - 2nd runner up April 2024
# UBS Hackathon - MKSSS’s Cummins, Pune - finalist April 2024
# TATA Power Hackathon - MindSpark COEP - Winner Oct 2023
# PICT INC ‘23 - PICT, Pune - 2nd runner up March 2023
# CRIF India Hackathon - MindSpark COEP - 2nd runner up Jan 2023
# Leetcode - 500+ questions solved
# Extra-Curricular
# Machine Learning Head, PICT CSI Club - Leading projects, sessions and SIGs of the ML domain for PCSB.
# Former Motorsport team member, PICT Automobile Club - Represented college at a national level for FKDC.
# Volunteer, PICT NSS - Actively volunteered for services of social cause.
# """

# generateQuestions = GenerateQuestions()
# response = generateQuestions.generate_questions(resume, "Barclays")

# print(response.message)