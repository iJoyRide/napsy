# from kafka_stream import stream_data
# from fastapi import FastAPI
# import asyncio
# from models import UrlsToScan

# app = FastAPI()
# async def create_batch_scanner(urls: list[str]):
#     # Create a batch scanner
#     batch  = []
#     for url in urls:
#         task = asyncio.create_task(stream_data(url, "nj_created"))
#         batch.append(task)
#     await asyncio.gather(*batch)
# # Create an instance of the FastAPI class


# async def check_cache():
#     print("Checking cache")
#     #if inside redis then dont craete batch scanner
#     #if not then create batch scanner
#     await create_batch_scanner(urls)


# # Define an async route at the root of the application
# @app.post('/url')
# async def urls(urls: UrlsToScan):
#     await check_cache(urls.urls)
#     return {"message": "URLs are being scanned"}

# if __name__ == '__main__':  
#     app.run(debug=True)


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from virus import check_virustotal  

app = FastAPI()

class UrlList(BaseModel):
    urls: List[str]

@app.post("/scan-urls/")
async def scan_urls(url_list: UrlList):
    # Assuming API_KEY is loaded from environment or another secure place
    api_key = os.getenv("APPI_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key is not configured correctly.")

    for url in url_list.urls:
        # Note: check_virustotal currently does not return anything, consider modifying it to return scan results if needed
        check_virustotal(url, api_key)
    
    return {"message": "URLs are being scanned"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
