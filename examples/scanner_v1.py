# Copyright 2022 Nils Zottmann
# Licensed under the EUPL-1.2-or-later

from postcardscanner import PostcardScanner
from postcardscanner.hardware.scanner_v1 import ScannerV1

def callback(image):
    print('Received image')
    with open('img.jpg','wb') as out:
        out.write(image.read())

scanner = PostcardScanner(scanner=ScannerV1(callback=callback))
scanner.start()

# Keep script running forever, thread runs endless
scanner.join()
