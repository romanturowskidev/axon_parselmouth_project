"""
Solution 9: Longitudinal Trend Identification using Parselmouth (Conceptual)

This script loads audio files, extracts acoustic features,
and generates a simplified longitudinal trend report.
"""

import parselmouth
from parselmouth.praat import call
import numpy as np
import os
import sys
import uuid

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
    report += format_value("Shimmer (local)", features["shimmer_local_db"], "dB")

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
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_dir = os.path.join(base_dir, "test_audio")
        output_dir = os.path.join(base_dir, "parselmouth_reports")
        os.makedirs(output_dir, exist_ok=True)

        audio_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".wav")])

        if not audio_files:
            print("❌ No .wav files found in test_audio.")
            sys.exit(1)

        for fname in audio_files:
            file_path = os.path.join(input_dir, fname)
            try:
                sound = parselmouth.Sound(file_path)
            except Exception as e:
                print(f"❌ Skipping file {fname}: {e}")
                sys.exit(1)

            features = extract_features(sound, fname)
            report = generate_single_file_report(fname, features)

            identifier_uuid = str(uuid.uuid4())
            algorithm_number = "09"
            algorithm_name = "parselmouth_longitudinal_trend"
            output_filename = f"{algorithm_number}_{identifier_uuid}_{algorithm_name}.txt"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "w") as f:
                f.write(report)

            print(f"✅ Report saved: {output_filename}")

        sys.exit(0)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

