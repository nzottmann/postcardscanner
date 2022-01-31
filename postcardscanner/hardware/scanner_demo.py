import time
from .scanner import Scanner
from postcardscanner.states import PostcardScannerState

class ScannerDemo(Scanner):
    scanning = False
    def __init__(self, callback):
        self.callback = callback
        
    def simulate_scan(self, image):
        self.scanning = True
        self.callback(image)
    
    def loop(self):
        time.sleep(1)
        if self.scanning:
            self.scanning = False
            return PostcardScannerState.scanning
        return PostcardScannerState.enabled
