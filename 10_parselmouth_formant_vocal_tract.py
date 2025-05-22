"""
Solution 10: Formant and Vocal Tract Summary using Parselmouth

This script loads an audio file, extracts mean formant frequencies (F1, F2, F3)
for voiced segments using Parselmouth and generates a textual summary.
"""

import parselmouth
from parselmouth.praat import call
import numpy as np
import os
import sys
import uuid

def load_audio(audio_file_path):
    try:
        return parselmouth.Sound(audio_file_path)
    except parselmouth.PraatError as e:
        print(f"Error loading audio file {audio_file_path}: {e}")
        return None

def extract_mean_formants_voiced(sound, time_step=0.01, max_num_formants=5, max_formant_freq=5500,
                                 window_length=0.025, pre_emphasis_from=50,
                                 pitch_floor=75, pitch_ceiling=600):
    results = {"mean_f1_hz": np.nan, "mean_f2_hz": np.nan, "mean_f3_hz": np.nan}
    try:
        formant = sound.to_formant_burg(time_step, max_num_formants, max_formant_freq, window_length, pre_emphasis_from)
        pitch = sound.to_pitch_ac(pitch_floor=pitch_floor, pitch_ceiling=pitch_ceiling)

        f1_values, f2_values, f3_values = [], [], []

        for t in formant.ts():
            pitch_val = call(pitch, "Get value at time", t, "Hertz", "Linear")
            if pitch_val and pitch_val > 0:
                f1 = call(formant, "Get value at time", 1, t, "Hertz", "Linear")
                f2 = call(formant, "Get value at time", 2, t, "Hertz", "Linear")
                f3 = call(formant, "Get value at time", 3, t, "Hertz", "Linear")
                if not np.isnan(f1): f1_values.append(f1)
                if not np.isnan(f2): f2_values.append(f2)
                if not np.isnan(f3): f3_values.append(f3)

        if f1_values: results["mean_f1_hz"] = np.mean(f1_values)
        if f2_values: results["mean_f2_hz"] = np.mean(f2_values)
        if f3_values: results["mean_f3_hz"] = np.mean(f3_values)

    except parselmouth.PraatError as e:
        print(f"Error extracting mean formants: {e}")
    except Exception as e:
        print(f"A general error occurred during mean formant extraction: {e}")
    return results

def generate_formant_report(data, filename):
    report = f"Formant and Vocal Tract Summary Report for: {filename}\n"
    report += "--------------------------------------------------------------\n\n"
    report += "Mean Formant Frequencies (Voiced Segments):\n"
    report += f"  - Mean F1: {data['mean_f1_hz']:.0f} Hz\n" if not np.isnan(data["mean_f1_hz"]) else "  - Mean F1: Not available\n"
    report += f"  - Mean F2: {data['mean_f2_hz']:.0f} Hz\n" if not np.isnan(data["mean_f2_hz"]) else "  - Mean F2: Not available\n"
    report += f"  - Mean F3: {data['mean_f3_hz']:.0f} Hz\n\n" if not np.isnan(data["mean_f3_hz"]) else "  - Mean F3: Not available\n\n"

    report += "Interpretation Guide:\n"
    report += "- F1 ~ tongue height (↓ F1 = ↑ tongue height)\n"
    report += "- F2 ~ tongue backness (↑ F2 = front vowels)\n"
    report += "- Changes may indicate articulatory imprecision or pathology (e.g. dysarthria).\n\n"

    report += "Conceptual Vocal Tract Metrics:\n"
    report += "  1. Vowel Space Area (VSA):\n"
    report += "     Requires vowel labeling (e.g., /i/, /a/, /u/) and F1/F2 extraction.\n"
    report += "  2. Formant Centralization Ratio (FCR):\n"
    report += "     Calculated from point vowels. Higher FCR may indicate centralization.\n\n"

    report += "General Notes:\n"
    report += "- Mean values summarize full voiced portions, not individual vowels.\n"
    report += "- For VSA/FCR, phonetic annotation (e.g., TextGrid) is needed.\n"
    return report

def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_dir = os.path.join(base_dir, "test_audio")
        output_dir = os.path.join(base_dir, "parselmouth_reports")
        os.makedirs(output_dir, exist_ok=True)

        audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".wav")]
        if not audio_files:
            print("❌ No .wav files found in test_audio.")
            sys.exit(1)

        for filename in audio_files:
            file_path = os.path.join(input_dir, filename)
            print(f"\n🎧 Analyzing: {filename}")
            sound = load_audio(file_path)

            if sound:
                formant_data = extract_mean_formants_voiced(sound)
                report = generate_formant_report(formant_data, filename)

                identifier_uuid = str(uuid.uuid4())
                algorithm_number = "10"
                algorithm_name = "parselmouth_formant_vocal_tract"
                report_filename = f"{algorithm_number}_{identifier_uuid}_{algorithm_name}.txt"
                report_path = os.path.join(output_dir, report_filename)

                with open(report_path, "w") as f:
                    f.write(report)

                print(f"✅ Report saved: {report_filename}")
            else:
                print(f"❌ Failed to process file: {filename}")
                sys.exit(1)

        sys.exit(0)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
