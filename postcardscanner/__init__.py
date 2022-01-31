import logging
logger = logging.getLogger('postcardscanner')
logging.basicConfig(level=logging.DEBUG)

from .thread import PostcardscannerThread

class PostcardScanner:
    def __init__(self, scanner):
        self.thread = PostcardscannerThread(scanner)
        self.thread.start()
        
    def start(self):
        self.thread.enable()
    
    def stop(self):
        self.thread.disable()
        
    def get_last_card(self):
        return None
        
    def simulate_scan(self, image=None):
        self.thread.simulate_scan(image)
