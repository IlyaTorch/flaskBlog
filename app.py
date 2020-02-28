from flask import Flask
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)


if __name__ == '__main__':
    app.run()
