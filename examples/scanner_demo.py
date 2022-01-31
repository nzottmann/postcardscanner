from io import BytesIO
from postcardscanner import PostcardScanner
from postcardscanner.hardware.scanner_demo import ScannerDemo

def callback(image):
    print('Received image')
    with open('img.jpg','wb') as out:
        out.write(image.read())

scanner = PostcardScanner(scanner=ScannerDemo(callback=callback))
scanner.start()

# Input file will be returned by callback
with open('examples/example.jpg','rb') as file:
    image = BytesIO(file.read())
scanner.simulate_scan(image)

# Keep script running forever, thread runs endless
scanner.join()
