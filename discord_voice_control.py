#!/usr/bin/env python3
"""
Improved Discord Voice Controller using Whisper STT
- Debug transcription logging
- Confirmation beep
- Adjustable buffer/interval for better responsiveness
"""

import threading
import queue
import time
import sys
import numpy as np
import sounddevice as sd
import keyboard
from difflib import SequenceMatcher
from faster_whisper import WhisperModel

# ========== CONFIGURATION ==========
COMMANDS = {
    "mute": "ctrl+shift+m",
    "unmute": "ctrl+shift+m",    # same hotkey, separate command name
    "deafen": "ctrl+shift+d",
    "camera on": "ctrl+shift+v",  # set your own keybind in Discord
}
SAMPLE_RATE = 16000
BUFFER_DURATION = 1.5          # seconds of audio for each transcription (increased)
PROCESS_INTERVAL = 1.0         # seconds between attempts (more frequent)
LEVEL_UPDATE_MS = 50
LEVEL_HISTORY = 30

WHISPER_MODEL_SIZE = "medium"    # or "base" for better accuracy
WHISPER_DEVICE = "cpu"

# ========== GLOBALS ==========
audio_queue = queue.Queue()
command_queue = queue.Queue()
running = True
selected_device = None
device_list = sd.query_devices()

def list_microphones():
    print("\nAvailable input devices:")
    for i, dev in enumerate(device_list):
        if dev['max_input_channels'] > 0:
            print(f"  [{i}] {dev['name']}")
    print()

def select_microphone():
    while True:
        try:
            idx = int(input("Enter device number: "))
            dev = device_list[idx]
            if dev['max_input_channels'] > 0:
                print(f"Selected: {dev['name']}\n")
                return idx
            else:
                print("That device has no input channels. Try again.")
        except (ValueError, IndexError):
            print("Invalid number. Use the index from the list.")

def similar(a, b, threshold=0.7):
    """Fuzzy string matching."""
    return SequenceMatcher(None, a, b).ratio() >= threshold

def execute_command(text):
    """Parse transcribed text with fuzzy alias matching and beep confirmation."""
    text_lower = text.lower().strip()
    # Debug: show transcription in console
    print(f"\n💬 Transcription: '{text_lower}'")

    # Command aliases (including common misrecognitions)
    command_map = {
        "mute": ["mute", "mood", "boot", "mut", "muted", "mute please", "mute now", "mic", "mike", "on", "mew"],
        "unmute": ["unmute", "unmood", "unmut", "un mute", "ummute", "mike off", "mic off", "off"],
        "deafen": ["deafen", "defen", "deff", "deaf", "deaf and"],
        "camera on": ["camera on", "camera", "cam on", "camera turn on", "cam"],
    }

    for canonical, aliases in command_map.items():
        for alias in aliases:
            if alias in text_lower or similar(alias, text_lower, threshold=0.75):
                hotkey = COMMANDS.get(canonical)
                if hotkey:
                    print(f"🎯 Matched: '{canonical}' → simulating {hotkey}")
                    keyboard.send(hotkey)
                    # Confirmation beep (Windows beep, fallback to terminal bell)
                    try:
                        import winsound
                        winsound.Beep(800, 150)
                    except ImportError:
                        print('\a', end='', flush=True)
                    return

def audio_level_meter():
    """Real‑time console level meter (main thread)."""
    global running
    level_buffer = np.zeros(LEVEL_HISTORY)
    idx = 0

    def audio_callback(indata, frames, time_info, status):
        if status:
            return
        rms = np.sqrt(np.mean(indata**2))
        level = min(1.0, rms * 10)
        audio_queue.put(level)

    stream = sd.InputStream(
        device=selected_device,
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        blocksize=int(SAMPLE_RATE * 0.05)
    )
    stream.start()
    print("\n🎙️ Live mic meter active. Speak commands like 'mute', 'deafen', 'camera on'.")
    print("Press Ctrl+C to stop.\n")

    try:
        while running:
            try:
                level = audio_queue.get(timeout=LEVEL_UPDATE_MS / 1000.0)
                level_buffer[idx] = level
                idx = (idx + 1) % LEVEL_HISTORY
                smooth_level = np.mean(level_buffer)
                bar_len = int(smooth_level * 50)
                bar = '█' * bar_len + '░' * (50 - bar_len)
                print(f"\r[{bar}] {smooth_level:.2f}", end='', flush=True)
            except queue.Empty:
                pass
    finally:
        stream.stop()
        stream.close()

def whisper_worker():
    """Background thread: captures audio, runs Whisper, queues transcriptions."""
    global running
    print(f"Loading Whisper model '{WHISPER_MODEL_SIZE}' on {WHISPER_DEVICE}...")
    model = WhisperModel(WHISPER_MODEL_SIZE, device=WHISPER_DEVICE, compute_type="int8")
    print("Whisper ready.\n")

    audio_buffer = np.array([], dtype=np.float32)
    sample_rate = SAMPLE_RATE

    def audio_callback(indata, frames, time_info, status):
        nonlocal audio_buffer
        if status:
            return
        audio_buffer = np.append(audio_buffer, indata.flatten())
        max_len = int(BUFFER_DURATION * sample_rate)
        if len(audio_buffer) > max_len:
            audio_buffer = audio_buffer[-max_len:]

    stream = sd.InputStream(
        device=selected_device,
        samplerate=sample_rate,
        channels=1,
        callback=audio_callback,
        blocksize=int(sample_rate * 0.1)
    )
    stream.start()

    last_process_time = 0
    # Optional: log transcriptions for debugging
    log_file = open("whisper_log.txt", "a", encoding="utf-8")

    while running:
        now = time.time()
        if now - last_process_time >= PROCESS_INTERVAL:
            last_process_time = now
            if len(audio_buffer) > sample_rate * 0.5:
                audio_segment = audio_buffer.copy()
                segments, _ = model.transcribe(audio_segment, beam_size=1, language="en")
                transcription = " ".join(seg.text for seg in segments).strip()
                if transcription:
                    # Log to file for debugging
                    log_file.write(f"{time.time()}: {transcription}\n")
                    log_file.flush()
                    command_queue.put(transcription)
        time.sleep(0.05)

    log_file.close()
    stream.stop()
    stream.close()

def command_consumer():
    """Process transcriptions from the queue."""
    while running:
        try:
            text = command_queue.get(timeout=0.1)
            execute_command(text)
        except queue.Empty:
            pass

def main():
    global running, selected_device
    print("=" * 50)
    print("    Discord Voice Controller (Improved)")
    print("=" * 50)

    list_microphones()
    selected_device = select_microphone()

    # Start threads
    whisper_thread = threading.Thread(target=whisper_worker, daemon=True)
    whisper_thread.start()
    consumer_thread = threading.Thread(target=command_consumer, daemon=True)
    consumer_thread.start()

    # Run meter in main thread
    try:
        audio_level_meter()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        running = False
        time.sleep(0.5)

if __name__ == "__main__":
    main()