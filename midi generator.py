import pickle
from mido import MetaMessage, Message, MidiFile, MidiTrack
from pprint import pprint

# Music21

# BPM = 84
BPM = 76
FPS = 30

quarter_note_length = 60 / BPM
sixteenth_note_length = quarter_note_length / 4

frame_length = 1 / FPS

ticks_per_quarter_note = 256

ticks_per_frame = int((ticks_per_quarter_note * BPM) // (60 * frame_length))

# Odczytaj tablicę z pliku
with open('big_notes_result.pickle', 'rb') as file:
    big_notes_result = pickle.load(file)

notes_names_table = []

for notes in big_notes_result:
    current_notes = []
    for note in notes:
        current_notes.append(note[1])
    notes_names_table.append(current_notes)

pprint(notes_names_table)
pprint(len(notes_names_table))


def is_note_stable(note_name, counter: int):
    if len(notes_names_table) - counter < 5:
        return True
    if note_name not in notes_names_table[counter + 1] \
            or note_name not in notes_names_table[counter + 2] \
            or note_name not in notes_names_table[counter + 3] \
            or note_name not in notes_names_table[counter + 4]:
        print(note_name)
        notes_names_table[counter].remove(note_name)
        return False
    return True


note_to_midi = {
    "C0": 12, "C#0": 13, "Db0": 13, "D0": 14, "D#0": 15, "Eb0": 15, "E0": 16, "F0": 17,
    "F#0": 18, "Gb0": 18, "G0": 19, "G#0": 20, "Ab0": 20, "A0": 21, "A#0": 22, "Bb0": 22,
    "B0": 23, "C1": 24, "C#1": 25, "Db1": 25, "D1": 26, "D#1": 27, "Eb1": 27, "E1": 28,
    "F1": 29, "F#1": 30, "Gb1": 30, "G1": 31, "G#1": 32, "Ab1": 32, "A1": 33, "A#1": 34,
    "Bb1": 34, "B1": 35, "C2": 36, "C#2": 37, "Db2": 37, "D2": 38, "D#2": 39, "Eb2": 39,
    "E2": 40, "F2": 41, "F#2": 42, "Gb2": 42, "G2": 43, "G#2": 44, "Ab2": 44, "A2": 45,
    "A#2": 46, "Bb2": 46, "B2": 47, "C3": 48, "C#3": 49, "Db3": 49, "D3": 50, "D#3": 51,
    "Eb3": 51, "E3": 52, "F3": 53, "F#3": 54, "Gb3": 54, "G3": 55, "G#3": 56, "Ab3": 56,
    "A3": 57, "A#3": 58, "Bb3": 58, "B3": 59, "C4": 60, "C#4": 61, "Db4": 61, "D4": 62,
    "D#4": 63, "Eb4": 63, "E4": 64, "F4": 65, "F#4": 66, "Gb4": 66, "G4": 67, "G#4": 68,
    "Ab4": 68, "A4": 69, "A#4": 70, "Bb4": 70, "B4": 71, "C5": 72, "C#5": 73, "Db5": 73,
    "D5": 74, "D#5": 75, "Eb5": 75, "E5": 76, "F5": 77, "F#5": 78, "Gb5": 78, "G5": 79,
    "G#5": 80, "Ab5": 80, "A5": 81, "A#5": 82, "Bb5": 82, "B5": 83, "C6": 84, "C#6": 85,
    "Db6": 85, "D6": 86, "D#6": 87, "Eb6": 87, "E6": 88, "F6": 89, "F#6": 90, "Gb6": 90,
    "G6": 91, "G#6": 92, "Ab6": 92, "A6": 93, "A#6": 94, "Bb6": 94, "B6": 95, "C7": 96,
    "C#7": 97, "Db7": 97, "D7": 98, "D#7": 99, "Eb7": 99, "E7": 100, "F7": 101, "F#7": 102,
    "Gb7": 102, "G7": 103, "G#7": 104, "Ab7": 104, "A7": 105, "A#7": 106, "Bb7": 106, "B7": 107,
    "C8": 108, "C#8": 109, "Db8": 109, "D8": 110, "D#8": 111, "Eb8": 111, "E8": 112, "F8": 113,
    "F#8": 114, "Gb8": 114, "G8": 115, "G#8": 116, "Ab8": 116, "A8": 117, "A#8": 118, "Bb8": 118,
    "B8": 119, "C9": 120, "C#9": 121, "Db9": 121, "D9": 122, "D#9": 123, "Eb9": 123, "E9": 124,
    "F9": 125, "F#9": 126, "Gb9": 126, "G9": 127
}

mid = MidiFile()
track0 = MidiTrack()
mid.tracks.append(track0)

# track0.append(MetaMessage('track_name', name='test', time=0))
# track0.append(MetaMessage('time_signature', numerator=4,
#                               denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))

mid.ticks_per_beat = ticks_per_quarter_note

track1 = MidiTrack()
mid.tracks.append(track1)

# Dodanie informacji o instrumencie
track1.append(Message('program_change', program=0))

current_notes = []
previous_notes = []
current_time = 0
current_time_offset = 0
counter = 0

for notes in notes_names_table:
    for note in notes:
        if note not in previous_notes:
            if is_note_stable(note, counter):
                track1.append(Message('note_on', note=int(note_to_midi[note]), velocity=64, time=current_time))
                current_notes.append(note)
        else:
            current_notes.append(note)
    print(f"counter: {counter}, current notes: {current_notes}, previous notes: {previous_notes}")
    print(f'offset: {current_time_offset}, current time: {current_time}')
    for note in previous_notes:
        if note not in current_notes:
            track1.append(Message('note_off', note=int(note_to_midi[note]), velocity=64, time=current_time))
    current_time += 1
    previous_notes = current_notes
    current_notes = []
    counter += 1
    print(current_time)

# pprint(mid)
mid.save('result.mid')

print(frame_length)


"""
TODO:
1. Sprawdzać czy dźwięk zniknął czy zmieniła się oktawa
"""
