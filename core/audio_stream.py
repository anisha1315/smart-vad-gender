import sys

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import pyaudio
except ImportError:
    pyaudio = None


class MicrophoneStream:
    def __init__(self, sample_rate: int = 16000, block_size: int = 2048, channels: int = 1):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        self.stream = None
        self.backend = "sounddevice" if sd is not None else "pyaudio" if pyaudio is not None else None
        self.device = None
        self.device_name = "Unknown"

        if self.backend is None:
            raise ImportError(
                "No audio backend available. Install 'sounddevice' or 'pyaudio'."
            )

    def _find_input_device(self):
        for idx, device in enumerate(sd.query_devices()):
            if device["max_input_channels"] > 0:
                return idx
        raise RuntimeError("No input device found for sounddevice.")

    def __enter__(self):
        if self.backend == "sounddevice":
            selected = sd.default.device
            if isinstance(selected, tuple):
                selected = selected[0]

            if selected is None or selected == -1:
                selected = self._find_input_device()

            self.device = selected
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                channels=self.channels,
                dtype="int16",
                device=self.device,
            )
            self.stream.start()

            try:
                self.device_name = sd.query_devices(self.device)["name"]
            except Exception:
                self.device_name = str(self.device)
        else:
            self._pyaudio = pyaudio.PyAudio()
            self.stream = self._pyaudio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.block_size,
            )
            self.device_name = "pyaudio default"
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if self.backend == "sounddevice":
            data, overflow = self.stream.read(self.block_size)
            if overflow:
                raise IOError("Audio input overflow")
            return data

        chunk = self.stream.read(self.block_size, exception_on_overflow=False)
        return chunk

    def close(self):
        if self.stream is None:
            return

        if self.backend == "sounddevice":
            self.stream.stop()
            self.stream.close()
        else:
            self.stream.stop_stream()
            self.stream.close()
            self._pyaudio.terminate()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()