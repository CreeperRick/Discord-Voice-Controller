# 🎙️ Discord Voice Controller (Whisper)

Control your Discord microphone mute, deafen, and camera hands‑free using **voice commands** and **OpenAI Whisper** (offline).  
Includes a live mic level meter, fuzzy command matching, and a transcription log.

## 📦 What you need to install locally (from scratch)

### 1. Python (3.8 or newer)

- **Windows**: Download from [python.org]([https://www.python.org/downloads/](https://www.python.org/downloads/release/python-3119/))  
  ✅ **Check** “Add Python to PATH” during installation.

- **macOS**:  
  ```bash
  brew install python@3.11
  ```
  or download from [python.org]([https://www.python.org/downloads/](https://www.python.org/downloads/release/python-3119/)).
- Linux (Ubuntu/Debian):
  
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip python3-venv
  ```
Verify installation by opening a terminal (Command Prompt / PowerShell / bash) and typing:

  ```bash
  python --version
  ```
  Should show Python 3.8+.
 
# 2. Pip (Python package manager)
Pip comes installed with Python 3.4+. To verify pip is installed:

```bash
python -m pip --version
```
If pip is not installed (very rare), install it manually:

Windows:

```bash
python -m ensurepip --upgrade
```
macOS / Linux:

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```
Upgrade pip to the latest version (recommended):

```bash
python -m pip install --upgrade pip
```
# 3. Virtual environment (recommended)
  Create and activate one:
  
  - Windows:

    ```bash
    python -m venv discord_env
    discord_env\Scripts\activate
     ```
- macOS / Linux:
   ```bash
  python3 -m venv discord_env
  source discord_env/bin/activate
  ```
  You’ll see (discord_env) at the start of your terminal line.

# 4. Required Python packages
  With the virtual environment activated, run:
  
  ```bash
  python -m pip install sounddevice numpy keyboard faster-whisper
  ```
  On Linux you may need system audio libraries first:
  ```sudo apt install portaudio19-dev python3-pyaudio```
  
  On macOS with Homebrew:
  ```brew install portaudio```
# 5. (Optional) Hugging Face token – remove rate‑limit warning
  Get a free token at huggingface.co/settings/tokens (read permission).
  Set it as environment variable:
  
  - Windows Command Prompt:

    cmd
    ``` cmd
    set HF_TOKEN=hf_xxxxxxxxxxxx
    ```
    Windows PowerShell:
  
    powershell  
    ``` powershell
    $env:HF_TOKEN = "hf_xxxxxxxxxxxx"
    ```
- macOS / Linux:
  
  ```bash
  export HF_TOKEN="hf_xxxxxxxxxxxx"
  ```
  If you skip this, the script still works – you’ll just see a warning.
# 🎮 Discord keybind setup (required for camera)
The script simulates keyboard shortcuts. Camera toggling needs a custom keybind:

1. Open Discord → User Settings (gear icon)

2. Go to Keybinds → Add a Keybind

3. Action: ```Toggle Video```

4. Keybind: press ```Ctrl+Shift+V``` (or any – but update the script if you change it)

Save.

Default shortcuts (work out of the box):

- ```Ctrl+Shift+M``` → Mute microphone

- ```Ctrl+Shift+D``` → Deafen

- ```Ctrl+Shift+V``` → Toggle video (needs above setup)

# 🚀 Running the script
1. Save the script as discord_voice_controller.py in a folder.

2. Open a terminal in that folder.

3. Activate the virtual environment (if you created one).

4. Run:

```bash
python discord_voice_control.py
```
# First run:
- The script lists your input devices – type the number of your microphone.

- It downloads the Whisper model (tiny ~75MB) – this happens once.

- You’ll see a live level meter:
[████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0.35

### Voice commands:
- ```"mute"``` / ```"unmute"``` – toggle mic mute

- ```"deafen"``` – toggle deafen

- ```"camera on"``` – toggle video (requires Discord keybind)

The console will show what Whisper heard and play a confirmation beep.

Press ```Ctrl+C``` to stop.


# 🐛 Troubleshooting
Problem	Fix

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `python not recognized` | Python not in PATH – reinstall with “Add to PATH” or use `py` instead of `python` on Windows. |
| `pip install` fails on Linux | Run `sudo apt install portaudio19-dev python3-dev` then try again. |
| Microphone not working | Check OS sound settings, then restart script and choose a different device number. |
| Commands ignored | Look at `whisper_log.txt` – it shows exactly what was transcribed. Increase `BUFFER_DURATION` or change `WHISPER_MODEL_SIZE = "base"` in the script. |
| Camera command does nothing | You **must** set the `Toggle Video` keybind in Discord manually (see instructions). |
| Keyboard shortcuts don’t affect Discord | Run terminal as **administrator/root** – some systems block global hotkeys otherwise. |


# 📄 License
MIT – see LICENSE file.

---

## 🐍 The script itself (`discord_voice_controller.py`)

You already have it from the previous answer – keep it as the third file in your repo.  

Now your GitHub repository will have **three files**:
- `LICENSE`
- `README.md`
- `discord_voice_controller.py`

All ready for users to clone and run.
