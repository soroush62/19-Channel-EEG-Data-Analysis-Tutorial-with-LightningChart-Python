import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define channel names
channel_names = [
    "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
    "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
]

# Path to the combined data CSV file
file_path = 'Dataset/all_data_combined.csv'

# Read the data, and convert each value to a numeric, forcing errors to NaN
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce')

# Drop rows that contain any NaN values (optional, if data sparsity is an issue)
data = data.dropna()

# Plot the box plot
plt.figure(figsize=(12, 6))
sns.boxplot(data=data, orient="h")
plt.title("Box Plot of Amplitude Distribution by Channel")
plt.xlabel("Amplitude")
plt.ylabel("EEG Channels")
plt.show()
