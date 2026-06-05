import numpy as np


class AudioDetector:

    def __init__(self, threshold=0.04):

        self.threshold = threshold

    def detect(self, audio_chunk):

        rms = np.sqrt(np.mean(audio_chunk ** 2))

        if rms > self.threshold:
            return True, rms

        return False, rms