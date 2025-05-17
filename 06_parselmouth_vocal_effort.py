"""
Solution 6: Vocal Effort and Strain Indicator using Parselmouth

This script loads an audio file, extracts measures related to vocal effort and strain
(intensity levels, jitter, shimmer) using Parselmouth, generates a textual summary,
and saves it to a report file.
"""

import parselmouth
from parselmouth.praat import call
import numpy as np
import os

def load_audio(audio_file_path):
    try:
        return parselmouth.Sound(audio_file_path)
    except parselmouth.PraatError as e:
        print(f"❌ Error loading audio file {audio_file_path}: {e}")
        return None

def extract_intensity_levels(sound):
    try:
        intensity = sound.to_intensity()
        mean_intensity_db = call(intensity, "Get mean", 0, 0)
        max_intensity_db = call(intensity, "Get maximum", 0, 0, "Parabolic")
        return {
            "mean_intensity_db": mean_intensity_db if mean_intensity_db is not None else np.nan,
            "max_intensity_db": max_intensity_db if max_intensity_db is not None else np.nan
        }
    except parselmouth.PraatError as e:
        print(f"❌ Error extracting intensity levels: {e}")
        return {"mean_intensity_db": np.nan, "max_intensity_db": np.nan}

def extract_jitter_shimmer_for_effort(sound, pitch_floor=75, pitch_ceiling=600):
    try:
        point_process = call(sound, "To PointProcess (periodic, cc)", pitch_floor, pitch_ceiling)

        if point_process is None:
            raise ValueError("Generated PointProcess is None")

        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)

        # Spróbuj shimmer tylko jeśli point_process wygląda poprawnie
        shimmer = np.nan
        try:
            shimmer = call([sound, point_process], "Get shimmer (local dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        except Exception as inner_e:
            print(f"⚠️ Could not extract shimmer: {inner_e}")

        return {
            "jitter_local": jitter if jitter is not None else np.nan,
            "shimmer_local_db": shimmer if shimmer is not None else np.nan
        }

    except parselmouth.PraatError as e:
        print(f"❌ Error extracting jitter/shimmer: {e}")
        return {
            "jitter_local": np.nan,
            "shimmer_local_db": np.nan
        }
    except Exception as e:
        print(f"❌ Unexpected error during jitter/shimmer extraction: {e}")
        return {
            "jitter_local": np.nan,
            "shimmer_local_db": np.nan
        }


def generate_vocal_effort_report(intensity_data, jitter_shimmer_data, audio_file_name):
    report = f"Vocal Effort and Strain Indicator Report for: {audio_file_name}\n"
    report += "=============================================================\n\n"

    report += "Intensity Levels (Effort Indicators):\n"
    report += f"  Mean Intensity: {intensity_data['mean_intensity_db']:.2f} dB\n" if not np.isnan(intensity_data['mean_intensity_db']) else "  Mean Intensity: Not available\n"
    report += f"  Maximum Intensity: {intensity_data['max_intensity_db']:.2f} dB\n" if not np.isnan(intensity_data['max_intensity_db']) else "  Maximum Intensity: Not available\n"
    report += "  Interpretation Guide: High values → vocal effort, low values → fatigue or quiet speech.\n\n"

    report += "Vocal Stability (Strain Indicators - Jitter & Shimmer):\n"
    if not np.isnan(jitter_shimmer_data['jitter_local']):
        jitter_display = f"{jitter_shimmer_data['jitter_local'] * 100:.2f}%" if jitter_shimmer_data['jitter_local'] < 0.1 else f"{jitter_shimmer_data['jitter_local']:.4f}"
        report += f"  Jitter (local): {jitter_display}\n"
    else:
        report += "  Jitter (local): Not available\n"

    report += f"  Shimmer (local, dB): {jitter_shimmer_data['shimmer_local_db']:.2f} dB\n" if not np.isnan(jitter_shimmer_data['shimmer_local_db']) else "  Shimmer (local, dB): Not available\n"
    report += "  Interpretation Guide: High values may suggest strain or instability.\n\n"

    report += "Combined Interpretation:\n"
    report += "  - High intensity + high jitter/shimmer → possible vocal strain.\n"
    report += "  - Low intensity + high jitter/shimmer → weak/unstable voice.\n"
    report += "  - Use for monitoring fatigue or effort over time.\n\n"

    report += "General Notes:\n"
    report += "- Acoustic parameters are sensitive to recording conditions.\n"
    report += "- Interpret results in clinical or task context.\n"

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
            intensity_data = extract_intensity_levels(sound)
            jitter_shimmer_data = extract_jitter_shimmer_for_effort(sound)
            report_content = generate_vocal_effort_report(intensity_data, jitter_shimmer_data, filename)

            filename_wo_ext = os.path.splitext(filename)[0]
            report_filename = f"06_{filename_wo_ext}_parselmouth_vocal_effort_report.txt"
            report_path = os.path.join(output_dir, report_filename)

            with open(report_path, "w") as f:
                f.write(report_content)

            print(f"✅ Report saved: {report_filename}")
        else:
            print(f"❌ Failed to process file: {filename}")

if __name__ == "__main__":
    main()



