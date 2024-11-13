import pandas as pd
import lightningchart as lc
import numpy as np

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

# Initialize the LightningChart for a single XY chart
chart = lc.ChartXY()
chart.set_title("Stacked Area Chart of EEG Channels Over Time")
chart.get_default_y_axis().set_title("EEG Amplitude (μV)")
chart.get_default_x_axis().set_title("Time (Sample Index)")

# Adding a legend for the stacked area chart
legend = chart.add_legend()

# Create stacked area series for each EEG channel
for channel in channel_names:
    # Create area series for each channel
    area_series = chart.add_area_series()
    area_series.set_name(channel)
    
    # Add data to the area series
    area_series.add(list(range(len(data))), data[channel].values)
    
    # Add series to legend
    legend.add(area_series)

# Display the chart
chart.open()
