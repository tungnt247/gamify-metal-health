from dotenv import dotenv_values


env = dotenv_values('.env')

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:yourpassword@db:5432/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = env.get('GEMINI_API_KEY')
    SECRET_KEY = env.get('SECRET_KEY')
    JWT_SECRET_KEY = env.get('JWT_SECRET_KEY')
    REDIS_URL = env.get('REDIS_URL', 'redis://redis:6379/0')
    AGORA_APP_ID = env.get('AGORA_APP_ID')
    AGORA_APP_CERTIFICATE = env.get('AGORA_APP_CERTIFICATE')
