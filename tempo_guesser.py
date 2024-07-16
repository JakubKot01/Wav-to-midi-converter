import librosa
import matplotlib.pyplot as plt


def plot_beats(file_path):
    y, sr = librosa.load(file_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    # Wyświetlenie tempa
    print(f"Detected tempo: {tempo:.2f} BPM")

    # Utworzenie wykresu fali dźwiękowej
    plt.figure(figsize=(14, 5))
    plt.plot(y, alpha=0.6)

    # Zaznaczenie bitów na wykresie
    beat_times = librosa.frames_to_time(beats, sr=sr)
    for beat_time in beat_times:
        plt.axvline(x=beat_time, color='r', linestyle='--', alpha=0.8)

    plt.title(f'Tempo: {tempo:.2f} BPM')
    plt.xlabel('Czas (s)')
    plt.ylabel('Amplituda')
    plt.show()


# Przykładowe użycie
file_path = 'dramatic piano sample.wav'
plot_beats(file_path)
