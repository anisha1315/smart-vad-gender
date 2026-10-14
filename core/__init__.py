import os
import sys

if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from core.audio_stream import MicrophoneStream
from core.engine import VADEngine
from core.identifier import GenderIdentifier

__all__ = ["MicrophoneStream", "VADEngine", "GenderIdentifier"]

if __name__ == "__main__":
    print("Do not run core.__init__.py directly. Use python main.py from the project root.")
