from flask_restx import Namespace, Resource, fields
import google.generativeai as genai
from .config import Config


api = Namespace('resources', description='Google Generative AI operations')

genai.configure(api_key=Config.GEMINI_API_KEY)

client = genai.GenerativeModel('gemini-1.5-flash')

model = api.model('Model', {
    'input': fields.String(required=True, description='Input text for the AI model'),
})

@api.route('/')
class GenerativeAI(Resource):
    @api.doc('Generate AI Response')
    @api.expect(model)
    def post(self):
        data = api.payload
        input_text = data['input']

        response = client.generate_content(input_text)

        return {'response': response.text}
