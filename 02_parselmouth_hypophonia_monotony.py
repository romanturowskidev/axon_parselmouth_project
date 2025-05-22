"""
Solution 2: Hypophonia and Monotony Analysis using Parselmouth

This script loads an audio file, extracts measures related to vocal intensity (hypophonia)
and pitch/intensity variability (monotony) using the Parselmouth library,
generates a textual summary, and saves it to a report file.
"""

import parselmouth
import numpy as np
import os
import sys
import uuid

def load_audio(audio_file_path):
    try:
        sound = parselmouth.Sound(audio_file_path)
        return sound
    except parselmouth.PraatError as e:
        print(f"Error loading audio file {audio_file_path}: {e}")
        return None

def extract_intensity_features(sound):
    try:
        intensity = sound.to_intensity()
        mean_intensity = parselmouth.praat.call(intensity, "Get mean", 0, 0, "dB")
        sd_intensity = parselmouth.praat.call(intensity, "Get standard deviation", 0, 0)
        return {
            "mean_intensity_db": mean_intensity if mean_intensity is not None else np.nan,
            "sd_intensity_db": sd_intensity if sd_intensity is not None else np.nan
        }
    except parselmouth.PraatError as e:
        print(f"Error extracting intensity features: {e}")
        return {"mean_intensity_db": np.nan, "sd_intensity_db": np.nan}

def extract_pitch_features(sound, pitch_floor=75, pitch_ceiling=600):
    try:
        pitch = sound.to_pitch_ac(pitch_floor=pitch_floor, pitch_ceiling=pitch_ceiling)
        mean_f0_hz = parselmouth.praat.call(pitch, "Get mean", 0, 0, "Hertz")
        sd_f0_hz = parselmouth.praat.call(pitch, "Get standard deviation", 0, 0, "Hertz")
        return {
            "mean_f0_hz": mean_f0_hz if mean_f0_hz is not None else np.nan,
            "sd_f0_hz": sd_f0_hz if sd_f0_hz is not None else np.nan
        }
    except parselmouth.PraatError as e:
        print(f"Error extracting pitch features: {e}")
        return {"mean_f0_hz": np.nan, "sd_f0_hz": np.nan}

def generate_hypophonia_monotony_report(intensity_data, pitch_data, audio_file_name):
    report = f"Hypophonia and Monotony Analysis Report for: {audio_file_name}\n"
    report += "-----------------------------------------------------------\n\n"

    report += "Intensity Analysis (Hypophonia Indicators):\n"
    if not np.isnan(intensity_data["mean_intensity_db"]):
        report += f"  Mean Intensity: {intensity_data['mean_intensity_db']:.2f} dB\n"
        report += "  Interpretation Guide (Hypophonia): Lower mean intensity values can suggest hypophonia.\n\n"
    else:
        report += "  Mean Intensity: Not available\n\n"

    report += "Pitch and Intensity Variability (Monotony Indicators):\n"
    if not np.isnan(pitch_data["sd_f0_hz"]):
        report += f"  Standard Deviation of Pitch (F0): {pitch_data['sd_f0_hz']:.2f} Hz\n"
        report += "  Lower SD of F0 = less pitch variation = possible monotony.\n\n"
    else:
        report += "  Standard Deviation of Pitch (F0): Not available\n\n"

    if not np.isnan(intensity_data["sd_intensity_db"]):
        report += f"  Standard Deviation of Intensity: {intensity_data['sd_intensity_db']:.2f} dB\n"
        report += "  Lower SD of intensity = possible loudness monotony.\n\n"
    else:
        report += "  Standard Deviation of Intensity: Not available\n\n"

    report += "Additional Pitch Info:\n"
    if not np.isnan(pitch_data["mean_f0_hz"]):
        report += f"  Mean Pitch (F0): {pitch_data['mean_f0_hz']:.2f} Hz\n\n"
    else:
        report += "  Mean Pitch (F0): Not available\n\n"

    report += (
        "General Notes:\n"
        "- Acoustic values only; not a diagnosis.\n"
        "- Consider recording quality and context.\n"
    )
    return report

def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_dir = os.path.join(base_dir, "test_audio")
        output_dir = os.path.join(base_dir, "parselmouth_reports")
        os.makedirs(output_dir, exist_ok=True)

        wav_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".wav")]

        if not wav_files:
            print(f"No .wav files found in {input_dir}")
            sys.exit(1)

        for filename in wav_files:
            audio_path = os.path.join(input_dir, filename)
            sound = load_audio(audio_path)

            if sound:
                intensity = extract_intensity_features(sound)
                pitch = extract_pitch_features(sound)
                report = generate_hypophonia_monotony_report(intensity, pitch, filename)

                identifier_uuid = str(uuid.uuid4())
                algorithm_number = "02"
                algorithm_name = "parselmouth_hypophonia_monotony"
                output_filename = f"{algorithm_number}_{identifier_uuid}_{algorithm_name}.txt"
                output_path = os.path.join(output_dir, output_filename)

                with open(output_path, "w") as f:
                    f.write(report)

                print(f"✅ Report saved: {output_path}")
            else:
                print(f"❌ Skipped (cannot process): {filename}")
                sys.exit(1)

        sys.exit(0)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

