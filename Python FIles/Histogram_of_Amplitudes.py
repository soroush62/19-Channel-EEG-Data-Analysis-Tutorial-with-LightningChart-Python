# # import pandas as pd
# # import numpy as np
# # import matplotlib.pyplot as plt
# # import seaborn as sns
# # from scipy.signal import welch

# # # Define channel names
# # channel_names = [
# #     "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
# #     "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
# # ]

# # # Path to the combined data CSV file
# # file_path = 'Dataset/all_data_combined.csv'

# # # Read data with additional steps to handle non-numeric values
# # data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)

# # # Convert all values to numeric, forcing non-numeric entries to NaN, then drop these rows
# # data = data.apply(pd.to_numeric, errors='coerce').dropna()
# # plt.figure(figsize=(15, 10))
# # for i, channel in enumerate(channel_names, 1):
# #     plt.subplot(5, 4, i)
# #     plt.hist(data[channel], bins=20, color='blue', alpha=0.7)
# #     plt.title(channel)
# #     plt.xlabel("Amplitude")
# #     plt.ylabel("Frequency")

# # plt.tight_layout()
# # plt.suptitle("Histogram of Amplitude Values by Channel", y=1.02)
# # plt.show()





# import pandas as pd
# import numpy as np
# import lightningchart as lc

# # Load LightningChart license
# lc.set_license(open('../license-key').read())

# # Define channel names
# channel_names = [
#     "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
#     "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
# ]

# # Path to the combined data CSV file
# file_path = 'Dataset/all_data_combined.csv'

# # Read data with additional steps to handle non-numeric values
# data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)
# data = data.apply(pd.to_numeric, errors='coerce').dropna()

# # Initialize a dashboard with 5 rows and 4 columns (for 19 channels, this will fit well)
# dashboard = lc.Dashboard(rows=5, columns=4, theme=lc.Themes.Dark)

# # Function to create histogram bar chart
# def create_histogram(column_data, channel_name, row_index, col_index):
#     # Calculate histogram data
#     counts, bin_edges = np.histogram(column_data, bins=20)
#     bar_data = [{'category': f'{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}', 'value': int(counts[i])} for i in range(len(counts))]

#     # Create a bar chart for each EEG channel
#     chart = dashboard.BarChart(
#         row_index=row_index,
#         column_index=col_index
#     )
#     chart.set_title(f'Histogram of {channel_name}')
    
#     # Set histogram data
#     chart.set_data(bar_data)

#     # Customize the color palette
#     chart.set_palette_colors(
#         steps=[
#             {'value': 0, 'color': lc.Color('blue')}, 
#             {'value': 0.5, 'color': lc.Color('yellow')}, 
#             {'value': 1, 'color': lc.Color('red')}  
#         ],
#         percentage_values=True 
#     )

# # Loop through each channel and create a histogram chart for it
# for i, channel in enumerate(channel_names):
#     row_index = i // 4  # Divide to get row position
#     col_index = i % 4   # Modulo to get column position
    
#     # Create a histogram for each channel
#     create_histogram(data[channel].dropna(), channel, row_index, col_index)

# # Open the dashboard to display the charts
# dashboard.open()

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

# Read data and convert to numeric, handling non-numeric values by coercing to NaN and dropping them
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce').dropna()

# Bin count for histograms
bin_count = 20

# Initialize LightningChart Dashboard for individual charts
dashboard = lc.Dashboard(rows=5, columns=4, theme=lc.Themes.Light)

# Function to create histogram for each channel with dynamic bin range
def create_histogram(data_column, channel_name, row_index, col_index):
    # Calculate histogram bins based on the data range for each channel
    data_min = data_column.min()
    data_max = data_column.max()
    counts, bin_edges = np.histogram(data_column, bins=bin_count, range=(data_min, data_max))
    
    # Format data for LightningChart
    bar_data = [{'category': f'{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}', 'value': int(counts[i])} for i in range(len(counts))]
    
    # Create a bar chart for each channel
    chart = dashboard.BarChart(
        column_index=col_index,
        row_index=row_index,
        row_span=1,
        column_span=1
    )
    chart.set_title(f'Channel: {channel_name}')
    chart.set_bars_effect(False)  # Disable gradient effect for a solid color look

    # Set color and data
    chart.set_data(bar_data)
    chart.set_palette_colors([{'value': 1, 'color': lc.Color('#3498db')}])  # Use a single blue color for all bars

# Loop through channels and create histograms
for i, channel in enumerate(channel_names):
    row_index = i // 4  # Arrange in a 5x4 grid
    col_index = i % 4
    create_histogram(data[channel], channel, row_index, col_index)

# Display the dashboard
dashboard.open()
