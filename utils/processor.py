import numpy as np


def process_audio(raw_data):
    if isinstance(raw_data, tuple) and len(raw_data) == 2:
        audio, overflow = raw_data
        if overflow:
            raise IOError("Audio input overflow")
        return process_audio(audio)

    if isinstance(raw_data, (bytes, bytearray, memoryview)):
        audio = np.frombuffer(raw_data, dtype=np.int16)
    elif isinstance(raw_data, np.ndarray):
        audio = raw_data
    elif isinstance(raw_data, list):
        audio = np.asarray(raw_data)
    else:
        try:
            audio = np.asarray(raw_data)
        except Exception:
            raise TypeError(
                "process_audio expects raw bytes, a numpy.ndarray, or a (data, overflow) tuple"
            )

    audio = np.asarray(audio, dtype=np.float32)
    if audio.dtype == np.int16:
        return audio / 32768.0
    if np.issubdtype(audio.dtype, np.integer):
        return audio / np.iinfo(audio.dtype).max
    return audio