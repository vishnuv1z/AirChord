# AirChord

AirChord is a simple Python project that lets you play guitar chords using your webcam. It uses hand tracking to detect your hands, a chord wheel UI to choose chords, and audio files to play the selected chord.

I made this as a small learning project to explore Python libraries like OpenCV and MediaPipe, and to understand how camera input, hand tracking, UI drawing, and audio playback can work together.

## Features

- Webcam-based hand tracking
- Chord wheel interface
- Left hand index finger selects chords by hovering over wheel sectors
- Right hand gestures control playback
- Support for adding custom guitar chord audio files

## How It Works

- Move your left hand index finger over a chord sector in the wheel.
- The hovered chord becomes the active chord.
- Use your right hand to control playback:
  - Open hand: play the selected chord
  - One finger: strum or retrigger the selected chord
  - Fist: mute or stop audio

## Requirements

Install the required Python libraries:

```powershell
pip install opencv-python mediapipe
```

This project currently uses Python's built-in Windows audio playback through `winsound`, so chord audio files should be `.wav` files.

## Adding Chord Audio

Add your chord audio files inside (or replace the existing ones):

```text
assets/audio/chords/
```

Use these exact filenames:

```text
C.wav
G.wav
D.wav
A.wav
E.wav
Am.wav
Em.wav
Dm.wav
```

Short guitar chord samples work best.

## Running The Project

From the project folder, run:

```powershell
python main.py
```

Allow camera access if your system asks for permission.

Press `Q` to close the app.

## Project Structure

```text
guitar-chords/
├── assets/
│   └── audio/
│       └── chords/
├── audio_player.py
├── chord_wheel.py
├── main.py
└── README.md
```

## Contributing

Anyone can use this project, modify it, or contribute improvements. Ideas like better gesture detection, more chord options, smoother UI, cross-platform audio support, or real-time guitar effects are welcome.
