import mido
from mido import MidiFile, MidiTrack, Message

# Definicje dźwięków
A4 = 69  # Numer dźwięku A4 w standardzie MIDI
E5 = 76  # Numer dźwięku E5 w standardzie MIDI
tempo = 120

# Tworzenie nowego pliku MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Przeliczenie opóźnienia na jednostki ticka
delay_ticks = int(mido.second2tick(0.5, mid.ticks_per_beat, mido.bpm2tempo(tempo)))

# Dodanie wiadomości o naciśnięciu klawisza dla dźwięku A4
track.append(Message('note_on', note=A4, velocity=64, time=0))

# Dodanie wiadomości o naciśnięciu klawisza dla dźwięku E5 z odpowiednim opóźnieniem
track.append(Message('note_on', note=E5, velocity=64, time=delay_ticks))

# Dodanie wiadomości o puszczeniu klawisza dla dźwięku A4 po 0.5 sekundy
track.append(Message('note_off', note=A4, velocity=64, time=delay_ticks))

# Dodanie wiadomości o puszczeniu klawisza dla dźwięku E5 po kolejnych 0.5 sekundy
track.append(Message('note_off', note=E5, velocity=64, time=delay_ticks))

# Zapisanie pliku MIDI
mid.save('output.mid')