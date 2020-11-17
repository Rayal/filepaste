from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['GET'])
def upload():



if __name__ == '__main__':
    app.run()
