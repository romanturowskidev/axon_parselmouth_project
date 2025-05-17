# Parselmouth Voice Analysis

This project is based on the [Praat-Parselmouth](https://github.com/YannickJadoul/Parselmouth) library and enables automatic analysis of voice features and generation of detailed text-based acoustic reports.

## 🔍 What does this project do?

- Generates a synthetic test audio file or analyzes provided `.wav` files
- Extracts core acoustic features:
  - Pitch (F0)
  - Intensity (loudness)
  - Jitter and Shimmer (voice stability)
  - HNR (Harmonics-to-Noise Ratio)
  - Formants (F1–F3)
- Creates a `.txt` report with interpretation guidelines

## Requirements

- Python 3.8+
- Parselmouth
- NumPy
- SciPy (used for generating synthetic audio)

## Install dependencies:

`pip install praat-parselmouth numpy scipy`


## How to run?

`./run_all_parselmouth_solutions.sh`

The generated report will be saved in the `parselmouth_reports` directory.


## Disclaimer

This project does not provide a medical diagnosis. Acoustic feature values should be interpreted carefully and in the appropriate clinical or research context.


## License

AXON DAO
