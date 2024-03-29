# Copyright 2022 Nils Zottmann
# Licensed under the EUPL-1.2-or-later

from postcardscanner import PostcardScanner
from postcardscanner.hardware.scanner_demo_camera import ScannerDemoCamera

def callback(image):
    print('Received image')
    with open('img.jpg','wb') as out:
        out.write(image.read())

scanner = PostcardScanner(scanner=ScannerDemoCamera(callback=callback))
scanner.start()
scanner.simulate_scan()

# Keep script running forever, thread runs endless
scanner.join()
