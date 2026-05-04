# 🎙️ Discord Voice Controller (Whisper)

Control your Discord microphone mute, deafen, and camera hands‑free using **voice commands** and **OpenAI Whisper** for local speech recognition.  
Includes a live microphone level meter and fuzzy command matching to catch common misrecognitions (e.g., “mood” → “mute”).

## ✨ Features

- **Voice commands** – say “mute”, “unmute”, “deafen”, “camera on”  
- **Real‑time audio meter** – console bar graph shows your mic level  
- **Microphone selection** – choose your input device at startup  
- **Fuzzy matching** – catches slight mispronunciations (“boot” → “mute”)  
- **Confirmation beep** – audible feedback when a command is executed  
- **Transcription log** – saves all recognized text to `whisper_log.txt` for debugging  
- **Fully offline** – Whisper runs locally, no cloud API required  

## 📦 Requirements

- Python 3.8 or newer  
- A working microphone  
- Discord Desktop (the script simulates keyboard shortcuts)

## 🔧 Installation

### 1. Clone or download the repository

```bash
git clone https://github.com/yourusername/discord-voice-controller.git
cd discord-voice-controller
