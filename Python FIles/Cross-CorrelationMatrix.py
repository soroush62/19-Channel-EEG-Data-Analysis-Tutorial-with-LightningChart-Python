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

# Read data with additional steps to handle non-numeric values
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)

# Convert all data to numeric, forcing non-numeric values to NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Drop rows with any NaN values (this ensures we only use valid numeric data)
data = data.dropna()

# Compute the correlation matrix
correlation_matrix = data.corr()

# Plot the heatmap of the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, square=True,
            xticklabels=channel_names, yticklabels=channel_names)
plt.title("Cross-Correlation Matrix of EEG Channels")
plt.show()
