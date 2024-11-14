import pandas as pd
import numpy as np
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

# Read data with additional steps to handle non-numeric values
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce').dropna()

# Initialize a dashboard with 5 rows and 4 columns (for 19 channels, this will fit well)
dashboard = lc.Dashboard(rows=5, columns=4, theme=lc.Themes.Dark)

# Function to create histogram bar chart
def create_histogram(column_data, channel_name, row_index, col_index):
    # Calculate histogram data
    counts, bin_edges = np.histogram(column_data, bins=20)
    bar_data = [{'category': f'{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}', 'value': int(counts[i])} for i in range(len(counts))]

    # Create a bar chart for each EEG channel
    chart = dashboard.BarChart(
        row_index=row_index,
        column_index=col_index
    )
    chart.set_title(f'Histogram of {channel_name}')
    
    # Set histogram data
    chart.set_data(bar_data)

    # Customize the color palette
    chart.set_palette_colors(
        steps=[
            {'value': 0, 'color': lc.Color('blue')}, 
            {'value': 0.5, 'color': lc.Color('yellow')}, 
            {'value': 1, 'color': lc.Color('red')}  
        ],
        percentage_values=True 
    )

# Loop through each channel and create a histogram chart for it
for i, channel in enumerate(channel_names):
    row_index = i // 4  # Divide to get row position
    col_index = i % 4   # Modulo to get column position
    
    # Create a histogram for each channel
    create_histogram(data[channel].dropna(), channel, row_index, col_index)

# Open the dashboard to display the charts
dashboard.open()