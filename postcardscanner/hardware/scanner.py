from postcardscanner.states import PostcardScannerState

class Scanner():
    def __init__(self, pins: dict, callback=None):
        pass
            
    def stop(self):
        pass
    
    def simulate_scan(self, image):
        pass
    
    def loop(self) -> PostcardScannerState:
        return PostcardScannerState.enabled
