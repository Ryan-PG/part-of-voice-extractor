import os
import librosa
import soundfile as sf
import csv

def extract_labeled_audio(labels_dir, voices_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    total_length_sum = 0

    for label_file in os.listdir(labels_dir):
        if label_file.endswith(".txt"):
            voice_file = label_file.replace(".txt", ".wav")
            label_path = os.path.join(labels_dir, label_file)
            voice_path = os.path.join(voices_dir, voice_file)
            
            if not os.path.exists(voice_path):
                print(f"Warning: Corresponding audio file not found for {label_file}")
                continue

            voice_output_dir = os.path.join(output_dir, os.path.splitext(voice_file)[0])
            if not os.path.exists(voice_output_dir):
                os.makedirs(voice_output_dir)
            
            csv_path = os.path.join(voice_output_dir, "segments_info.csv")
            length_sum = 0

            with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Start Time", "End Time", "Length", "Label", "File Name"])
                
                audio, sr = librosa.load(voice_path, sr=None)
                
                with open(label_path, 'r', encoding='utf-8') as f:
                    for idx, line in enumerate(f):
                        parts = line.strip().split('\t')
                        if len(parts) == 3:
                            start_time, end_time, label = parts
                            start_time, end_time = float(start_time), float(end_time)

                            segment_length = end_time - start_time
                            if 5 <= segment_length <= 30:
                                
                                start_sample = int(start_time * sr)
                                end_sample = int(end_time * sr)
                                segment = audio[start_sample:end_sample]
                                
                                segment_filename = f"part{idx + 1}.wav"
                                segment_path = os.path.join(voice_output_dir, segment_filename)
                                sf.write(segment_path, segment, sr)
                                
                                csv_writer.writerow([start_time, end_time, segment_length, label, segment_filename])
                                length_sum += segment_length
                                print(f"Extracted segment saved: {segment_path}")
                
                csv_writer.writerow(["Total", "", length_sum, "", ""])
                total_length_sum += length_sum

    print(f"Total length of all extracted segments: {total_length_sum} seconds")

labels_folder = "Labels"
voices_folder = "Voices"
output_folder = "Extracted_Voices"

extract_labeled_audio(labels_folder, voices_folder, output_folder)