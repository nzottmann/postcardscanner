import time
from postcardscanner import PostcardScanner
from postcardscanner.hardware import ScannerV0

scanner = ScannerV0()

#while True:
#    scanner.loop()

def callback(image):
    print(image)

scanner = PostcardScanner(scanner=ScannerV0(callback=callback))

scanner.start()
while True:
    time.sleep(1)
scanner.stop()
