"""
Solution 3: Speech Fluency and Pause Analysis using Parselmouth

This script loads an audio file, analyzes speech fluency by segmenting speech and silence,
calculates speech/articulation rates (conceptually, as syllable count is external),
and measures pause characteristics using Parselmouth. It generates a textual summary
and saves it to a report file.
"""

import parselmouth
from parselmouth.praat import call
import numpy as np
import os
import sys
import uuid

def load_audio(audio_file_path):
    try:
        return parselmouth.Sound(audio_file_path)
    except parselmouth.PraatError as e:
        print(f"Error loading audio file {audio_file_path}: {e}")
        return None

def segment_speech_silence(sound, silence_threshold_db_factor=0.3, min_pause_duration_s=0.15, min_speech_duration_s=0.1):
    segments = []
    try:
        intensity = sound.to_intensity(minimum_pitch=100)
        max_intensity = call(intensity, "Get maximum", 0, 0, "Parabolic")
        silence_threshold_db = max_intensity - 25 if not np.isnan(max_intensity) else -35
        silence_threshold_db = max(silence_threshold_db, -50)

        num_frames = call(intensity, "Get number of frames")
        time_step = intensity.get_time_step()
        start_time = intensity.get_start_time()
        current_label = None
        segment_start = start_time

        for i in range(num_frames):
            frame_time = call(intensity, "Get time from frame number", i + 1)
            frame_intensity = call(intensity, "Get value in frame", i + 1)
            label = "silence" if frame_intensity < silence_threshold_db else "speech"

            if current_label is None:
                current_label = label
                segment_start = frame_time - time_step / 2
            elif label != current_label:
                segment_end = frame_time - time_step / 2
                duration = segment_end - segment_start
                if (current_label == "speech" and duration >= min_speech_duration_s) or \
                   (current_label == "silence" and duration >= min_pause_duration_s):
                    segments.append((current_label, segment_start, segment_end))
                current_label = label
                segment_start = segment_end

        # Last segment
        if current_label:
            segment_end = intensity.get_end_time()
            duration = segment_end - segment_start
            if (current_label == "speech" and duration >= min_speech_duration_s) or \
               (current_label == "silence" and duration >= min_pause_duration_s):
                segments.append((current_label, segment_start, segment_end))

    except Exception as e:
        print(f"Error in segmentation: {e}")
    return segments

def calculate_fluency_metrics(sound_duration, segments, num_syllables_placeholder=None):
    total_speech = sum(end - start for label, start, end in segments if label == "speech")
    total_pause = sum(end - start for label, start, end in segments if label == "silence")
    num_pauses = sum(1 for label, *_ in segments if label == "silence")
    pause_durations = [end - start for label, start, end in segments if label == "silence"]

    speech_rate = (num_syllables_placeholder / sound_duration) if sound_duration > 0 and num_syllables_placeholder else np.nan
    articulation_rate = (num_syllables_placeholder / total_speech) if total_speech > 0 and num_syllables_placeholder else np.nan
    avg_syllable_duration = (total_speech / num_syllables_placeholder) if total_speech > 0 and num_syllables_placeholder else np.nan
    mean_pause_duration = np.mean(pause_durations) if pause_durations else np.nan

    return {
        "total_duration_s": sound_duration,
        "phonation_time_s": total_speech,
        "total_pause_duration_s": total_pause,
        "num_pauses": num_pauses,
        "mean_pause_duration_s": mean_pause_duration,
        "speech_rate_sps": speech_rate,
        "articulation_rate_sps": articulation_rate,
        "avg_syllable_duration_s": avg_syllable_duration,
        "segments": segments
    }

def generate_fluency_report(metrics, audio_file_name):
    report = f"Speech Fluency and Pause Analysis Report for: {audio_file_name}\n"
    report += "------------------------------------------------------------\n\n"
    report += f"Total Duration: {metrics['total_duration_s']:.2f} s\n"
    report += f"Phonation Time: {metrics['phonation_time_s']:.2f} s\n"
    report += f"Total Pause Duration: {metrics['total_pause_duration_s']:.2f} s\n"
    report += f"Number of Pauses: {metrics['num_pauses']}\n"
    report += f"Mean Pause Duration: {metrics['mean_pause_duration_s']:.2f} s\n\n" if not np.isnan(metrics['mean_pause_duration_s']) else "Mean Pause Duration: N/A\n\n"
    report += f"Speech Rate: {metrics['speech_rate_sps']:.2f} syll/s\n" if not np.isnan(metrics['speech_rate_sps']) else "Speech Rate: N/A\n"
    report += f"Articulation Rate: {metrics['articulation_rate_sps']:.2f} syll/s\n" if not np.isnan(metrics['articulation_rate_sps']) else "Articulation Rate: N/A\n"
    report += f"Avg Syllable Duration: {metrics['avg_syllable_duration_s']:.3f} s\n\n" if not np.isnan(metrics['avg_syllable_duration_s']) else "Avg Syllable Duration: N/A\n\n"

    report += "Segmentation Preview (first 10 segments):\n"
    for i, (label, start, end) in enumerate(metrics["segments"][:10]):
        report += f"  - {label.title()} from {start:.2f}s to {end:.2f}s ({end-start:.2f}s)\n"
    if len(metrics["segments"]) > 10:
        report += "  ...\n"

    report += "\nNotes:\n- Placeholder syllable count = 20\n- Adjust for better accuracy using real count.\n"
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

        for file in wav_files:
            path = os.path.join(input_dir, file)
            sound = load_audio(path)
            if sound:
                segments = segment_speech_silence(sound, min_pause_duration_s=0.1, min_speech_duration_s=0.1)
                metrics = calculate_fluency_metrics(sound.get_total_duration(), segments, num_syllables_placeholder=20)
                report = generate_fluency_report(metrics, file)

                identifier_uuid = str(uuid.uuid4())
                algorithm_number = "03"
                algorithm_name = "parselmouth_speech_fluency"
                report_name = f"{algorithm_number}_{identifier_uuid}_{algorithm_name}.txt"
                report_path = os.path.join(output_dir, report_name)

                with open(report_path, "w") as f:
                    f.write(report)

                print(f"✅ Report saved: {report_path}")
            else:
                print(f"❌ Failed to process {file}")
                sys.exit(1)

        sys.exit(0)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()








