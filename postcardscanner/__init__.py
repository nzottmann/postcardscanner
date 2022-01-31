import logging
logger = logging.getLogger('postcardscanner')
logging.basicConfig(level=logging.DEBUG)
import threading
from .states import PostcardScannerState
from .hardware.scanner import Scanner

class PostcardScanner(threading.Thread):
    state = PostcardScannerState.disabled
    
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        super(PostcardScanner, self).__init__(daemon=True)
        
    def simulate_scan(self, image=None):
        self.scanner.simulate_scan(image)
        
    def run(self):
        self.state = PostcardScannerState.enabled
        logger.debug(f'state: {self.state}')
        while True:
            if self.state is PostcardScannerState.disabled:
                continue
            
            new_state = self.scanner.loop()
            if new_state is not self.state:
                logger.debug(f'state: {new_state}')
                self.state = new_state
                