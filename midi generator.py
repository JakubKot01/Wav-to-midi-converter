import pickle
from mido import MetaMessage, Message, MidiFile, MidiTrack
import mido
import numpy as np
from pprint import pprint

FILTER_VERBOSE = False

tempo = 92
FPS = 50

frame_length = (1 / FPS)
print(f'Frame length: {frame_length}')
# ticks_per_quarter_note = 960

# with open('big_notes_result_test.pickle', 'rb') as file:
with open('dramatic_piano_sample.pickle', 'rb') as file:
    big_notes_result = pickle.load(file)

notes_names_table = []
notes_volumes_table = []

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
    "C#7": 97, "Db7": 97, "D7": 98, "D#7": 99, "Eb7": 99, "E7": 100, "F7": 101, "F#7": 102, "Gb7": 102, "G7": 103,
    "G#7": 104, "Ab7": 104, "A7": 105, "A#7": 106, "Bb7": 106, "B7": 107,
    "C8": 108, "C#8": 109, "Db8": 109, "D8": 110, "D#8": 111, "Eb8": 111, "E8": 112, "F8": 113,
    "F#8": 114, "Gb8": 114, "G8": 115, "G#8": 116, "Ab8": 116, "A8": 117, "A#8": 118, "Bb8": 118,
    "B8": 119, "C9": 120, "C#9": 121, "Db9": 121, "D9": 122, "D#9": 123, "Eb9": 123, "E9": 124,
    "F9": 125, "F#9": 126, "Gb9": 126, "G9": 127
}

for notes in big_notes_result:
    current_notes = []
    current_volumes = []
    for note in notes:
        if note[1] in note_to_midi:
            current_notes.append(note[1])
            current_volumes.append(note[2])
    notes_names_table.append(current_notes)
    notes_volumes_table.append(current_volumes)

moll_tons = {
    "C-moll": ["C", "D", "D#", "F", "G", "G#", "A#"],
    "C#-moll": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "D-moll": ["D", "E", "F", "G", "A", "A#", "C"],
    "D#-moll": ["D#", "F", "F#", "G#", "A#", "B", "C#"],
    "E-moll": ["E", "F#", "G", "A", "B", "C", "D"],
    "F-moll": ["F", "G", "G#", "A#", "C", "C#", "D#"],
    "F#-moll": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "G-moll": ["G", "A", "A#", "C", "D", "D#", "F"],
    "G#-moll": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
    "A-moll": ["A", "B", "C", "D", "E", "F", "G"],
    "A#-moll": ["A#", "C", "C#", "D#", "F", "F#", "G#"],
    "H-moll": ["H", "C#", "D", "E", "F#", "G", "A"]
}

tons_sounds_counters = {
    "C-moll": 0.0,
    "C#-moll": 0.0,
    "D-moll": 0.0,
    "D#-moll": 0.0,
    "E-moll": 0.0,
    "F-moll": 0.0,
    "F#-moll": 0.0,
    "G-moll": 0.0,
    "G#-moll": 0.0,
    "A-moll": 0.0,
    "A#-moll": 0.0,
    "H-moll": 0.0
}

# TODO: Sprawdzić czy głośność narasta czy maleje

def is_note_stable(note_name, counter):
    if len(notes_names_table) - counter < 4:
        return True

    if note_name not in notes_names_table[counter + 1] \
            or note_name not in notes_names_table[counter + 2] \
            or note_name not in notes_names_table[counter + 3]:
        return False
    return True

def are_note_properties_ok(note_name, counter, active_notes):
    # Czy nuta jest w tonacji?
    # if note_name[:-1] not in moll_tons[found_ton]:
    #    return False

    # Czy nuta jest przesunięta o jeden półton?
    print(f"note_name: {note_name}")
    for note in active_notes:
        if note_to_midi[note_name] == note_to_midi[note] + 1 \
                or note_to_midi[note_name] == note_to_midi[note] - 1:
            return False

    if is_note_stable(note_name, counter):
        return True
    return False


