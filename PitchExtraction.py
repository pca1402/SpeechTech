import numpy as np
import parselmouth
from scipy.io import wavfile
import os

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
  categorizing them as Masculine/Femenine depending on said value.
  """
  if (frequency > 160):
    gender = "Femenine"
  else:
    gender = "Masculine"
  return gender

folder_path = r'C:\Users\paula\Speech_Tech_Project\SampleData' # Use 'r' prefix for raw string to handle backslashes
# Iterate through all entries in the directory
for filename in os.listdir(folder_path):
    # Construct the full path
    full_path = os.path.join(folder_path, filename)
    # Check if the current entry is a file
    if os.path.isfile(full_path):
      mean_freq = extract_pitch(full_path, 85, 255)
      gender = gender_classify(mean_freq)
      print(f"Result {filename}: {mean_freq}Hz = {gender}")
