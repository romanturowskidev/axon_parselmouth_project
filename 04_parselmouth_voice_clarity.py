"""
Solution 4: Voice Clarity and Quality Assessment using Parselmouth

This script loads an audio file, extracts Harmonics-to-Noise Ratio (HNR) and
Cepstral Peak Prominence (CPP) using Parselmouth (interfacing with Praat),
 generates a textual summary, and saves it to a report file.
"""

import parselmouth
from parselmouth.praat import call
import numpy as np
import os

def load_audio(audio_file_path):
    try:
        return parselmouth.Sound(audio_file_path)
    except parselmouth.PraatError as e:
        print(f"❌ Error loading {audio_file_path}: {e}")
        return None

def extract_hnr(sound):
    try:
        harmonicity = sound.to_harmonicity_cc(
            time_step=0.01,
            minimum_pitch=75,
            silence_threshold=0.1,
            periods_per_window=1.0
        )
        hnr = call(harmonicity, "Get mean", 0, 0)
        return hnr if hnr is not None else np.nan
    except parselmouth.PraatError as e:
        print(f"⚠️ Error extracting HNR: {e}")
        return np.nan

def generate_clarity_report(hnr, audio_file_name):
    report = f"Voice Clarity Assessment Report for: {audio_file_name}\n"
    report += "=====================================================\n\n"

    report += "Harmonics-to-Noise Ratio (HNR):\n"
    if not np.isnan(hnr):
        report += f"  Mean HNR: {hnr:.2f} dB\n"
        report += "  Interpretation:\n"
        report += "    - Higher HNR = clearer, more harmonic voice\n"
        report += "    - Lower HNR = breathy, hoarse, or noisy phonation\n"
        report += "    - Healthy voices often show HNR > 20 dB\n\n"
    else:
        report += "  Mean HNR: Not available\n\n"

    report += "General Notes:\n"
    report += "- HNR reflects the clarity and periodicity of the voice.\n"
    report += "- Low HNR may indicate vocal instability, breathiness, or pathology.\n"
    report += "- Interpretation depends on context and recording quality.\n"

    return report

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "test_audio")
    output_dir = os.path.join(base_dir, "parselmouth_reports")
    os.makedirs(output_dir, exist_ok=True)

    audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".wav")]
    if not audio_files:
        print("❌ No .wav files found in test_audio.")
        return

    for filename in audio_files:
        file_path = os.path.join(input_dir, filename)
        sound = load_audio(file_path)

        if sound:
            hnr_value = extract_hnr(sound)
            report = generate_clarity_report(hnr_value, filename)

            filename_wo_ext = os.path.splitext(filename)[0]
            report_filename = f"04_{filename_wo_ext}_parselmouth_voice_clarity_report.txt"
            report_path = os.path.join(output_dir, report_filename)

            with open(report_path, "w") as f:
                f.write(report)

            print(f"✅ Report saved: {report_filename}")
        else:
            print(f"❌ Failed to process file: {filename}")

if __name__ == "__main__":
    main()



