import time
from io import BytesIO
import subprocess
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from .scanner import Scanner
from postcardscanner.states import PostcardScannerState

class ScannerV1(Scanner):
    clockwise = False
    steptype_1 = "Half"
    steptype_2 = "Half"
    stepdelay = .0003
    counter = 0
    def __init__(self, callback, pins={
        'dir': 4,
        'step': 17,
        'mode': (22, 27, 18),
        's1': 16,
        's2': 19,
        's3': 20,
        's4': 21,
        'sleep': 23,
        'led': 12
    }):
        self.pins = pins
        self.callback = callback
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # GPIOs
        GPIO.setup((pins['s1'], pins['s2'], pins['s3'], pins['s4']), GPIO.IN)
        GPIO.setup((pins['sleep'], pins['led']), GPIO.OUT)

        self.motor = RpiMotorLib.A4988Nema(pins['dir'], pins['step'], pins['mode'], "DRV8825")
        
        self._init_state()
        
    def _sns(self, sensor):
        sensors = ('s1', 's2', 's3', 's4')
        return GPIO.input(self.pins[sensors[sensor]])
        
    def _mot_sleep(self, state):
        GPIO.output(self.pins['sleep'], state)
        
    def _led(self, state):
        GPIO.output(self.pins['led'], state)
        
    def _init_state(self):
        if not self._sns(0) and not self._sns(1):
            self.pos = 0
        else:
            self.pos = 2
        
    def capture(self):
        process = subprocess.Popen(
            ['libcamera-still', '-n', '-t', '1', '-o', '-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )        
        return BytesIO(process.stdout.read())
    
    def loop(self):
        if self.pos == 0:
            if self._sns(0) and self._sns(1):
                self.pos = 1
                self._mot_sleep(1)
                self.counter = 0
            else:
                self._mot_sleep(0)
                time.sleep(0.1)
                return PostcardScannerState.enabled
        if self.pos == 1:
            self.counter += 1
            if self.counter > 50:
                self.pos = 99
            self.motor.motor_go(self.clockwise, self.steptype_1, 100, self.stepdelay, False, 0)
            if not self._sns(0) or not self._sns(1):
                self.pos = 0
            if self._sns(2):
                self.pos = 2
                self.counter = 0
            else:
                return PostcardScannerState.scanning
        if self.pos == 2:
            self.counter += 1
            if self.counter > 100:
                self.pos = 99
            self.motor.motor_go(self.clockwise, self.steptype_1, 100, self.stepdelay, False, 0)
            if not self._sns(2):
                self.pos = 1
            if self._sns(3):
                self.pos = 3
                self.counter = 0
            return PostcardScannerState.scanning
        if self.pos == 3:
            self.counter += 1
            if self.counter > 100:
                self.pos = 99
            self.motor.motor_go(self.clockwise, self.steptype_1, 100, self.stepdelay, False, 0)
            if not self._sns(1):
                self.motor.motor_go(not self.clockwise, self.steptype_1, 100, self.stepdelay, False, 0)
                self._mot_sleep(0)
                self._led(1)
                self.callback(self.capture())
                self._led(0)
                self._mot_sleep(1)
                #time.sleep(1)
                self.pos = 4
                self.counter = 0
            return PostcardScannerState.scanning
        if self.pos == 4:
            self.counter += 1
            if self.counter > 3:
                self.pos = 99
            self.motor.motor_go(self.clockwise, self.steptype_2, 3000, .00005, False, 0)
            if not self._sns(3):
                self.motor.motor_go(self.clockwise, self.steptype_2, 3000, .00005, False, 0)
                self._mot_sleep(0)
                self.pos = 0
            return PostcardScannerState.scanning
        if self.pos == 99:
            self._mot_sleep(0)
            if self._sns(0) or self._sns(1) or self._sns(2) or self._sns(3):
                time.sleep(0.1)
                return PostcardScannerState.error
            else:
                self.pos = 0
        
        return PostcardScannerState.enabled
