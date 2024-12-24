import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse
import os

def plot_spectrogram(wav_file, output_file=None):
    # Read the WAV file
    sample_rate, data = wavfile.read(wav_file)
    
    # Determine if the audio is stereo or mono
    if len(data.shape) == 2:
        data = data.mean(axis=1)  # Convert stereo to mono by averaging channels
    
    # Plot the spectrogram
    plt.figure(figsize=(10, 4))
    plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512, cmap='viridis')
    plt.title("Spectrogram of " + os.path.basename(wav_file))
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.colorbar(label='Intensity [dB]')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file)
        print(f"Spectrogram saved as {output_file}")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot the spectrogram of a WAV file.")
    parser.add_argument("wav_file", type=str, help="Path to the WAV file")
    parser.add_argument("-o", "--output", type=str, help="Output file for the spectrogram image (e.g., spectrogram.png)")
    args = parser.parse_args()
    
    plot_spectrogram(args.wav_file, args.output)

if __name__ == "__main__":
    main()