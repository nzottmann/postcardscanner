import time
from io import BytesIO
import subprocess
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from .scanner import Scanner
from postcardscanner.states import PostcardScannerState

class ScannerV0(Scanner):
    def __init__(self, callback, pins={
        'dir': 20,
        'step': 21,
        'mode': (14, 15, 18),
        's1': 5,
        's2': 6,
        'sensor_pwr': (13, 19)
    }):
        self.pins = pins
        self.callback = callback
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        # Sensor power
        GPIO.setup(pins['sensor_pwr'], GPIO.OUT)
        GPIO.output(pins['sensor_pwr'], 1)

        # Sensors
        GPIO.setup((pins['s1'], pins['s2']), GPIO.IN)

        self.motor = RpiMotorLib.A4988Nema(pins['dir'], pins['step'], pins['mode'], "DRV8825")
        
        self._init_state()
        
    def _s1(self):
        return GPIO.input(self.pins['s1'])
    
    def _s2(self):
        return GPIO.input(self.pins['s2'])
        
    def _init_state(self):
        if not self._s2():
            self.pos = 0
        else:
            self.pos = 3
        
    def capture(self):
        process = subprocess.Popen(
            ['libcamera-still', '-n', '-t', '1', '-o', '-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )        
        return BytesIO(process.stdout.read())
    
    def loop(self):
        if self.pos == 0:
            if self._s1():
                self.pos = 1
            else:
                time.sleep(0.1)
                return PostcardScannerState.enabled
        if self.pos == 1:
            self.motor.motor_go(True, "1/8" , 10, .00001, False, 0)
            if not self._s1():
                self.pos = 0
            if self._s2():
                self.pos = 2
            else:
                return PostcardScannerState.scanning
        if self.pos == 2:
            self.motor.motor_go(True, "1/8" , 32*20, .00001, False, 0)
            self.callback(self.capture())
            self.pos = 3
        if self.pos == 3:
            self.motor.motor_go(True, "1/8" , 32*200, .00001, False, 0)
            self.pos = 4
            return PostcardScannerState.scanning
        if self.pos == 4:
            if not self._s2():
                self.pos = 0
            else:
                time.sleep(0.1)
                return PostcardScannerState.error
        
        return PostcardScannerState.enabled
