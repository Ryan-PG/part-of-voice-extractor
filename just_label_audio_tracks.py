import os
import librosa
import soundfile as sf
import csv
import re

def extract_number(filename):
    match = re.search(r'(\d+)\.(\d+)', filename)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        return (major, minor)
    else:
        # fallback if no major.minor pattern, use first number or push to end
        match = re.search(r'(\d+)', filename)
        return (int(match.group(1)), 0) if match else (float('inf'), float('inf'))


def get_audio_length(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=None)
        return round(len(audio) / sr, 2)  # length in seconds, rounded to 2 decimals
    except Exception as e:
        print(f"Error reading length for {file_path}: {e}")
        return 0.0

def build_csv_from_labels(labels_dir, voices_dir, output_dir):
    file_type = input("Enter the file type ('mp3' or 'wav' or 'm4a'): (default = mp3) ").strip().lower()
    if file_type not in ['mp3', 'wav', 'm4a']:
        file_type = 'mp3'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt') and not f.endswith('_done.txt')]

    if len(label_files) != 1:
        print("Error: There should be exactly one label file in the Labels directory.")
        return

    label_file = label_files[0]
    label_path = os.path.join(labels_dir, label_file)

    # List and sort all audio files numerically
    audio_files = sorted(
        [f for f in os.listdir(voices_dir) if f.endswith(f'.{file_type}')],
        key=extract_number
    )

    if not audio_files:
        print("Error: No audio files found in the Voices directory.")
        return

    voice_output_dir = os.path.join(output_dir, os.path.splitext(label_file)[0])
    if not os.path.exists(voice_output_dir):
        os.makedirs(voice_output_dir)

    csv_path = os.path.join(voice_output_dir, "segments_info.csv")

    with open(label_path, 'r', encoding='utf-8') as lf, open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Length (s)", "Label", "File Name"])

        lines = [line.strip() for line in lf if line.strip()]

        if len(lines) > len(audio_files):
            print("Warning: More labels than audio files. Some labels will be skipped.")

        for idx, label in enumerate(lines):
            if idx >= len(audio_files):
                break

            audio_file = audio_files[idx]
            audio_path = os.path.join(voices_dir, audio_file)
            length = get_audio_length(audio_path)

            csv_writer.writerow([length, label, audio_file])
            print(f"Mapped label '{label}' to audio file '{audio_file}' with length {length} seconds")

    #! Rename label file to mark as done
    done_label_path = os.path.join(labels_dir, label_file.replace(".txt", "_done.txt"))
    os.rename(label_path, done_label_path)

    print(f"CSV built successfully at {csv_path}")

# Usage
labels_folder = "Labels"
voices_folder = "Voices"
output_folder = "Extracted_Voices"

build_csv_from_labels(labels_folder, voices_folder, output_folder)
