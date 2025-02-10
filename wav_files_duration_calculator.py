import os
import wave
import contextlib

def get_total_duration(directory):
    total_duration = 0.0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                try:
                    with contextlib.closing(wave.open(file_path, 'r')) as wav_file:
                        frames = wav_file.getnframes()
                        rate = wav_file.getframerate()
                        duration = frames / float(rate)
                        total_duration += duration
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    return total_duration

def main():
    parent_directory = input("Enter the parent directory: ").strip()
    
    if not os.path.isdir(parent_directory):
        print(f"Invalid directory: {parent_directory}")
        return
    
    subdirectories = [os.path.join(parent_directory, d) for d in os.listdir(parent_directory) 
                      if os.path.isdir(os.path.join(parent_directory, d))]
    subdirectories.append(parent_directory)
    
    total_duration = 0.0
    for directory in subdirectories:
        duration = get_total_duration(directory)
        print(f"Total duration in {directory}: {duration:.2f} seconds")
        total_duration += duration
    
    print(f"Total duration across all directories: {total_duration:.2f} seconds")

if __name__ == "__main__":
    main()