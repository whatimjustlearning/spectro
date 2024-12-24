import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse

def plot_waveform(wav_file):
    # Read the WAV file
    sample_rate, data = wavfile.read(wav_file)
    
    # Determine if the audio is stereo or mono
    if len(data.shape) == 2:
        data = data.mean(axis=1)  # Convert stereo to mono by averaging channels
    
    # Create a time array in seconds
    time = np.linspace(0, len(data) / sample_rate, num=len(data))
    
    # Plot the waveform
    plt.figure(figsize=(10, 4))
    plt.plot(time, data, label="Waveform")
    plt.title("Waveform of " + wav_file)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot the waveform of a WAV file.")
    parser.add_argument("wav_file", type=str, help="Path to the WAV file")
    args = parser.parse_args()
    
    plot_waveform(args.wav_file)

if __name__ == "__main__":
    main()