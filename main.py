"""
This module contains the main server code.
"""

from flask import Flask, jsonify, request
from Services.GenerateQuestions import GenerateQuestions
from Services.EvaluateAnswer import EvaluateAnswer
from Services.FollowUp import FollowUp

app = Flask(__name__)

@app.route("/")
def root():
    """
    Root route of the server.
    """
    return jsonify({
        "status": "success",
        "message": "Server is Up and Running",
        "data": "Server is Up and Running"

    }), 200

@app.route("/resume", methods=["POST", "GET"])
def generate_questions():
    """
    Generates questions from a resume.
    Args:
        resume (str): The resume from which questions are to be generated.
    """

    if request.method == "POST":
        data = request.get_json()
    else:
        data = request.args

    resume = data.get("resume", None)
    company_name = data.get("company_name", "")
    print("=========================================={}=====================================".format(company_name))
    
    if resume is None:
        return jsonify({
            "status": "error",
            "message": "Invalid request, missing 'resume' field",
            "data": None
        }), 400

    generator = GenerateQuestions()
    result = generator.generate_questions(resume, company_name)

    if not result.status:
        return jsonify({
            "status": "error",
            "message": result.message,
            "data": None
        }), 500

    return jsonify({
        "status": "success",
        "message": result.message,
        "data": result.data
    }), 200

@app.route("/evaluate", methods=["POST"])
def evaluate_answer():
    """
    Evaluates the answer given by the interviewee based on the question asked.
    Args:
        question (str): The question asked by the interviewer.
        answer (str): The answer given by the interviewee.
    """
    data = request.get_json()
    question = data.get("question", None)
    answer = data.get("answer", None)

    if question is None or answer is None:
        return jsonify({
            "status": "error",
            "message": "Invalid request, missing 'question' or 'answer' field",
            "data": None
        }), 400

    evaluator = EvaluateAnswer()
    result = evaluator.evaluate_answer(question, answer)

    if not result.status:
        return jsonify({
            "status": "error",
            "message": result.message,
            "data": None
        }), 500

    return jsonify({
        "status": "success",
        "message": result.message,
        "data": result.data
    }), 200

@app.route("/follow-up", methods=["POST"])
def get_follow_up_question():
    """
    Generate follow-up question based on the previous question and answer.
    Args:
        question (str): The previous question asked by the interviewer.
        answer (str): The previous answer given by the interviewee.
    """
    data = request.get_json()
    question = data.get("question", None)
    answer = data.get("answer", None)

    if question is None or answer is None:
        return jsonify({
            "status": "error",
            "message": "Invalid request, missing 'question' or 'answer' field",
            "data": None
        }), 400

    follow_up = FollowUp()
    result = follow_up.get_follow_up_question(question, answer)

    if not result.status:
        return jsonify({
            "status": "error",
            "message": result.message,
            "data": None
        }), 500

    return jsonify({
        "status": "success",
        "message": result.message,
        "data": result.data
    }), 200

@app.route("/evaluate/follow-up-question", methods=["POST"])
def asses_follow_up_question():
    """
    Assess the follow-up question based on context
    Args:
        question (str): The previous question asked by the interviewer.
        answer (str): The previous answer given by the interviewee.
        follow_up_question (str): The follow-up question generated.
        follow_up_answer (str): The expected answer to the follow-up question.
    """
    data = request.get_json()
    question = data.get("question", None)
    answer = data.get("answer", None)
    follow_up_question = data.get("follow_up_question", None)
    follow_up_answer = data.get("follow_up_answer", None)

    if question is None or answer is None or follow_up_question is None or follow_up_answer is None:
        return jsonify({
            "status": "error",
            "message": "Invalid request, one or more fields are missing",
            "data": None
        }), 400

    follow_up = FollowUp()
    result = follow_up.asses_follow_up_question(question,
                                                answer,
                                                follow_up_question,
                                                follow_up_answer
                                                )

    if not result.status:
        return jsonify({
            "status": "error",
            "message": result.message,
            "data": None
        }), 500

    return jsonify({
        "status": "success",
        "message": result.message,
        "data": result.data
    }), 200



if __name__ == "__main__":
    # generator = GenerateQuestions()
    # result = generator.generate_questions("Data Structures and Algorithms")
    app.run(host = "0.0.0.0", port = 5000)
