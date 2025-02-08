from Services.Utils.ExtractPdf import extract_text_from_pdf
from Services.GenerateQuestions import GenerateQuestions
from Services.EvaluateAnswer import EvaluateAnswer
from Services.FollowUp import FollowUp
from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "Server is Up and Running",
        "data": "Server is Up and Running"

    }), 200

@app.route("/generate-questions", methods=["POST"])
def generate_questions():
    data = request.get_json()
    resume = data.get("resume", None)

    if resume is None:
        return jsonify({
            "status": "error",
            "message": "Invalid request, missing 'resume' field",
            "data": None
        }), 400
    
    generator = GenerateQuestions()
    result = generator.generate_questions(resume)

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
    
@app.route("/evaluate-answer", methods=["POST"])
def evaluate_answer():
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

@app.route("/follow-up-question", methods=["POST"])
def get_follow_up_question():
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

@app.route("/evaluate-follow-up-question", methods=["POST"])
def asses_follow_up_question():
    data = request.get_json()
    question = data.get("question", None)
    answer = data.get("answer", None)
    follow_up_question = data.get("follow_up_question", None)
    follow_up_answer = data.get("follow_up_answer", None)

    if question is None or answer is None or follow_up_question is None or follow_up_answer is None:
        return jsonify({
            "status": "error",
            "message": "Invalid request, missing 'question', 'answer', 'follow_up_question' or 'follow_up_answer' field",
            "data": None
        }), 400
    
    follow_up = FollowUp()
    result = follow_up.asses_follow_up_question(question, answer, follow_up_question, follow_up_answer)

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
    app.run(debug=True, host="0.0.0.0")