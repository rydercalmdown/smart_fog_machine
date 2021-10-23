import logging
import time
import RPi.GPIO as GPIO


class RelayController():
    """Class for controlling the relay"""

    def __init__(self):
        self._set_defaults()
        self._setup_gpio()
        self.fog_is_on = False

    def __del__(self):
        GPIO.cleanup()

    def _set_defaults(self):
        """Set defaults for the application"""
        self.fog_pin = 5

    def _setup_gpio(self):
        """Set up the GPIO defaults"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.fog_pin, GPIO.OUT, initial=GPIO.HIGH)

    def fog_on(self):
        """Turns the fog on if its available"""
        logging.info('Turning Fog On')
        self._cycle_pin(self.fog_pin)
        self.fog_is_on = True

    def fog_off(self):
        """Turns the fog off"""
        logging.info('Turning Fog Off')
        self._cycle_pin(self.fog_pin)
        self.fog_is_on = False

    def _cycle_pin(self, pin, timeout=0.3):
        """Cycle a relay channel on and off"""
        GPIO.output(pin, GPIO.LOW)
        time.sleep(timeout)
        GPIO.output(pin, GPIO.HIGH)
