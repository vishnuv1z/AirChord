import time
import winsound
from pathlib import Path


CHORD_AUDIO_DIR = Path(__file__).parent / "assets" / "audio" / "chords"
CHORD_AUDIO_FILES = {
    "C": CHORD_AUDIO_DIR / "C.wav",
    "G": CHORD_AUDIO_DIR / "G.wav",
    "D": CHORD_AUDIO_DIR / "D.wav",
    "A": CHORD_AUDIO_DIR / "A.wav",
    "E": CHORD_AUDIO_DIR / "E.wav",
    "Am": CHORD_AUDIO_DIR / "Am.wav",
    "Em": CHORD_AUDIO_DIR / "Em.wav",
    "Dm": CHORD_AUDIO_DIR / "Dm.wav",
}


class ChordAudioPlayer:
    def __init__(self, cooldown_seconds=0.45):
        self.current_chord = None
        self.last_play_time = 0
        self.cooldown_seconds = cooldown_seconds

    def play_chord(self, chord, force=False):
        now = time.monotonic()
        can_replay = now - self.last_play_time >= self.cooldown_seconds

        if not force and chord == self.current_chord:
            return
        if force and not can_replay:
            return

        audio_path = CHORD_AUDIO_FILES.get(chord)
        if audio_path is None or not audio_path.exists():
            print(f"Missing audio file for {chord}: {audio_path}")
            self.current_chord = chord
            self.last_play_time = now
            return

        winsound.PlaySound(str(audio_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.current_chord = chord
        self.last_play_time = now

    def stop(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.current_chord = None
