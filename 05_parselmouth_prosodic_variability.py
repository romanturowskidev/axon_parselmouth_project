"""
Solution 5: Prosodic Variability Analysis using Parselmouth

This script loads an audio file, extracts measures of pitch (F0) and intensity variability
(standard deviations) using Parselmouth, discusses conceptual analysis of contours,
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
        print(f"❌ Error loading audio file {audio_file_path}: {e}")
        return None

def extract_intensity_variability(sound):
    try:
        intensity = sound.to_intensity()
        sd_intensity_db = parselmouth.praat.call(intensity, "Get standard deviation", 0, 0)
        return sd_intensity_db if sd_intensity_db is not None else np.nan
    except parselmouth.PraatError as e:
        print(f"❌ Error extracting intensity variability: {e}")
        return np.nan

def extract_pitch_variability(sound, pitch_floor=75, pitch_ceiling=600):
    try:
        pitch = sound.to_pitch_ac(pitch_floor=pitch_floor, pitch_ceiling=pitch_ceiling)
        sd_f0_hz = parselmouth.praat.call(pitch, "Get standard deviation", 0, 0, "Hertz")
        return sd_f0_hz if sd_f0_hz is not None else np.nan
    except parselmouth.PraatError as e:
        print(f"❌ Error extracting pitch variability: {e}. This might be an unvoiced segment.")
        return np.nan

def generate_prosodic_variability_report(sd_f0, sd_intensity, audio_file_name):
    report = f"Prosodic Variability Analysis Report for: {audio_file_name}\n"
    report += "--------------------------------------------------------\n\n"

    report += "Pitch Variability (F0 Standard Deviation):\n"
    if not np.isnan(sd_f0):
        report += f"  Standard Deviation of Pitch (F0): {sd_f0:.2f} Hz\n"
        report += "  Interpretation Guide: Higher values indicate more pitch modulation (dynamic intonation), while lower values suggest a more monotonous pitch (monopitch).\n\n"
    else:
        report += "  Standard Deviation of Pitch (F0): Not available\n\n"

    report += "Intensity Variability (Loudness Standard Deviation):\n"
    if not np.isnan(sd_intensity):
        report += f"  Standard Deviation of Intensity: {sd_intensity:.2f} dB\n"
        report += "  Interpretation Guide: Higher values indicate more dynamic use of loudness, while lower values suggest monoloudness.\n\n"
    else:
        report += "  Standard Deviation of Intensity: Not available\n\n"

    report += "Conceptual Analysis of Pitch and Intensity Contours:\n"
    report += "  Advanced analysis would involve examining the actual contours (patterns of rise and fall) of pitch and intensity over time.\n"
    report += "  Techniques might include:\n"
    report += "    - Identifying pitch inflections\n"
    report += "    - Analyzing shape of intonational phrases\n"
    report += "    - Correlating with linguistic units\n\n"

    report += "General Notes:\n"
    report += "- These are acoustic measurements, not a medical diagnosis.\n"
    report += "- Interpretation should be done by a qualified professional.\n"
    report += "- Contour analysis provides more detail than global statistics.\n"

    return report

def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_dir = os.path.join(base_dir, "test_audio")
        output_dir = os.path.join(base_dir, "parselmouth_reports")
        os.makedirs(output_dir, exist_ok=True)

        audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".wav")]
        if not audio_files:
            print("No audio files found in test_audio folder.")
            sys.exit(1)

        for filename in audio_files:
            file_path = os.path.join(input_dir, filename)
            sound = load_audio(file_path)

            if sound:
                sd_intensity = extract_intensity_variability(sound)
                sd_f0 = extract_pitch_variability(sound)
                report_content = generate_prosodic_variability_report(sd_f0, sd_intensity, filename)

                identifier_uuid = str(uuid.uuid4())
                algorithm_number = "05"
                algorithm_name = "parselmouth_prosodic_variability"
                report_filename = f"{algorithm_number}_{identifier_uuid}_{algorithm_name}.txt"
                report_path = os.path.join(output_dir, report_filename)

                with open(report_path, "w") as f:
                    f.write(report_content)

                print(f"✅ Report saved: {report_path}")
            else:
                print(f"❌ Failed to process file: {filename}")
                sys.exit(1)

        sys.exit(0)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

