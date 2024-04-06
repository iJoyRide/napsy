from kafka_stream import stream_data
from fastapi import FastAPI

async def create_batch_scanner():
    # Create a batch scanner
    async for batch in get_data():
        print(batch)
# Create an instance of the FastAPI class
app = FastAPI()

# Define an async route at the root of the application
@app.get('/')
async def home():

    return {"message": "Hello, FastAPI!"}

if __name__ == '__main__':
    app.run(debug=True)
