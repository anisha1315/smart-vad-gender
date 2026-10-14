# smart_vad_gender

A simple Python speech activity detection and gender inference demo.

## Setup

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The project now uses a lightweight energy-based VAD and a simple pitch estimator, with audio capture supported via `sounddevice` or `pyaudio` on Windows.
