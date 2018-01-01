#!/usr/bin/env python

"""midi_notes.py: MIDI Note indexed frequency and name lists.
"""

__version__     = "0.2.2"
__status__      = "Development"

__author__      = "Randy Rubin"
__copyright__   = "Copyright 2018, Randy Rubin"
__license__     = "MIT"


# returns a list of 128 MIDI note frequencies

def freqs():
    midi_note_freqs = []
    for i in range(2**7):
        midi_note_freqs.append(2 ** ((i - 69) / 12) * 440.0)
    return midi_note_freqs


# returns a list of 128 MIDI note names 

def names():
    midi_note_names = []

    midi_note_names.append("C-1")
    midi_note_names.append("C#-1")
    midi_note_names.append("D-1")
    midi_note_names.append("D#-1")
    midi_note_names.append("E-1")
    midi_note_names.append("F-1")
    midi_note_names.append("F#-1")
    midi_note_names.append("G-1")
    midi_note_names.append("G#-1")
    midi_note_names.append("A-1")
    midi_note_names.append("A#-1")
    midi_note_names.append("B-1")

    midi_note_names.append("C0")
    midi_note_names.append("C#0")
    midi_note_names.append("D0")
    midi_note_names.append("D#0")
    midi_note_names.append("E0")
    midi_note_names.append("F0")
    midi_note_names.append("F#0")
    midi_note_names.append("G0")
    midi_note_names.append("G#0")
    midi_note_names.append("A0")
    midi_note_names.append("A#0")
    midi_note_names.append("B0")

    midi_note_names.append("C1")
    midi_note_names.append("C#1")
    midi_note_names.append("D1")
    midi_note_names.append("D#1")
    midi_note_names.append("E1")
    midi_note_names.append("F1")
    midi_note_names.append("F#1")
    midi_note_names.append("G1")
    midi_note_names.append("G#1")
    midi_note_names.append("A1")
    midi_note_names.append("A#1")
    midi_note_names.append("B1")

    midi_note_names.append("C2")
    midi_note_names.append("C#2")
    midi_note_names.append("D2")
    midi_note_names.append("D#2")
    midi_note_names.append("E2")
    midi_note_names.append("F2")
    midi_note_names.append("F#2")
    midi_note_names.append("G2")
    midi_note_names.append("G#2")
    midi_note_names.append("A2")
    midi_note_names.append("A#2")
    midi_note_names.append("B2")

    midi_note_names.append("C3")
    midi_note_names.append("C#3")
    midi_note_names.append("D3")
    midi_note_names.append("D#3")
    midi_note_names.append("E3")
    midi_note_names.append("F3")
    midi_note_names.append("F#3")
    midi_note_names.append("G3")
    midi_note_names.append("G#3")
    midi_note_names.append("A3")
    midi_note_names.append("A#3")
    midi_note_names.append("B3")

    midi_note_names.append("C4")
    midi_note_names.append("C#4")
    midi_note_names.append("D4")
    midi_note_names.append("D#4")
    midi_note_names.append("E4")
    midi_note_names.append("F4")
    midi_note_names.append("F#4")
    midi_note_names.append("G4")
    midi_note_names.append("G#4")
    midi_note_names.append("A4")
    midi_note_names.append("A#4")
    midi_note_names.append("B4")

    midi_note_names.append("C5")
    midi_note_names.append("C#5")
    midi_note_names.append("D5")
    midi_note_names.append("D#5")
    midi_note_names.append("E5")
    midi_note_names.append("F5")
    midi_note_names.append("F#5")
    midi_note_names.append("G5")
    midi_note_names.append("G#5")
    midi_note_names.append("A5")
    midi_note_names.append("A#5")
    midi_note_names.append("B5")

    midi_note_names.append("C6")
    midi_note_names.append("C#6")
    midi_note_names.append("D6")
    midi_note_names.append("D#6")
    midi_note_names.append("E6")
    midi_note_names.append("F6")
    midi_note_names.append("F#6")
    midi_note_names.append("G6")
    midi_note_names.append("G#6")
    midi_note_names.append("A6")
    midi_note_names.append("A#6")
    midi_note_names.append("B6")

    midi_note_names.append("C7")
    midi_note_names.append("C#7")
    midi_note_names.append("D7")
    midi_note_names.append("D#7")
    midi_note_names.append("E7")
    midi_note_names.append("F7")
    midi_note_names.append("F#7")
    midi_note_names.append("G7")
    midi_note_names.append("G#7")
    midi_note_names.append("A7")
    midi_note_names.append("A#7")
    midi_note_names.append("B7")

    midi_note_names.append("C8")
    midi_note_names.append("C#8")
    midi_note_names.append("D8")
    midi_note_names.append("D#8")
    midi_note_names.append("E8")
    midi_note_names.append("F8")
    midi_note_names.append("F#8")
    midi_note_names.append("G8")
    midi_note_names.append("G#8")
    midi_note_names.append("A8")
    midi_note_names.append("A#8")
    midi_note_names.append("B8")

    midi_note_names.append("C9")
    midi_note_names.append("C#9")
    midi_note_names.append("D9")
    midi_note_names.append("D#9")
    midi_note_names.append("E9")
    midi_note_names.append("F9")
    midi_note_names.append("F#9")
    midi_note_names.append("G9")

    return midi_note_names
