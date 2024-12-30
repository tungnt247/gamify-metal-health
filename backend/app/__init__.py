from flask import Flask
from flask_restx import Api
from .resources import api as resources_api
from .quizes import api as quizes_api
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

api = Api(
    app,
    version="1.0",
    title="Mental Health API",
    description="Gamify Mental Health API Doc",
    doc="/swagger"
)
api.add_namespace(resources_api, path='/resources')
api.add_namespace(quizes_api, path='/quizes')

if __name__ == "__main__":
    app.run(debug=True)
