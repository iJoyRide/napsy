from kafka_stream import stream_data
from fastapi import FastAPI
import asyncio
from models import UrlsToScan

app = FastAPI()
async def create_batch_scanner(urls: list[str]):
    # Create a batch scanner
    batch  = []
    for url in urls:
        task = asyncio.create_task(stream_data(url, "nj_created"))
        batch.append(task)
    await asyncio.gather(*batch)
# Create an instance of the FastAPI class


async def check_cache():
    print("Checking cache")
    #if inside redis then dont craete batch scanner
    #if not then create batch scanner
    await create_batch_scanner(urls)


# Define an async route at the root of the application
@app.post('/url')
async def urls(urls: UrlsToScan):
    await check_cache(urls.urls)
    return {"message": "URLs are being scanned"}

if __name__ == '__main__':  
    app.run(debug=True)


