from postcardscanner import PostcardScanner
from postcardscanner.hardware.scanner_v1 import ScannerV1

from fastapi import FastAPI
from fastapi.responses import FileResponse

def callback(image):
    print('Received image')
    with open('img.jpg','wb') as out:
        out.write(image.read())

scanner = PostcardScanner(scanner=ScannerV1(callback=callback))
scanner.start()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Get last postcard from /last_postcard"}

@app.get("/last_postcard")
async def root():
    return FileResponse('img.jpg')
