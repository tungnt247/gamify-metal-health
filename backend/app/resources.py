from flask_restx import Namespace, Resource, fields
from .client import GeminiAPICLient


api = Namespace('resources', description='Google Generative AI operations')
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

        client = GeminiAPICLient()
        response = client.generate_text(input_text)

        return {'response': response}
