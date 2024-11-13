import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import welch

# Define channel names
channel_names = [
    "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
    "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
]

# Path to the combined data CSV file
file_path = 'Dataset/all_data_combined.csv'

# Read data with additional steps to handle non-numeric values
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)

# Convert all values to numeric, forcing non-numeric entries to NaN, then drop these rows
data = data.apply(pd.to_numeric, errors='coerce').dropna()
plt.figure(figsize=(15, 10))
for i, channel in enumerate(channel_names, 1):
    plt.subplot(5, 4, i)
    plt.hist(data[channel], bins=20, color='blue', alpha=0.7)
    plt.title(channel)
    plt.xlabel("Amplitude")
    plt.ylabel("Frequency")

plt.tight_layout()
plt.suptitle("Histogram of Amplitude Values by Channel", y=1.02)
plt.show()
