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

# Normalize the data for visualization
data_normalized = (data - data.min()) / (data.max() - data.min())

# Plot the heatmap using a subset of the data to reduce load
subset_size = 1000  # Adjust to manage performance
data_normalized_subset = data_normalized.iloc[:subset_size]

plt.figure(figsize=(12, 6))
sns.heatmap(data_normalized_subset.T, cmap="viridis", cbar=True, xticklabels=100, yticklabels=channel_names)
plt.title("EEG Time-Series Heatmap (Subset)")
plt.xlabel("Time (sample index)")
plt.ylabel("EEG Channels")
plt.xticks(rotation=45)
plt.show()
