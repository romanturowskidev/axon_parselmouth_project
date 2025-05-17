"""
Solution 7: Fundamental Vocal Parameter Shift Analysis using Parselmouth

This script loads two audio files (representing different time points or conditions),
 extracts key acoustic parameters (mean F0, mean intensity, HNR, jitter, shimmer)
 from both using Parselmouth, compares these parameters, generates a textual summary
 of the shifts, and saves it to a report file.
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

def extract_mean_f0(sound, pitch_floor=75, pitch_ceiling=600):
    try:
        pitch = sound.to_pitch_ac(pitch_floor=pitch_floor, pitch_ceiling=pitch_ceiling)
        return call(pitch, "Get mean", 0, 0, "Hertz")
    except: return np.nan

def extract_mean_intensity(sound):
    try:
        intensity = sound.to_intensity()
        return call(intensity, "Get mean", 0, 0, "dB")
    except: return np.nan

def extract_hnr(sound):
    try:
        harmonicity = sound.to_harmonicity_cc()
        return call(harmonicity, "Get mean", 0, 0)
    except: return np.nan

def extract_jitter_shimmer(sound, pitch_floor=75, pitch_ceiling=600):
    jitter, shimmer = np.nan, np.nan
    try:
        point_process = call(sound, "To PointProcess (periodic, cc)", pitch_floor, pitch_ceiling)
        report = call(point_process, "Get report", 0, 0, 0.0001, 0.02, 0.01, 0.0001, 0.02, 0.01, 0.02, 0.4)
        for line in report.split("\n"):
            if "Jitter (local):" in line:
                try: jitter = float(line.split(":")[1].strip().split(" ")[0])
                except: pass
            elif "Shimmer (local, dB):" in line:
                try: shimmer = float(line.split(":")[1].strip().split(" ")[0])
                except: pass
    except: pass
    return {"jitter_local": jitter, "shimmer_local_db": shimmer}

def analyze_recording(sound):
    if not sound:
        return {k: np.nan for k in ["mean_f0_hz", "mean_intensity_db", "hnr_db", "jitter_local", "shimmer_local_db"]}
    return {
        "mean_f0_hz": extract_mean_f0(sound),
        "mean_intensity_db": extract_mean_intensity(sound),
        "hnr_db": extract_hnr(sound),
        **extract_jitter_shimmer(sound)
    }

def generate_report(params, file_name):
    report = f"Fundamental Vocal Parameter Profile Report\n"
    report += f"For recording: {file_name}\n"
    report += "----------------------------------------------------------\n\n"

    def format_line(name, value, unit=""):
        return f"{name}: {value:.2f} {unit}\n" if not np.isnan(value) else f"{name}: Not available\n"

    report += format_line("Mean Pitch (F0)", params["mean_f0_hz"], "Hz")
    report += format_line("Mean Intensity", params["mean_intensity_db"], "dB")
    report += format_line("HNR", params["hnr_db"], "dB")

    jitter = params["jitter_local"]
    shimmer = params["shimmer_local_db"]
    if not np.isnan(jitter):
        jitter_str = f"{jitter*100:.2f}%" if jitter < 0.1 else f"{jitter:.4f}"
        report += f"Jitter (local): {jitter_str}\n"
    else:
        report += "Jitter (local): Not available\n"

    report += format_line("Shimmer (local, dB)", shimmer, "dB")

    report += "\nInterpretation Notes:\n"
    report += "- ↑ F0 = higher pitch (stress, arousal); ↓ F0 = fatigue or low tone.\n"
    report += "- ↑ Jitter/Shimmer = unstable phonation; ↓ = stable voice.\n"
    report += "- ↓ HNR = breathy or hoarse; ↑ = clear and steady voice.\n"
    report += "- Results depend on task, microphone, and health status.\n"

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

    for file in audio_files:
        path = os.path.join(input_dir, file)
        sound = load_audio(path)
        if not sound:
            print(f"❌ Skipping file: {file}")
            continue

        params = analyze_recording(sound)
        report = generate_report(params, file)

        filename_base = os.path.splitext(file)[0]
        output_file = f"07_{filename_base}_parselmouth_parameter_profile.txt"
        output_path = os.path.join(output_dir, output_file)

        with open(output_path, "w") as f:
            f.write(report)

        print(f"✅ Report saved: {output_file}")

if __name__ == "__main__":
    main()


