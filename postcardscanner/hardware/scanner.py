from postcardscanner.states import PostcardScannerState

class Scanner():
    def __init__(self, callback):
        pass
    
    def simulate_scan(self, image=None):
        pass
    
    def loop(self) -> PostcardScannerState:
        return PostcardScannerState.enabled
