from flask import Flask
from cmd_parser import create_parser

app = Flask(__name__)


@app.route('/', methods=['GET'])
def help():
    parser = create_parser()
    return parser.format_help()


if __name__ == '__main__':
    app.run()
