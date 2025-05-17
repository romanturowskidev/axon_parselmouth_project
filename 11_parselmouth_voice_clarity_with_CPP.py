# Same as "04_parselmouth_voice_clarity" script, byt with added CPP parametr:

import os
import numpy as np
import scipy.signal
import soundfile as sf
import parselmouth
from parselmouth.praat import call

def calculate_cpp_simple(audio_path):
    try:
        y, sr = sf.read(audio_path)
        if y.ndim > 1:
            y = y.mean(axis=1)  # mono

        y_preemph = scipy.signal.lfilter([1, -0.97], 1, y)
        spectrum = np.fft.fft(y_preemph)
        log_power_spectrum = np.log(np.abs(spectrum) ** 2 + 1e-12)
        cepstrum = np.abs(np.fft.ifft(log_power_spectrum))

        lower = int(0.002 * sr)
        upper = int(0.02 * sr)
        cpp = np.max(cepstrum[lower:upper])
        return round(cpp, 3)
    except Exception as e:
        print(f"⚠️ Error calculating CPP: {e}")
        return np.nan

def extract_hnr(sound):
    try:
        harmonicity = sound.to_harmonicity_cc()
        return call(harmonicity, "Get mean", 0, 0)
    except:
        return np.nan

def load_audio(audio_file_path):
    try:
        return parselmouth.Sound(audio_file_path)
    except:
        return None

def generate_clarity_quality_report(hnr, cpp, audio_file_name):
    report = f"Voice Clarity and Quality Assessment Report for: {audio_file_name}\n"
    report += "-----------------------------------------------------------\n\n"

    report += f"Harmonics-to-Noise Ratio (HNR):\n"
    if not np.isnan(hnr):
        report += f"  Mean HNR: {hnr:.2f} dB\n"
    else:
        report += "  Mean HNR: Not available\n"

    report += f"\nApproximate Cepstral Peak Prominence (CPP):\n"
    if not np.isnan(cpp):
        report += f"  CPP (approx.): {cpp:.2f} (a.u.)\n"
    else:
        report += "  CPP: Not available\n"

    report += "\nGeneral Notes:\n"
    report += "- HNR calculated via Parselmouth (Praat interface).\n"
    report += "- CPP estimated directly in Python (no Praat required).\n"
    report += "- Values depend on signal quality and are not medical diagnoses.\n"
    return report

def main():
    input_dir = "test_audio"
    output_dir = "parselmouth_reports"
    os.makedirs(output_dir, exist_ok=True)

    audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".wav")]
    if not audio_files:
        print("❌ No .wav files found in 'test_audio'")
        return

    for filename in audio_files:
        file_path = os.path.join(input_dir, filename)
        sound = load_audio(file_path)
        cpp = calculate_cpp_simple(file_path)

        if sound:
            hnr = extract_hnr(sound)
            report = generate_clarity_quality_report(hnr, cpp, filename)

            # ✅ Zmieniona nazwa pliku raportu:
            report_filename = f"11_{os.path.splitext(filename)[0]}_parselmouth_voice_clarity_report.txt"
            report_path = os.path.join(output_dir, report_filename)

            with open(report_path, "w") as f:
                f.write(report)
            print(f"✅ Report saved: {report_path}")
        else:
            print(f"❌ Failed to load: {filename}")

if __name__ == "__main__":
    main()
