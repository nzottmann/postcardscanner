from postcardscanner import PostcardScanner
from postcardscanner.hardware import ScannerV0

def callback(image):
    print('Received image')
    with open('img.jpg','wb') as out:
        out.write(image.read())

scanner = PostcardScanner(scanner=ScannerV0(callback=callback))
scanner.start()

# Keep script running forever, thread runs endless
scanner.join()
