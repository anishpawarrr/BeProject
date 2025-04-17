from json import loads, dump
import random

class FinaliseQuestions:
    
    def SetQuestions(self):
        data = None
        with open("questions.json", "r") as f:
            data = loads(f.read())

        newQuestions = dict()

        for question_set in data:
            include = random.randint(0, 2)

            if include == 1:
                newQuestions[question_set] = data[question_set]

        with open("questions.json", "w") as f:
            dump(newQuestions, f, indent=4)
        
