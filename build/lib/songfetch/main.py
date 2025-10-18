import os
from songfetch.ascii_convert import convert
from songfetch.player_utils import (
    get_art,
    get_player_name,
    get_title,
    get_artist,
    get_album,
    get_duration_formatted,
    get_volume,
    get_backend,
    get_duration,
    get_position
)

def progress_bar():
    # Calculate percentage
    pos = get_position()
    dur = get_duration()
    if pos == 0 or dur == 0:
        percentage = 0
    else:
        percentage = pos / dur

    # Calculate filled and empty characters
    filled = int(percentage * 16)
    empty = 16 - filled
    fprint = "▓" * filled
    eprint = "░" * empty

    # Convert microseconds to seconds
    pos_seconds = int(pos / 1000000)
    dur_seconds = int(dur / 1000000)

    # Nicer representation
    display_pos = f"{pos_seconds // 60:02d}:{pos_seconds % 60:02d}"
    display_dur = f"{dur_seconds // 60:02d}:{dur_seconds % 60:02d}"

    # Full representation
    display_str = f"\033[0m {display_pos} / {display_dur} ({round(percentage * 100)}%)"

    return fprint + eprint + display_str

def get_info_line():
    # Line separator
    line = f"\033[34m─────────────────────────────────────────\033[0m"
    now_playing = "Now Playing"
    playback_info = "Playback Info"

    # ANSI color palettes
    normal = "".join([f"\033[4{i}m   \033[0m" for i in range(8)])
    bright = "".join([f"\033[10{i}m   \033[0m" for i in range(8)])

    # Concatenate info lines
    info_lines = [
        # Track info
        f"\033[1;34m{get_player_name()}\033[0m",
        line, f"\033[97m{now_playing}\033[0m", line,
        f"\033[34mTitle\033[0m: {get_title()}",
        f"\033[34mArtist\033[0m: {get_artist()}",
        f"\033[34mAlbum\033[0m: {get_album()}",
        f"\033[34mDuration\033[0m: {get_duration_formatted()}",
        f"\033[34m{progress_bar()}\033[0m",

        # Player info (minimal, only volume and backend now)
        line, f"\033[97m{playback_info}\033[0m", line,
        f"\033[34mVolume\033[0m: {get_volume()}",
        f"\033[34mBackend\033[0m: {get_backend()}",

        "",
        # Palette
        normal, bright
    ]
    return info_lines

def main():
    # Terminal size
    columns = os.get_terminal_size().columns
    max_width = 104

    if columns < max_width:
        art_col = []
        max_art = 2
    else:
        art_col = convert(get_art())
        max_art = max(len(x) for x in art_col)

    info_col = get_info_line()
    max_info = max(len(y) for y in info_col[:-2])

    # Print side by side
    if len(art_col) > len(info_col):
        new_info_col = info_col + [''] * (len(art_col) - len(info_col))
        for i in range(len(art_col)):
            print(f"{art_col[i]:{max_art-2}}{new_info_col[i]:{max_info}}")
    else:
        new_art_col = art_col + [''] * (len(info_col) - len(art_col))
        for j in range(len(info_col)):
            print(f"{new_art_col[j]:{max_art-2}}{info_col[j]:{max_info}}")

if __name__ == "__main__":
    main()
