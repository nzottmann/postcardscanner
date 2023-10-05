# Copyright 2022 Nils Zottmann
# Licensed under the EUPL-1.2-or-later

from postcardscanner import PostcardScanner
from postcardscanner.hardware.scanner_v3 import ScannerV3

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading

import base64
import os

class ScannerStatus(BaseModel):
    last_postcard_timestamp: str
    last_postcard_successful: bool
    scanner_state: str

image_file_lock = threading.Lock()

def callback(image, success=True):
    print(f'Received image, success: {success}')
    filename = 'img_success.jpg' if success else 'img_fail.jpg'

    with image_file_lock:
        image.save(filename, quality=95)

# Create image files if they do not exist yet
with open('img_success.jpg', 'a+') as f:
    pass
with open('img_fail.jpg', 'a+') as f:
    pass

scanner = PostcardScanner(scanner=ScannerV3(callback=callback))
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
    return 'Use routes /last_postcard or /last_postcard_timestamp'

@app.get("/last_postcard")
async def last_postcard():
    with open('img_success.jpg', 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image

@app.get("/last_postcard_timestamp")
async def last_postcard_timestamp():
    with image_file_lock:
        return os.path.getctime('img_success.jpg')

@app.get("/postcard_scanner_status", response_model=ScannerStatus)
async def postcard_scanner_status():
    with image_file_lock:
        ts_success = os.path.getctime('img_success.jpg')
        ts_fail = os.path.getctime('img_fail.jpg')
    
    return ScannerStatus(
        last_postcard_timestamp=max(ts_success, ts_fail),
        last_postcard_successful=(ts_success > ts_fail),
        scanner_state=scanner.state
    )
@app.get("/accept_postcard", status_code=204)
async def accept_postcard():
    scanner.accept_postcard()
    return 

@app.get("/reject_postcard", status_code=204)
async def reject_postcard():
    scanner.reject_postcard()
    return 