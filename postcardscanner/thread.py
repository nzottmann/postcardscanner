import logging
import time
import threading
import queue
from .states import PostcardScannerState
from .hardware.scanner import Scanner
from . import logger

class PostcardscannerThread(threading.Thread):
    state = PostcardScannerState.disabled
    
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        super(PostcardscannerThread, self).__init__(daemon=True)

    def enable(self):
        self.state = PostcardScannerState.enabled
        logger.debug('enabled')
            
    def disable(self):
        self.state = PostcardScannerState.disabled
        
    def simulate_scan(self, image):            
        logger.debug('Scan simulation requested')
        self.scanner.simulate_scan(image)
        
    def run(self):
        while True:
            if self.state is PostcardScannerState.disabled:
                continue
            
            new_state = self.scanner.loop()
            if new_state is not self.state:
                logger.debug(f'state: {new_state}')
                self.state = new_state
