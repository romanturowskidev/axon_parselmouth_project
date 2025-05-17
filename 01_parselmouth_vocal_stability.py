"""
Solution 1: Vocal Stability Assessment using Parselmouth

This script loads an audio file, extracts Jitter, Shimmer, and Harmonics-to-Noise Ratio (HNR)
using the Parselmouth library (interfacing with Praat), generates a textual summary,
and saves the summary to a report file.
"""

import parselmouth
from parselmouth.praat import call
import numpy as np
import os

def load_audio(audio_file_path):
    try:
        sound = parselmouth.Sound(audio_file_path)
        return sound
    except parselmouth.PraatError as e:
        print(f"Error loading audio file {audio_file_path}: {e}")
        return None

def extract_hnr(sound):
    try:
        harmonicity = sound.to_harmonicity_cc()
        hnr = call(harmonicity, "Get mean", 0, 0)
        return hnr if hnr is not None else np.nan
    except parselmouth.PraatError as e:
        print(f"Error extracting HNR: {e}")
        return np.nan


def extract_jitter_shimmer(sound):
    jitter_value_local = np.nan
    shimmer_value_local_db = np.nan

    try:
        jitter_value_local = call(sound, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        shimmer_value_local_db = call(sound, "Get shimmer (local dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    except parselmouth.PraatError as e:
        print(f"⚠️ Error extracting jitter/shimmer: {e}")

    return {
        "jitter_local": jitter_value_local if jitter_value_local is not None else np.nan,
        "shimmer_local_db": shimmer_value_local_db if shimmer_value_local_db is not None else np.nan
    }
    

def generate_stability_report(hnr, jitter_shimmer_data, audio_file_name):
    report = f"Vocal Stability Assessment Report for: {audio_file_name}\n"
    report += "-----------------------------------------------------\n\n"

    report += "Harmonics-to-Noise Ratio (HNR):\n"
    if not np.isnan(hnr):
        report += f"  Mean HNR: {hnr:.2f} dB\n"
        report += "  Interpretation Guide: Higher HNR values generally indicate a clearer, more harmonic voice quality. Lower values can suggest breathiness or hoarseness.\n\n"
    else:
        report += "  Mean HNR: Not available\n\n"

    report += "Jitter (Frequency Perturbation):\n"
    if not np.isnan(jitter_shimmer_data["jitter_local"]):
        jitter_display = f"{jitter_shimmer_data['jitter_local'] * 100:.2f}%" if jitter_shimmer_data["jitter_local"] < 0.1 else f"{jitter_shimmer_data['jitter_local']:.4f}"
        report += f"  Jitter (local): {jitter_display}\n"
        report += "  Interpretation Guide: Higher jitter values can indicate vocal instability or roughness. Values below 1–1.5% are often considered normal.\n\n"
    else:
        report += "  Jitter (local): Not available\n\n"

    report += "Shimmer (Amplitude Perturbation):\n"
    if not np.isnan(jitter_shimmer_data["shimmer_local_db"]):
        report += f"  Shimmer (local, dB): {jitter_shimmer_data['shimmer_local_db']:.2f} dB\n"
        report += "  Interpretation Guide: Higher shimmer values can indicate amplitude instability. Values below 0.5 dB are often considered normal.\n\n"
    else:
        report += "  Shimmer (local, dB): Not available\n\n"

    report += "General Notes:\n"
    report += "- These are research indicators, not medical diagnoses.\n"
    report += "- Recording conditions and equipment affect results.\n"
    return report

def main():
    input_dir = "test_audio"
    output_dir = "parselmouth_reports"
    os.makedirs(output_dir, exist_ok=True)

    audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".wav")]
    if not audio_files:
        print("No .wav files found in test_audio folder.")
        return

    for filename in audio_files:
        input_path = os.path.join(input_dir, filename)
        sound = load_audio(input_path)
        if sound:
            hnr_value = extract_hnr(sound)
            jitter_shimmer_data = extract_jitter_shimmer(sound)
            report_content = generate_stability_report(hnr_value, jitter_shimmer_data, filename)

            base_name = os.path.splitext(filename)[0]
            report_filename = f"01_{base_name}_parselmouth_vocal_stability_report.txt"
            report_path = os.path.join(output_dir, report_filename)

            with open(report_path, "w") as f:
                f.write(report_content)

            print(f"✅ Report saved: {report_path}")
        else:
            print(f"❌ Failed to process: {filename}")

if __name__ == "__main__":
    main()
