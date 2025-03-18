from flask import Flask
from controller import base


app = Flask(__name__)

app.secret_key = "dsjfj234234werwer234234"

app.register_blueprint(base.base)
