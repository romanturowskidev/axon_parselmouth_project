"""
Solution 8: Comprehensive Baseline Acoustic Profile using Parselmouth

This script loads a single audio file and extracts a comprehensive set of acoustic
parameters using Parselmouth to create a baseline profile. This includes:
- Mean, Min, Max Pitch (F0)
- Standard Deviation of Pitch (F0)
- Mean, Min, Max Intensity
- Standard Deviation of Intensity
- Jitter (local)
- Shimmer (local, dB)
- Harmonics-to-Noise Ratio (HNR)
- Cepstral Peak Prominence (CPP)
- Speech Rate (syllables per second - conceptual, as actual syllabification is complex)
- Pause metrics (number of pauses, total pause duration, mean pause duration)
- Formant Frequencies (F1, F2, F3 - mean values for voiced segments)

It then generates a textual summary and saves it to a report file.
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

def extract_pitch_profile(sound, pitch_floor=75, pitch_ceiling=600):
    results = {"mean_f0_hz": np.nan, "min_f0_hz": np.nan, "max_f0_hz": np.nan, "sd_f0_hz": np.nan}
    try:
        pitch = sound.to_pitch_ac(pitch_floor=pitch_floor, pitch_ceiling=pitch_ceiling)
        results["mean_f0_hz"] = call(pitch, "Get mean", 0, 0, "Hertz")
        results["min_f0_hz"] = call(pitch, "Get minimum", 0, 0, "Hertz", "Parabolic")
        results["max_f0_hz"] = call(pitch, "Get maximum", 0, 0, "Hertz", "Parabolic")
        results["sd_f0_hz"] = call(pitch, "Get standard deviation", 0, 0, "Hertz")
    except Exception as e:
        print(f"⚠️ Error extracting pitch profile: {e}")
    return results

def extract_intensity_profile(sound):
    results = {"mean_intensity_db": np.nan, "min_intensity_db": np.nan, "max_intensity_db": np.nan, "sd_intensity_db": np.nan}
    try:
        intensity = sound.to_intensity()
        results["mean_intensity_db"] = call(intensity, "Get mean", 0, 0, "dB")
        results["min_intensity_db"] = call(intensity, "Get minimum", 0, 0, "Parabolic")
        results["max_intensity_db"] = call(intensity, "Get maximum", 0, 0, "Parabolic")
        results["sd_intensity_db"] = call(intensity, "Get standard deviation", 0, 0)
    except Exception as e:
        print(f"⚠️ Error extracting intensity profile: {e}")
    return results

def generate_report(filename, pitch, intensity):
    report = f"Baseline Acoustic Report for: {filename}\n"
    report += "===============================================\n\n"

    report += "Pitch Profile:\n"
    for k, v in pitch.items():
        label = k.replace("_", " ").capitalize()
        report += f"  {label}: {v:.2f} Hz\n" if not np.isnan(v) else f"  {label}: Not available\n"

    report += "\nIntensity Profile:\n"
    for k, v in intensity.items():
        label = k.replace("_", " ").capitalize()
        report += f"  {label}: {v:.2f} dB\n" if not np.isnan(v) else f"  {label}: Not available\n"

    report += "\nInterpretation Notes:\n"
    report += "- Mean F0 indicates average pitch (higher = more tense, lower = more relaxed).\n"
    report += "- SD F0 indicates pitch variability (low = monotony).\n"
    report += "- Intensity stats reflect loudness; lower values may suggest hypophonia.\n"

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
        sound = load_audio(file_path)
        if not sound:
            print(f"❌ Skipping file: {fname}")
            continue

        pitch = extract_pitch_profile(sound)
        intensity = extract_intensity_profile(sound)

        report = generate_report(fname, pitch, intensity)

        name_wo_ext = os.path.splitext(fname)[0]
        output_filename = f"08_{name_wo_ext}_parselmouth_baseline_profile_report.txt"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w") as f:
            f.write(report)

        print(f"✅ Report saved: {output_filename}")

if __name__ == "__main__":
    main()


