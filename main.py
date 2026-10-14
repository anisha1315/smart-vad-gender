import math
import numpy as np

from core.audio_stream import MicrophoneStream
from core.engine import VADEngine
from core.identifier import GenderIdentifier
from utils.processor import process_audio


def run_system():
    vad = VADEngine()
    gender_tool = GenderIdentifier()

    print("--- System Active: Detecting Speech & Gender ---")
    input("Press Enter, then speak clearly into the microphone...\n")

    try:
        with MicrophoneStream(sample_rate=16000, block_size=2048) as mic:
            print(f"Using microphone: {mic.device_name}")
            print("Recording for 4 seconds...")

            frames = []
            blocks = int(16000 * 4 / 2048)
            for _ in range(blocks):
                raw_chunk = next(mic)
                frames.append(process_audio(raw_chunk))

            audio = np.concatenate(frames, axis=0)
            print("Analyzing captured audio...")

            if not vad.is_speech(audio):
                print("No speech detected. Please try again and speak clearly into the microphone.")
                return

            label, pitch = gender_tool.detect_gender(audio)
            if pitch is None or not math.isfinite(pitch):
                print("Could not determine pitch clearly. Please try again.")
                return

            avg_pitch = int(pitch)
            label = "Male" if avg_pitch < 165 else "Female"
            print(f" [V] Final Speaker: {label} ({avg_pitch} Hz)")
            
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    except ImportError as exc:
        print(f"\nMissing dependency: {exc}")
        print("Install the required audio package using 'pip install -r requirements.txt'.")
    except Exception as exc:
        print(f"\nError: {exc}")


if __name__ == "__main__":
    run_system()