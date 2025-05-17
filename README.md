# Axon Parselmouth Project

This project contains a set of voice analysis tools built on [Parselmouth](https://github.com/YannickJadoul/Parselmouth), a Python wrapper for Praat. It enables automated extraction of acoustic parameters from speech recordings and generates detailed textual reports for research and analysis.

## 🔍 Features

- Fundamental frequency (F0) extraction
- Intensity profile analysis
- Voice stability metrics: Jitter, Shimmer
- Harmonics-to-Noise Ratio (HNR)
- Cepstral Peak Prominence (CPP)
- Formant tracking (F1–F3)
- Speech fluency and pause analysis
- Multi-report generator with batch support

## 🚀 How to Run

```bash
./run_all_parselmouth_solutions.sh
```

Output reports are saved in the `parselmouth_reports/` directory.

## 📦 Installation

Install dependencies using:

```bash
pip install -r requirements.txt
```

## 🧪 Files Overview

- `01_...py` to `11_...py`: Modular analysis scripts
- `test_audio/`: Folder with `.wav` audio files
- `parselmouth_reports/`: Output reports in `.txt` format
- `run_all_parselmouth_solutions.sh`: Batch script to run all analyses
- `README.md`, `CHANGELOG.md`, `LICENSE`: Documentation and metadata

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
