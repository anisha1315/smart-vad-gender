import numpy as np


class VADEngine:
    def __init__(self, energy_threshold: float = 0.008):
        self.energy_threshold = energy_threshold

    def is_speech(self, audio_data):
        audio = np.asarray(audio_data, dtype=np.float32)
        if audio.size == 0:
            return False

        energy = np.sqrt(np.mean(audio**2))
        return energy > self.energy_threshold 