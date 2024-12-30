from flask_restx import Namespace, Resource, fields
from .client import GeminiAPICLient
from flask import request, jsonify
from flask_restx import Resource
import random


api = Namespace('quizes', description='Google Generative AI operations')
quiz_model = api.model("Quiz", {
    "questions": fields.List(fields.Nested(api.model("Question", {
        "question": fields.String(required=True, description="Quiz question"),
        "options": fields.List(fields.String, required=True, description="Options (A, B, C)"),
        "answer": fields.String(required=True, description="Correct answer (A, B, or C)"),
    }))),
})
answer_model = api.model("Answer", {
    "answers": fields.List(fields.Integer, description="List of selected options by index")
})
MENTAL_HEALTH_TOPICS = [
    "stress management",
    "anxiety reduction",
    "mindfulness",
    "mental health awareness",
    "positive psychology"
]

def generate_question(topic):
    prompt = f"Generate a multiple-choice question on the topic of {topic}. Include 4 options and mark the correct answer."
    client = GeminiAPICLient()
    response = client.generate_text(prompt)
    response = response.replace("**", "")

    lines = response.split("\n")
    lines = [line for line in lines if line != ""]

    question = lines[0].replace("Question: ", "").strip()
    options = [line.strip().replace("  ", " ") for line in lines[1:5]]
    correct_option = lines[5].replace("Correct Answer:", "").strip()
    correct_option_idx = options.index(correct_option)

    return {"question": question, "options": options, "correct_option_idx": correct_option_idx}


@api.route('/')
class QuizGenerator(Resource):
    def get(self):
        """Generate a random multiple-choice quiz."""
        topic = random.choice(MENTAL_HEALTH_TOPICS)
        quiz = [generate_question(topic) for _ in range(5)]
        return jsonify({"quiz": quiz})


@api.route("/score/")
class QuizScore(Resource):
    @api.expect(answer_model)
    def post(self):
        """Calculate and return the score based on user answers."""
        data = request.json
        user_answers = data.get("user_answers", [])
        correct_answers = data.get("correct_answers", [])

        score = 0
        for idx, answer in enumerate(user_answers):
            if answer == correct_answers[idx]:
                score += 1

        return jsonify({"score": score, "total": len(correct_answers)})
