import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import plotly.graph_objects as go
import os
import shutil
import numpy as np
import tqdm
from concurrent.futures import ThreadPoolExecutor
import pickle

content_dir = os.path.join(os.getcwd(), "dramatic_piano_sample")

# Usunięcie katalogu "content" i jego zawartości
shutil.rmtree(content_dir, ignore_errors=True)

# Utworzenie nowego katalogu "content"
os.makedirs(content_dir, exist_ok=True)

AUDIO_FILE = "full-loud-glide-piano-dramatic-loop_140bpm_G_minor.wav"

# Configuration
FPS = 50
FFT_WINDOW_SECONDS = 0.25  # how many seconds of audio make up an FFT window

# Note range to display
FREQ_MIN = 10
FREQ_MAX = 1000

# TOP_NOTES = 4

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Output size. Generally use SCALE for higher res, unless you need a non-standard aspect ratio.
RESOLUTION = (1920, 1080)
SCALE = 1  # 0.5=QHD(960x540), 1=HD(1920x1080), 2=4K(3840x2160)

fs, data = wavfile.read(AUDIO_FILE)
audio = data.T[0]
FRAME_STEP = (fs / FPS)
FFT_WINDOW_SIZE = int(fs * FFT_WINDOW_SECONDS)
AUDIO_LENGTH = len(audio) / fs

note_recognition_threshold = 0.3


def plot_fft(p, xf, fs, notes, dimensions=(960, 540)):
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

    fig.add_trace(go.Scatter(
        x=xf,
        y=p))

    for note in notes:
        fig.add_annotation(x=note[0] + 10, y=note[2],
                           text=note[1],
                           font={'size': 48},
                           showarrow=False)
    return fig


def extract_sample(audio, frame_number):
    end = frame_number * FRAME_OFFSET
    begin = int(end - FFT_WINDOW_SIZE)

    if end == 0:
        # We have no audio yet, return all zeros (very beginning)
        return np.zeros((np.abs(begin)), dtype=float)
    elif begin < 0:
        # We have some audio, padd with zeros
        return np.concatenate([np.zeros((np.abs(begin)), dtype=float), audio[0:end]])
    else:
        # Usually this happens, return the next sample
        return audio[begin:end]


def find_top_notes(fft):
    if np.max(fft.real) < 0.001:
        return []

    lst = [x for x in enumerate(fft.real)]
    lst = sorted(lst, key=lambda x: x[1], reverse=True)

    max_y = max(x[1] for x in lst)

    idx = 0
    found = []
    found_note = set()
    while idx < len(lst):
        f = xf[lst[idx][0]]
        y = lst[idx][1]
        n = freq_to_number(f)
        n0 = int(round(n))
        name = note_name(n0)

        if name not in found_note and y > note_recognition_threshold * max_y:
            found_note.add(name)
            s = [f, note_name(n0), y]
            found.append(s)
        idx += 1

    return found


def freq_to_number(f):
    if f <= 0:
        return 0  # lub wartość, która jest odpowiednia dla twojego zastosowania
    else:
        return 69 + 12 * np.log2(f / 440.0)


def number_to_freq(n): return 440 * 2.0 ** ((n - 69) / 12.0)


def note_name(n): return NOTE_NAMES[n % 12] + str(int(n / 12 - 1))


window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, FFT_WINDOW_SIZE, False)))

xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1 / fs)
FRAME_COUNT = int(AUDIO_LENGTH * FPS)
print(AUDIO_LENGTH)
FRAME_OFFSET = int(len(audio) / FRAME_COUNT)

mx = 0
for frame_number in range(FRAME_COUNT):
    sample = extract_sample(audio, frame_number)

    fft = np.fft.rfft(sample * window)
    fft = np.abs(fft).real
    mx = max(np.max(fft), mx)

print(f"Max amplitude: {mx}")

big_notes_result = []


# Function to process each frame in parallel
def process_frame(frame_number):
    sample = extract_sample(audio, frame_number)
    fft = np.fft.rfft(sample * window)
    # fft = np.abs(fft) / mx
    s = find_top_notes(fft)
    big_notes_result.append(s)
    return fft.real, s


# Process frames in parallel
with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(tqdm.tqdm(executor.map(process_frame, range(FRAME_COUNT)), total=FRAME_COUNT))

# Save the frames
for frame_number, (fft, s) in enumerate(results):
    fig = plot_fft(fft, xf, fs, s, RESOLUTION)
    fig.write_image(os.path.join(content_dir, f"frame{frame_number}.png"), scale=2)

# Zapisywanie tablicy big_notes_result przy użyciu pickle
with open('dramatic_piano_sample.pickle', 'wb') as f:
    pickle.dump(big_notes_result, f)
