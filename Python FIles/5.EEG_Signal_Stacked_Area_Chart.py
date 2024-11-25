import pandas as pd
import lightningchart as lc
import numpy as np

lc.set_license('my-license-key')

channel_names = [
    "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
    "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
]

# Load EEG data
file_path = 'Dataset/all_data_combined.csv'
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)

# Convert to numeric and drop rows with missing values
data = data.apply(pd.to_numeric, errors='coerce').dropna()

# Downsample the dataset by averaging over windows
window_size = 10
downsampled_data = data.groupby(data.index // window_size).mean()

# Apply logarithmic normalization
log_normalized_data = np.log1p(np.abs(downsampled_data))

chart = lc.ChartXY()
chart.set_title("Stacked Area Chart of Log-Normalized EEG Channels Over Time (Downsampled)")
chart.get_default_y_axis().set_title("Log-Normalized EEG Amplitude")
chart.get_default_x_axis().set_title("Time (Downsampled Index)")

legend = chart.add_legend()

for channel in channel_names:
    area_series = chart.add_area_series()
    area_series.set_name(channel)
    
    area_series.add(list(range(len(log_normalized_data))), log_normalized_data[channel].values)
    
    legend.add(area_series)

chart.open()
