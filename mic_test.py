import sounddevice as sd
import numpy as np

# List devices
print("Input devices:")
print(sd.query_devices())
default_id = sd.default.device[0]
print(f"Default input device index: {default_id}")

# Try to open a stream and print raw energy
def callback(indata, frames, time, status):
    energy = np.linalg.norm(indata) / frames
    print(f"Energy: {energy:.4f}", flush=True)

try:
    with sd.InputStream(samplerate=16000, channels=1, callback=callback, blocksize=1024, dtype='int16'):
        input("🎤 Mic is live. Speak and watch the numbers. Press Enter to stop...\n")
except Exception as e:
    print(f"Error: {e}")