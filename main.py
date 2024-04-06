from kafka_stream import get_data
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define an async route at the root of the application
@app.get('/')
async def home():
    
    return {"message": "Hello, FastAPI!"}

if __name__ == '__main__':
    app.run(debug=True)
