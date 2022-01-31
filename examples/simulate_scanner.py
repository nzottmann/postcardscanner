import time
from postcardscanner import PostcardScanner

def callback(image):
    print(image)

scanner = PostcardScanner(callback=callback, simulate=True)

scanner.start()
time.sleep(1)
scanner.simulate_scan()
scanner.stop()

time.sleep(2)
