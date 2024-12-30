from flask import Flask
from flask_restx import Api
from .resources import api as resources_api
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
api.add_namespace(resources_api, path='/resources')

if __name__ == "__main__":
    app.run(debug=True)
