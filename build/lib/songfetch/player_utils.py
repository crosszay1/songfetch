import subprocess, re

# Default values for fallback
DEFAULTS = {
    "player_name": "No player",
    "art": "",
    "title": "No title found",
    "artist": "No artist found",
    "album": "No album found",
    "duration_formatted": "00:00",
    "volume": "Unknown",
    "position": 0,
    "duration": 0,
}

# We'll need users audio backend (pipewire, pulse, etc.)
def get_backend():
    try:
        if subprocess.run(["pgrep", "-x", "pipewire"], capture_output=True, text=True).returncode == 0:
            return "PipeWire"
        elif subprocess.run(["pgrep", "-x", "pulseaudio"], capture_output=True, text=True).returncode == 0:
            return "PulseAudio"
        else:
            return "ALSA"
    except Exception:
        return "Unknown"

# MPRIS info functions
def get_player_name():
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{ playerName }}"], capture_output=True, text=True)
        name = result.stdout.strip()
        return name if name else DEFAULTS["player_name"]
    except Exception:
        return DEFAULTS["player_name"]

def get_art():
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{ mpris:artUrl }}"], capture_output=True, text=True)
        art = result.stdout.strip()
        return art if art else DEFAULTS["art"]
    except Exception:
        return DEFAULTS["art"]

def get_title():
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{ trunc(title, 33) }}"], capture_output=True, text=True)
        title = result.stdout.strip()
        return title if title else DEFAULTS["title"]
    except Exception:
        return DEFAULTS["title"]

def get_artist():
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{ trunc(artist, 32) }}"], capture_output=True, text=True)
        artist = result.stdout.strip()
        return artist if artist else DEFAULTS["artist"]
    except Exception:
        return DEFAULTS["artist"]

def get_album():
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{ trunc(album, 33) }}"], capture_output=True, text=True)
        album = result.stdout.strip()
        return album if album else DEFAULTS["album"]
    except Exception:
        return DEFAULTS["album"]

def get_duration_formatted():
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{ duration(mpris:length) }}"], capture_output=True, text=True)
        duration = result.stdout.strip()
        return duration if duration else DEFAULTS["duration_formatted"]
    except Exception:
        return DEFAULTS["duration_formatted"]

# Current volume
def get_volume():
    try:
        current_backend = get_backend()
        if current_backend == "PipeWire":
            result = subprocess.run(["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"], capture_output=True, text=True)
            final_result = re.search(r'\d+\.\d+', result.stdout)
            percentage = int(float(final_result.group()) * 100) if final_result else DEFAULTS["volume"]
        elif current_backend == "PulseAudio":
            result = subprocess.run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], capture_output=True, text=True)
            final_result = re.search(r'(\d+)%', result.stdout)
            percentage = int(final_result.group()) if final_result else DEFAULTS["volume"]
        else:
            result = subprocess.run(["amixer", "get", "Master"], capture_output=True, text=True)
            final_result = re.search(r'(\d+)%', result.stdout)
            percentage = int(final_result.group()) if final_result else DEFAULTS["volume"]
        return f"{percentage}%" if isinstance(percentage, int) else DEFAULTS["volume"]
    except Exception:
        return DEFAULTS["volume"]

def get_position():
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{ position }}"], capture_output=True, text=True)
        pos = result.stdout.strip()
        return int(pos) if pos.isdigit() else DEFAULTS["position"]
    except Exception:
        return DEFAULTS["position"]

def get_duration():
    try:
        result = subprocess.run(["playerctl", "metadata", "--format", "{{ mpris:length }}"], capture_output=True, text=True)
        dur = result.stdout.strip()
        return int(dur) if dur.isdigit() else DEFAULTS["duration"]
    except Exception:
        return DEFAULTS["duration"]
