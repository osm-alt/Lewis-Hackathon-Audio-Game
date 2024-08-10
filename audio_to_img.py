import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def save_sound_wave_image(audio_file, output_image_file):
    # Read the audio file
    sample_rate, data = wavfile.read(audio_file)

    # Check if the audio file is stereo or mono
    if len(data.shape) == 2:
        data = data.mean(axis=1)  # Convert stereo to mono by averaging channels

    # Create a time array in seconds
    time = np.linspace(0, len(data) / sample_rate, num=len(data))

    # Plot the waveform
    plt.figure(figsize=(10, 4))
    plt.plot(time, data)
    plt.title("Sound Wave")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid()
    
    # Save the plot as an image file
    plt.savefig(output_image_file)
    plt.close()