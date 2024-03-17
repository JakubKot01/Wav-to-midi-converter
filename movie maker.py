from moviepy.video.fx.resize import resize as resize_clip
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
from tqdm import tqdm
import os

FPS = 30
RESOLUTION = (1920, 1080)
AUDIO_FILE = "sample 3 - piano (short sample).wav"
CONTENT_FOLDER = "content"

# Znajdź wszystkie pliki w folderze "content"
image_files = [os.path.join(CONTENT_FOLDER, f) for f in os.listdir(CONTENT_FOLDER) if os.path.isfile(os.path.join(CONTENT_FOLDER, f))]

# Inicjalizacja paska postępu
progress_bar = tqdm(total=len(image_files), desc="Loading images")

# Ładowanie obrazów jako sekwencji klipów obrazów
image_clips = []
for image_file in image_files:
    clip = ImageSequenceClip([image_file], fps=FPS)
    resized_clip = resize_clip(clip, newsize=RESOLUTION)
    image_clips.append(resized_clip)
    progress_bar.update(1)

# Zakończenie paska postępu
progress_bar.close()

# Ładowanie pliku audio jako klipu audio
audio_clip = AudioFileClip(AUDIO_FILE)

# Inicjalizacja paska postępu dla łączenia klipów wideo
progress_bar_concat = tqdm(total=len(image_clips), desc="Concatenating video clips")

# Łączenie klipów obrazów w jeden klip wideo
video_clip = concatenate_videoclips(image_clips, method="compose")

# Dodanie ścieżki dźwiękowej do klipu wideo
video_clip = video_clip.set_audio(audio_clip)

# Zakończenie paska postępu
progress_bar_concat.close()

# Zapisanie klipu wideo do pliku
output_file = "output_video.mp4"
video_clip.write_videofile(output_file, fps=FPS, codec="libx264", audio_codec="aac")
