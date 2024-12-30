import google.generativeai as genai
from .config import Config


class GeminiAPICLient:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.client = genai.GenerativeModel('gemini-1.5-flash')

    def generate_text(self, input):
        response = self.client.generate_content(input)
        return response.text
