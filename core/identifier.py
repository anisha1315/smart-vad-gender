import numpy as np


class GenderIdentifier:
    def detect_gender(self, audio_data, sample_rate: int = 16000):
        audio = np.asarray(audio_data, dtype=np.float32)
        if audio.ndim > 1:
            audio = audio.flatten()

        if audio.size == 0:
            return "Unknown", None

        pitch = self._estimate_pitch(audio, sample_rate)
        if pitch is None:
            return "Unknown", None

        label = "Male" if pitch < 165 else "Female"
        return label, pitch

    def _estimate_pitch(self, signal, sample_rate):
        signal = signal - np.mean(signal)
        if len(signal) < int(sample_rate * 0.05):
            return None

        autocorr = np.correlate(signal, signal, mode="full")
        autocorr = autocorr[len(autocorr) // 2 :]

        min_lag = int(sample_rate / 300)
        max_lag = int(sample_rate / 80)
        if max_lag >= len(autocorr):
            max_lag = len(autocorr) - 1

        autocorr[:min_lag] = 0
        peak = np.argmax(autocorr[min_lag:max_lag]) + min_lag
        if peak <= 0 or autocorr[peak] <= 0:
            return None

        peak_strength = autocorr[peak]
        if peak_strength < 0.3 * np.max(autocorr):
            return None

        pitch = sample_rate / peak
        if pitch < 50 or pitch > 500:
            return None

        return pitch