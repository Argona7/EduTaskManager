from flask import Flask
from ..DataBase.DB import *


app = Flask(__name__)

def main():

@app.route('/')
def index():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)