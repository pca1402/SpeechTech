import numpy as np
import parselmouth
from scipy.io import wavfile
import os
from pathlib import Path

def extract_pitch(audio_file, fmin, fmax):
  """
  This function extracts pitch from audio file using Parselmouth library.
  Args:
  audio_file: Path to .wav file
  fmin: Minimum pitch to detect (Hz)
  fmax: Maximum pitch to detect (Hz)
  Returns:
  mean_f0: Mean fundamental frequency in Hz
  """
  # Load sound file
  sound = parselmouth.Sound(audio_file)
  # Extract pitch
  pitch = sound.to_pitch(pitch_floor=fmin, pitch_ceiling=fmax)
  # Get pitch values
  pitch_values = pitch.selected_array['frequency']
  # Remove unvoiced frames (where pitch = 0)
  pitch_values = pitch_values[pitch_values > 0]
  if len(pitch_values) > 0:
    mean_f0 = np.mean(pitch_values)
  else:
    mean_f0 = 0
    print(f"Warning: No pitch detected in {audio_file}")
  return mean_f0

def gender_classify(frequency):
  """
  This function classifies extracted audio files based on their mean_f0,
  categorizing them as Masculine/Feminine depending on said value.
  """
  if (frequency > 160):
    gender = "Feminine"
  else:
    gender = "Masculine"
  return gender

# Get the directory where THIS script is saved
# .resolve() ensures handling of symlinks or weird OS paths
BASE_DIR = Path(__file__).resolve().parent

# Define data folder relative to that base
# Even if someone else clones this Git repo/script, it will still work without needing to change any paths, as long as the folder structure is maintained
data_folder = BASE_DIR / "SampleData"

# Accessing a specific file
file_path = data_folder / "audio_01.wav"

folder_path = data_folder / "AudioSamples" / "GivenSamples"
# Iterate through all entries in the directory
for filename in os.listdir(folder_path):
    # Construct the full path
    full_path = os.path.join(folder_path, filename)
    # Check if the current entry is a file
    if os.path.isfile(full_path):
      mean_freq = extract_pitch(full_path, 85, 255)
      gender = gender_classify(mean_freq)
      print(f"Result given_{filename}: {mean_freq}Hz = {gender}")

folder_path = data_folder / "AudioSamples" / "CollectedSamples"
# Iterate through all entries in the directory
for filename in os.listdir(folder_path):
    # Construct the full path
    full_path = os.path.join(folder_path, filename)
    # Check if the current entry is a file
    if os.path.isfile(full_path):
      mean_freq = extract_pitch(full_path, 85, 255)
      gender = gender_classify(mean_freq)
      print(f"Result collected_{filename}: {mean_freq}Hz = {gender}")
