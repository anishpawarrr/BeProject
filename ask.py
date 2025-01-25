import requests

root = "http://127.0.0.1:5000"

generate_questions = root + "/generate-questions"

evaluate_answer = root + "/evaluate-answer"

payload_generate_questions = {"resume": "python,java,c++,c#"}

payload_evaluate_answer = {"question": "What is 100 + 200", "answer": "It is 300"}

# response = requests.post(generate_questions, json=payload_generate_questions)

response = requests.post(evaluate_answer, json=payload_evaluate_answer)

print(response)
print(response.json())
