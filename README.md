# Extract Labeled Audio Segments

This project provides a Python script to process labeled audio files by extracting specific segments based on timestamps provided in text files. Each extracted segment is saved as a separate audio file, and a CSV file is generated to document segment details.

## Features

- Reads label files containing timestamps and associated text labels.
- Extracts audio segments based on provided start and end times.
- Saves each extracted segment as a separate `.wav`/`.mp3` file.
- Generates a CSV file containing segment information:
  - Start Time
  - End Time
  - Length (in seconds)
  - Label
  - Extracted File Name
- Filters segments based on duration (5 to 30 seconds).
- Calculates the total duration of extracted segments and includes it in the CSV file.
- **Processed files are renamed to avoid duplicate processing on subsequent runs.**

## Folder Structure

```
.
├── Labels
│   ├── voice1.txt
│   ├── voice2.txt
│   └── ...
├── Voices
│   ├── voice1.wav
│   ├── voice2.wav
│   └── ...
├── Extracted_Voices
│   ├── voice1
│   │   ├── part1.wav
│   │   ├── part2.wav
│   │   ├── segments_info.csv
│   │   └── ...
│   └── voice2
├── extract_audio.py
└── README.md
```

## Requirements

Ensure you have the following dependencies installed:

- Python 3.x
- `librosa` (for audio processing)
- `soundfile` (for saving audio files)

You can install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your labeled text files inside the `Labels` directory.
2. Place your corresponding audio files inside the `Voices` directory.
3. Run the script to extract audio segments:

```bash
python extract_audio.py
```

\*\* Consider that every `txt` file name in Labels directory must be the same of a `.wav`/`.mp3` file name in Voices directory.

4. The extracted segments and CSV files will be saved in the `Extracted_Voices` directory.

### Extracting All Voices

If you want to extract all voice segments regardless of length, simply comment out the if-statement in the script that filters segments based on duration.

### Processed Files

Once a file is processed successfully, its name will be changed to `<txt_file_name>_done.txt` to prevent reprocessing in future runs.

## Example of Label File

Example content of a `voice1.txt` file:

```
185.092898\t188.701361\tحرق بزنید گوفتم چی شده
204.274181\t208.186754\tد شما اگه عرضه داشتید  تا به حال حقدونو گرفته بودید
```

Each line contains:

- Start Time (seconds)
- End Time (seconds)
- Text Label (speech transcription)

## Output

For each audio file, a corresponding folder will be created containing:

- Extracted audio segments in `.wav` format.
- A `segments_info.csv` file with detailed segment information.
- A final row in the CSV file containing the total duration of extracted segments.

Example of CSV file output:

```
Start Time,End Time,Length,Label,File Name
185.092898,188.701361,3.608463,حرق بزنید گوفتم چی شده,part1.wav
204.274181,208.186754,3.912573,د شما اگه عرضه داشتید  تا به حال حقدونو گرفته بودید,part2.wav
Total,,7.521036,,
```

## License

This project is open-source and available under the [MIT License](LICENSE).

## Contributions

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## Contact

For any inquiries or suggestions, please open an issue on the GitHub repository.
