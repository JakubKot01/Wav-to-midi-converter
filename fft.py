import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import plotly.graph_objects as go
import tqdm
import pickle

# Konfiguracja
AUDIO_FILE = "lo-fi piano sample.wav"
FPS = 50
FFT_WINDOW_SECONDS = 0.25  # ile sekund audio składa się na okno FFT
FREQ_MIN = 10
FREQ_MAX = 1000
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
RESOLUTION = (1920, 1080)
SCALE = 1  # 0.5=QHD(960x540), 1=HD(1920x1080), 2=4K(3840x2160)
NOTE_RECOGNITION_THRESHOLD = 0.3
CONTENT_DIR = os.path.join(os.getcwd(), "lo-fi_piano_sample")

# Przygotowanie katalogu
def prepare_directory(directory):
    shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory, exist_ok=True)

# Ekstrakcja próbki audio
def extract_sample(audio, frame_number, frame_offset, fft_window_size):
    end = frame_number * frame_offset
    begin = int(end - fft_window_size)

    if end == 0:
        return np.zeros((np.abs(begin)), dtype=float)
    elif begin < 0:
        return np.concatenate([np.zeros((np.abs(begin)), dtype=float), audio[0:end]])
    else:
        return audio[begin:end]

# Znalezienie głównych nut w FFT
def find_top_notes(fft, xf, note_recognition_threshold):
    if np.max(fft) < 0.001:
        return []

    lst = sorted(enumerate(fft), key=lambda x: x[1], reverse=True)
    max_y = max(x[1] for x in lst)
    found_notes = []
    found_note_set = set()

    for idx, value in lst:
        f = xf[idx]
        y = value
        n = freq_to_number(f)
        n0 = int(round(n))
        name = note_name(n0)

        if name not in found_note_set and y > note_recognition_threshold * max_y:
            found_note_set.add(name)
            found_notes.append([f, name, y])

    return found_notes

# Konwersje częstotliwości i numerów nut
def freq_to_number(f):
    return 69 + 12 * np.log2(f / 440.0) if f > 0 else 0

def number_to_freq(n):
    return 440 * 2.0 ** ((n - 69) / 12.0)

def note_name(n):
    return NOTE_NAMES[n % 12] + str(int(n / 12 - 1))

# Tworzenie wykresu FFT
def plot_fft(p, xf, notes, dimensions=(960, 540)):
    layout = go.Layout(
        title="frequency spectrum",
        autosize=False,
        width=dimensions[0],
        height=dimensions[1],
        xaxis_title="Frequency (note)",
        yaxis_title="Magnitude",
        font={'size': 24}
    )

    fig = go.Figure(layout=layout,
                    layout_xaxis_range=[FREQ_MIN, FREQ_MAX],
                    layout_yaxis_range=[0, 1]
                    )

    fig.add_trace(go.Scatter(x=xf, y=p))

    for note in notes:
        fig.add_annotation(x=note[0] + 10, y=note[2],
                           text=note[1],
                           font={'size': 48},
                           showarrow=False)
    return fig

# Główna funkcja przetwarzania audio
def process_audio():
    prepare_directory(CONTENT_DIR)

    # Odczyt pliku audio
    fs, data = wavfile.read(AUDIO_FILE)
    audio = data.T[0].astype(np.float32)
    frame_step = (fs / FPS)
    fft_window_size = int(fs * FFT_WINDOW_SECONDS)
    audio_length = len(audio) / fs
    frame_count = int(audio_length * FPS)
    frame_offset = int(len(audio) / frame_count)

    # Normalizacja danych audio do zakresu -1.0 do 1.0, jeśli są typu int16
    if audio.dtype == np.int16:
        audio = audio / 32768.0

    # Sprawdzenie typu danych i zakresu wartości
    print(f"Audio data type: {audio.dtype}")
    print(f"Sample values (first 10 samples): {audio[:10]}")

    # Okno FFT i częstotliwości
    window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, fft_window_size, False)))
    xf = np.fft.rfftfreq(fft_window_size, 1 / fs)

    # Znalezienie maksymalnej amplitudy
    max_amplitude = 0
    for frame_number in range(frame_count):
        sample = extract_sample(audio, frame_number, frame_offset, fft_window_size)
        fft = np.fft.rfft(sample * window)
        max_amplitude = max(np.max(np.abs(fft)), max_amplitude)

    print(f"Max amplitude: {max_amplitude}")

    big_notes_result = []
    results = []

    # Przetwarzanie każdej ramki
    for frame_number in tqdm.tqdm(range(frame_count)):
        sample = extract_sample(audio, frame_number, frame_offset, fft_window_size)
        fft = np.fft.rfft(sample * window)
        top_notes = find_top_notes(np.abs(fft), xf, NOTE_RECOGNITION_THRESHOLD)
        big_notes_result.append(top_notes)
        results.append((fft.real, top_notes))

    # Zapisanie wykresów
    for frame_number, (fft, notes) in enumerate(results):
        fig = plot_fft(fft, xf, notes, RESOLUTION)
        fig.write_image(os.path.join(CONTENT_DIR, f"frame{frame_number}.png"), scale=2)

    # Zapisanie wyników przy użyciu pickle
    with open('lo-fi_piano_sample.pickle', 'wb') as f:
        pickle.dump(big_notes_result, f)

# Uruchomienie głównej funkcji
if __name__ == "__main__":
    process_audio()
