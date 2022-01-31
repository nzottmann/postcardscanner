import time
from io import BytesIO
import subprocess
from .scanner import Scanner
from postcardscanner.states import PostcardScannerState

class ScannerDemoCamera(Scanner):
    scanning = False
    def __init__(self, callback):
        self.callback = callback
        
    def capture(self):
        process = subprocess.Popen(
            ['libcamera-still', '-n', '-t', '1', '-o', '-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )        
        return BytesIO(process.stdout.read())
        
    def simulate_scan(self, image=None):
        self.scanning = True
        self.callback(self.capture())
    
    def loop(self):
        time.sleep(1)
        if self.scanning:
            self.scanning = False
            return PostcardScannerState.scanning
        return PostcardScannerState.enabled
