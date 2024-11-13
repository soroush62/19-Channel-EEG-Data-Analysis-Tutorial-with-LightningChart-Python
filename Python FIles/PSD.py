# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from scipy.signal import welch

# # Define channel names
# channel_names = [
#     "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
#     "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
# ]

# # Path to the combined data CSV file
# file_path = 'Dataset/all_data_combined.csv'

# # Read data with additional steps to handle non-numeric values
# data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)

# # Convert all values to numeric, forcing non-numeric entries to NaN, then drop these rows
# data = data.apply(pd.to_numeric, errors='coerce').dropna()

# plt.figure(figsize=(12, 6))
# for channel in channel_names:
#     freqs, psd = welch(data[channel], fs=256, nperseg=512)  # Assuming a sampling rate of 256 Hz
#     plt.semilogy(freqs, psd, label=channel)
    
# plt.title("Power Spectral Density (PSD) of EEG Channels")
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Power Spectral Density (uV^2/Hz)")
# plt.legend(loc="upper right", ncol=2)
# plt.show()




import pandas as pd
import numpy as np
from scipy.signal import welch
import lightningchart as lc

# Load LightningChart license
lc.set_license(open('../license-key').read())

# Define channel names
channel_names = [
    "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
    "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
]

# Path to the combined data CSV file
file_path = 'Dataset/all_data_combined.csv'

# Read and clean data
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce').dropna()

# Initialize LightningChart
chart = lc.ChartXY()
chart.set_title("Power Spectral Density (PSD) of EEG Channels")
chart.get_default_y_axis().set_title("Log(Power Spectral Density) (log(uV^2/Hz))")
chart.get_default_x_axis().set_title("Frequency (Hz)")

# Sampling rate and PSD computation
fs = 256
legend = chart.add_legend()
# Iterate over each EEG channel, compute PSD, and apply logarithmic transformation to plot
for channel in channel_names:
    # Compute PSD
    freqs, psd = welch(data[channel], fs=fs, nperseg=512)
    
    # Apply logarithmic transformation to PSD values
    log_psd = np.log10(psd + 1e-10)  # Adding a small constant to avoid log(0)

    # Create a line series for each channel
    line_series = chart.add_line_series()
    line_series.set_name(channel)
    legend.add(line_series)
    
    # # Explicitly set data for the line series
    # line_series.add([(float(f), float(p)) for f, p in zip(freqs, log_psd)])
    for f, p in zip(freqs, log_psd):
        line_series.add(f, p)

# Display the chart
chart.open()
