from kafka_stream import get_data
from flask import Flask

app = Flask(__name__)

@app.route('/')
async def home():
    return 'Hello, Async Flask!'

if __name__ == '__main__':
    app.run(debug=True)
