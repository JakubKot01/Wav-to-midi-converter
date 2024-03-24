import mido


def print_midi_file_contents(midi_file_path):
    try:
        mid = mido.MidiFile(midi_file_path)
        print("Format:", mid.type)
        print("Ticks per beat:", mid.ticks_per_beat)
        print("Tracks:")
        for i, track in enumerate(mid.tracks):
            print(f"Track {i}:")
            for msg in track:
                print(msg)
    except Exception as e:
        print("Error:", e)


# Ścieżka do pliku MIDI
midi_file_path = "canon in D - test.mid"
# midi_file_path = "result.mid"
# midi_file_path = "oneNote.mid"
# midi_file_path = "twoNotes.mid"
# midi_file_path = "doubleNote.mid"

# Wywołanie funkcji
print_midi_file_contents(midi_file_path)
