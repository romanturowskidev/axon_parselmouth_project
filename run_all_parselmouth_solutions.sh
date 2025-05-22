#!/bin/bash
# Script to run all Parselmouth-based voice analysis solutions sequentially.

PYTHON_EXECUTABLE="python3"
BASE_DIR="."

SOLUTIONS=(
    "01_parselmouth_vocal_stability.py"
    "02_parselmouth_hypophonia_monotony.py"
    "03_parselmouth_speech_fluency.py"
    "04_parselmouth_voice_clarity.py"
    "05_parselmouth_prosodic_variability.py"
    "06_parselmouth_vocal_effort.py"
    "07_parselmouth_parameter_shift.py"
    "08_parselmouth_baseline_profile.py"
    "09_parselmouth_longitudinal_trend.py"
    "10_parselmouth_formant_vocal_tract.py"
)

echo "Starting execution of all Parselmouth-based voice analysis solutions..."

for solution_script in "${SOLUTIONS[@]}"
do
    echo "----------------------------------------------------------------------"
    echo "Running: ${solution_script}"
    echo "----------------------------------------------------------------------"
    
    if [ -f "${BASE_DIR}/${solution_script}" ]; then
        ${PYTHON_EXECUTABLE} "${BASE_DIR}/${solution_script}"
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 0 ]; then
            echo "✅ Successfully executed ${solution_script}"
        else
            echo "❌ Error executing ${solution_script} (exit code: $EXIT_CODE)"
            echo "Stopping execution."
            exit 1
        fi
    else
        echo "❌ Error: Script ${BASE_DIR}/${solution_script} not found."
        echo "Stopping execution."
        exit 1
    fi

    echo ""
done

echo "----------------------------------------------------------------------"
echo "✅ All Parselmouth-based solutions executed successfully."
exit 0
