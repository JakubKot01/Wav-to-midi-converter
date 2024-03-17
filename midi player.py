import mido
import pyvst

# Ścieżka do pliku MIDI
midi_file_path = "sciezka/do/pliku.mid"

# Wczytaj plik MIDI
mid = mido.MidiFile(midi_file_path)

# Inicjalizacja hosta VST
host = pyvst.VstHost()

# Wczytaj plugin VST
plugin_path = "sciezka/do/pluginu.vst"
plugin = host.load_plugin(plugin_path)

# Ustawienia pluginu VST (opcjonalne)
plugin.set_sample_rate(44100)
plugin.set_block_size(512)
plugin.resume()

# Pętla przez wydarzenia MIDI
for msg in mid.play():
    # Wysyłanie wiadomości MIDI do pluginu VST
    plugin.process_midi_event(msg)

    # Jeśli wiadomość to dźwięk, generuj dźwięk
    if msg.type == "note_on":
        plugin.process_audio(None, 512)

# Zatrzymaj plugin VST
plugin.suspend()

# Zwolnij zasoby
host.unload_plugin(plugin)
