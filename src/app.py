import os
import logging
import threading
import time
import subprocess
from rtsparty import Stream
from objectdaddy import Daddy
from relay_controller import RelayController


class PersonDetectingFogMachine():

    def __init__(self):
        logging.info('Starting App')
        self.fog_run_timeout = 2
        self._setup_stream()
        self._setup_object_recognition()
        self._setup_relay()

    def _setup_stream(self):
        """Set up the stream to the camera"""
        logging.info('Starting stream')
        self.stream = Stream(os.environ.get('STREAM_URL'))

    def _setup_object_recognition(self):
        """Set up object recognition and load models"""
        logging.info('Loading ML models')
        self.daddy = Daddy()
        self.daddy.set_callbacks(self.object_detected, self.object_expired)

    def _setup_relay(self):
        """Set up the relay controller"""
        self.rc = RelayController()

    def object_detected(self, detection):
        """Callback for an object being detected"""
        logging.info(f'{detection.label} detected')
        try:
            if detection.is_person():
                self.trigger_fog()
        except Exception:
            pass

    def trigger_fog(self):
        """Trigger the fog machine"""
        self.rc.fog_on()
        time.sleep(self.fog_run_timeout)
        self.rc.fog_off()

    def object_expired(self, detection):
        """Callback for an object expiring"""
        logging.info(f'{detection.label} expired')

    def process_frames_from_stream(self):
        """Processes the frames from the stream"""
        logging.info('Triggering fog to test')
        self.trigger_fog()
        logging.info('Test complete')
        logging.info('Watching for people')
        while True:
            logging.debug('Checking Frame')
            frame = self.stream.get_frame()
            if self.stream.is_frame_empty(frame):
                continue
            self.latest_frame = frame
            self.daddy.process_frame(frame)

    def run(self):
        """Run the application"""
        try:
            self.process_frames_from_stream()
        except KeyboardInterrupt:
            logging.info('Exiting application')


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    pdfm = PersonDetectingFogMachine()
    pdfm.run()
