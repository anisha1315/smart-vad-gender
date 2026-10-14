import wave
import numpy as np

try:
    import sounddevice as sd
except ImportError:
    sd = None


def save_wav(file_path, audio_data, sample_rate=16000, channels=1):
    audio = np.asarray(audio_data, dtype=np.float32)
    audio = np.round(audio * 32767).astype(np.int16)
    if audio.ndim > 1 and channels == 1:
        audio = audio[:, 0]

    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())


def record_to_file(file_path, duration_seconds=5, sample_rate=16000, channels=1):
    if sd is None:
        raise ImportError("Install sounddevice to record audio: pip install sounddevice")

    data = sd.rec(
        int(duration_seconds * sample_rate),
        samplerate=sample_rate,
        channels=channels,
        dtype="int16",
    )
    sd.wait()
    save_wav(file_path, data.astype(np.float32) / 32768.0, sample_rate=sample_rate, channels=channels)