def is_going_to_be_replaced(note, counter):
    if len(notes_names_table) - counter < 5:
        return False
    for i in range(counter, counter + 5):
        for incoming_notes in notes_names_table[i]:
            if note_to_midi[note] != note_to_midi[incoming_notes] - 1 \
                    and note_to_midi[note] != note_to_midi[incoming_notes] + 1:
                return False
    return True

mid = MidiFile(type=0)
track0 = MidiTrack()
mid.tracks.append(track0)

current_time = 0

current_notes = []
previous_notes = []

# Filtering

for counter, notes in enumerate(notes_names_table):
    for note_number, note in enumerate(notes):
        if is_note_stable(note, counter):
            current_notes.append(note)
        else:
            if counter < len(big_notes_result):
                if FILTER_VERBOSE:
                    print(f'\ncounter: {counter}, notes: {big_notes_result[counter]}')
                if note_number < len(big_notes_result[counter]):
                    if FILTER_VERBOSE:
                        print(f'Note counter: {note_number}, note: {big_notes_result[counter][note_number]}')
                    del big_notes_result[counter][note_number]
                else:
                    if FILTER_VERBOSE:
                        print(f'Note counter: {note_number} INDEX OUT OF RANGE')
            else:
                if FILTER_VERBOSE:
                    print(f'\nCounter: {counter} INDEX OUT OF RANGE')

    previous_notes = current_notes.copy()
    current_notes.clear()

# Creating midi file

notes_names_table = []
notes_volumes_table = []

for notes in big_notes_result:
    current_notes = []
    current_volumes = []
    for note in notes:
        if note[1] in note_to_midi:
            current_notes.append(note[1])
            current_volumes.append(note[2])
    notes_names_table.append(current_notes)
    notes_volumes_table.append(current_volumes)

active_notes = {}

# for counter, notes in enumerate(notes_names_table):
#     for note_number, note in enumerate(notes):
#         for ton in moll_tons:
#             if note[:-1] in moll_tons[ton]:
#                 if note[:-1] in active_notes:
#                     del active_notes[note[:-1]]
#                 else:
#                     print(f'note: {note} counted for tone: {ton}')
#                     tons_sounds_counters[ton] += notes_volumes_table[counter][note_number]
#                     active_notes[note[:-1]] = 1
#             else:
#                 tons_sounds_counters[ton] -= notes_volumes_table[counter][note_number]
#
# found_ton = max(tons_sounds_counters, key=tons_sounds_counters.get)
#
# pprint(tons_sounds_counters)
# print(f'found tone: {found_ton}')

current_notes = []
previous_notes = []
current_time = 0
counter = 0
last_message_time = 0

active_notes = {}

for counter, notes in enumerate(notes_names_table):
    delay_ticks = mido.second2tick(current_time - last_message_time, mid.ticks_per_beat, mido.bpm2tempo(tempo))
    for note_number, note in enumerate(notes):
        if note not in previous_notes:
            if are_note_properties_ok(note, counter, active_notes):
                track0.append(Message('note_on',
                                      note=int(note_to_midi[note]),
                                      velocity=64,
                                      time=delay_ticks))
                print(f'Note {note} activated from frame No. {counter} at time {current_time}')
                current_notes.append(note)
                active_notes[note] = current_time
                last_message_time = current_time
        else:
            current_notes.append(note)

    for note in previous_notes:
        if note not in current_notes \
                or is_going_to_be_replaced(note, counter):
            track0.append(Message('note_off',
                                  note=int(note_to_midi[note]),
                                  velocity=0,
                                  time=delay_ticks))
            print(f'Note {note} deactivated from frame No. {counter} at time {current_time}')
            del active_notes[note]
            last_message_time = current_time

    current_time += frame_length
    previous_notes = current_notes.copy()
    current_notes.clear()

mid.save('dramatic_piano_sample.mid')
