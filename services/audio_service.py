import threading
import time


class AudioService:

    def __init__(self, alert_service=None):

        self.alert_service = alert_service

        self.detected = False

        self.running = False

        self.thread = None

    # START AUDIO SERVICE

    def start(self):

        if not self.running:

            self.running = True

            self.thread = threading.Thread(
                target=self.monitor_audio,
                daemon=True
            )

            self.thread.start()

            print("AUDIO SERVICE STARTED")

    # STOP AUDIO SERVICE

    def stop(self):

        self.running = False

        print("AUDIO SERVICE STOPPED")

    # AUDIO MONITOR LOOP

    def monitor_audio(self):

        while self.running:

            # PLACEHOLDER AUDIO DETECTION

            # Future:
            # microphone monitoring
            # voice detection
            # noise analysis

            self.detected = False

            time.sleep(1)