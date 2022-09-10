from postcardscanner import PostcardScanner
from postcardscanner.hardware.scanner_v1 import ScannerV1

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import base64
import os

def callback(image):
    print('Received image')
    with open('img.jpg','wb') as out:
        out.write(image.read())

scanner = PostcardScanner(scanner=ScannerV1(callback=callback))
scanner.start()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return os.path.getctime('img.jpg')

@app.get("/last_postcard")
async def root():
    with open('img.jpg', 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image

@app.get("/last_postcard_timestamp")
async def root():
    return os.path.getctime('img.jpg')
