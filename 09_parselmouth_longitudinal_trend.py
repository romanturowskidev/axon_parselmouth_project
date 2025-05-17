"""
Solution 9: Longitudinal Trend Identification using Parselmouth (Conceptual)

This script outlines the conceptual approach for identifying longitudinal trends
in acoustic parameters extracted using Parselmouth. It assumes that data from
multiple recordings over time for a single participant has been collected and
 key parameters (e.g., mean F0, mean intensity, HNR, jitter, shimmer) have been
 extracted for each recording (similar to the Baseline Profile script).

The script will:
1. Simulate a dataset of such longitudinal acoustic data.
2. Demonstrate a simple trend analysis (e.g., by observing changes or fitting a simple linear trend).
3. Generate a textual summary of potential trends.
4. Save the summary to a report file.

Note: Actual trend analysis can be much more sophisticated, involving statistical
 tests, time series analysis, and more robust regression models. This is a simplified
 illustration.
"""

import parselmouth
from parselmouth.praat import call
import numpy as np
import os
from datetime import datetime

def extract_features(sound, filename):
    warnings = []

    def safe_call(func, description):
        try:
            return func()
        except Exception as e:
            warnings.append(f"Could not extract {description} – {e}")
            return np.nan

    f0_mean = safe_call(lambda: np.nanmean(sound.to_pitch().selected_array['frequency'][sound.to_pitch().selected_array['frequency'] > 0]), "Mean F0")
    intensity_mean = safe_call(lambda: np.nanmean(sound.to_intensity().values[0]), "Mean Intensity")
    hnr_mean = safe_call(lambda: np.nanmean(sound.to_harmonicity().values[0]), "HNR")

    point_process = safe_call(lambda: call(sound, "To PointProcess (periodic, cc)", 75, 500), "PointProcess")
    jitter_local = safe_call(lambda: call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3), "Jitter")
    shimmer_local = safe_call(lambda: call(sound, "Get shimmer (local dB)", point_process, 0, 0, 0.0001, 0.02, 1.3, 1.6), "Shimmer")

    return {
        "mean_f0_hz": f0_mean,
        "mean_intensity_db": intensity_mean,
        "hnr_db": hnr_mean,
        "jitter_local": jitter_local,
        "shimmer_local_db": shimmer_local,
        "warnings": warnings
    }

def generate_single_file_report(audio_filename, features):
    report = f"Parselmouth Longitudinal Trend Report for: {audio_filename}\n"
    report += "============================================================\n\n"

    def format_value(label, value, unit):
        return f"{label}: {value:.2f} {unit}\n" if not np.isnan(value) else f"{label}: Not available\n"

    report += format_value("Mean F0", features["mean_f0_hz"], "Hz")
    report += format_value("Mean Intensity", features["mean_intensity_db"], "dB")
    report += format_value("HNR", features["hnr_db"], "dB")
    report += format_value("Jitter (local)", features["jitter_local"], "")
    report += format_value("Shimmer (local, dB)", features["shimmer_local_db"], "dB")

    if features["warnings"]:
        report += "\nWarnings:\n"
        report += "---------\n"
        for w in features["warnings"]:
            report += f"- {w}\n"

    report += "\nInterpretation Notes:\n"
    report += "- ↑ F0 = higher pitch (stress, tension); ↓ F0 = fatigue or depression\n"
    report += "- ↑ Jitter/Shimmer = vocal instability (neurological or phonatory disorders)\n"
    report += "- ↓ HNR = breathy/hoarse voice; ↑ HNR = clearer phonation\n"

    return report

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "test_audio")
    output_dir = os.path.join(base_dir, "parselmouth_reports")
    os.makedirs(output_dir, exist_ok=True)

    audio_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".wav")])

    if not audio_files:
        print("❌ No .wav files found in test_audio.")
        return

    for fname in audio_files:
        file_path = os.path.join(input_dir, fname)
        sound = parselmouth.Sound(file_path)
        features = extract_features(sound, fname)
        report = generate_single_file_report(fname, features)

        # Nazwa pliku: 09_nazwa_bez_wav_parselmouth_longitudinal_trend_report.txt
        name_wo_ext = os.path.splitext(fname)[0]
        output_filename = f"09_{name_wo_ext}_parselmouth_longitudinal_trend_report.txt"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w") as f:
            f.write(report)

        print(f"✅ Report saved: {output_filename}")

if __name__ == "__main__":
    main()



