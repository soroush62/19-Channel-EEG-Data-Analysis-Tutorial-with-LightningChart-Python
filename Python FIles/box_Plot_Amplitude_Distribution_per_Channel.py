# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Define channel names
# channel_names = [
#     "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
#     "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
# ]

# # Path to the combined data CSV file
# file_path = 'Dataset/all_data_combined.csv'

# # Read the data, and convert each value to a numeric, forcing errors to NaN
# data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', low_memory=False)
# data = data.apply(pd.to_numeric, errors='coerce')

# # Drop rows that contain any NaN values (optional, if data sparsity is an issue)
# data = data.dropna()

# # Plot the box plot
# plt.figure(figsize=(12, 6))
# sns.boxplot(data=data, orient="h")
# plt.title("Box Plot of Amplitude Distribution by Channel")
# plt.xlabel("Amplitude")
# plt.ylabel("EEG Channels")
# plt.show()




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

# # Read the data, and convert each value to numeric, handling non-numeric entries by converting to NaN
# data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', low_memory=False)
# data = data.apply(pd.to_numeric, errors='coerce').dropna()  # Drop rows with NaN values

# # Create a LightningChart box plot
# chart = lc.ChartXY(
#     theme=lc.Themes.Light,
#     title="Box Plot of Amplitude Distribution by Channel"
# )

# # Prepare data for the box plot
# dataset = []
# x_values_outlier = []
# y_values_outlier = []

# for i, channel in enumerate(channel_names):
#     # Extract data for each channel
#     column_data = data[channel].values

#     # Define positions for each box in the plot
#     start = (i * 2) + 1
#     end = start + 1

#     # Calculate statistics for the box plot
#     lower_quartile = float(np.percentile(column_data, 25))
#     upper_quartile = float(np.percentile(column_data, 75))
#     median = float(np.median(column_data))
#     lower_extreme = float(np.min(column_data))
#     upper_extreme = float(np.max(column_data))

#     # Add the box plot data for this channel
#     box_data = {
#         'start': start,
#         'end': end,
#         'lowerQuartile': lower_quartile,
#         'upperQuartile': upper_quartile,
#         'median': median,
#         'lowerExtreme': lower_extreme,
#         'upperExtreme': upper_extreme
#     }
#     dataset.append(box_data)

#     # Identify outliers using the IQR method
#     iqr = upper_quartile - lower_quartile
#     lower_bound = lower_quartile - 1.5 * iqr
#     upper_bound = upper_quartile + 1.5 * iqr
#     outliers = [y for y in column_data if y < lower_bound or y > upper_bound]

#     # Add outliers to the plot
#     for outlier in outliers:
#         x_values_outlier.append(start + 0.5)  # Set outliers at the middle of each box
#         y_values_outlier.append(outlier)

# # Add box series to the chart
# box_series = chart.add_box_series()
# box_series.add_multiple(dataset)

# # Add outliers as a separate point series
# outlier_series = chart.add_point_series(
#     sizes=True,
#     rotations=True,
#     lookup_values=True
# )
# outlier_series.set_point_color(lc.Color('red'))
# outlier_series.append_samples(
#     x_values=x_values_outlier,
#     y_values=y_values_outlier,
#     sizes=[1] * len(y_values_outlier)  # Set a uniform size for all outliers
# )

# # Customize axis labels
# chart.get_default_x_axis().set_title("Amplitude")
# chart.get_default_y_axis().set_title("EEG Channels")

# # Display the chart
# chart.open()








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

# Read the data, and convert each value to numeric, handling non-numeric entries by converting to NaN
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce').dropna()  # Drop rows with NaN values

# Create a LightningChart box plot
chart = lc.ChartXY(
    theme=lc.Themes.Light,
    title="Box Plot of Amplitude Distribution by Channel"
)

# Customize x-axis labels to show channel names
x_axis = chart.get_default_x_axis()
x_axis.set_title("EEG Channels")
x_axis.set_tick_strategy('Empty')

# Prepare data for the box plot with a wider spacing between boxes
dataset = []
x_values_outlier = []
y_values_outlier = []
gap = 3  # Increase this gap to separate the boxes more

for i, channel in enumerate(channel_names):
    # Extract data for each channel
    column_data = data[channel].values

    # Define positions for each box in the plot with increased spacing
    start = i * gap
    end = start + 1

    # Calculate statistics for the box plot
    lower_quartile = float(np.percentile(column_data, 25))
    upper_quartile = float(np.percentile(column_data, 75))
    median = float(np.median(column_data))
    lower_extreme = float(np.min(column_data))
    upper_extreme = float(np.max(column_data))

    # Add the box plot data for this channel
    box_data = {
        'start': start,
        'end': end,
        'lowerQuartile': lower_quartile,
        'upperQuartile': upper_quartile,
        'median': median,
        'lowerExtreme': lower_extreme,
        'upperExtreme': upper_extreme
    }
    dataset.append(box_data)

    # Add custom tick labels at the midpoint of each box
    custom_tick = x_axis.add_custom_tick()
    custom_tick.set_value((start + end) / 2)
    custom_tick.set_text(channel)

    # Identify outliers using the IQR method
    iqr = upper_quartile - lower_quartile
    lower_bound = lower_quartile - 1.5 * iqr
    upper_bound = upper_quartile + 1.5 * iqr
    outliers = [y for y in column_data if y < lower_bound or y > upper_bound]

    # Add outliers to the plot
    for outlier in outliers:
        x_values_outlier.append((start + end) / 2)  # Center outliers within each box
        y_values_outlier.append(outlier)

# Add box series to the chart
box_series = chart.add_box_series()
box_series.add_multiple(dataset)

# Add outliers as a separate point series
outlier_series = chart.add_point_series(
    sizes=True,
    rotations=True,
    lookup_values=True
)
outlier_series.set_point_color(lc.Color('red'))
outlier_series.append_samples(
    x_values=x_values_outlier,
    y_values=y_values_outlier,
    sizes=[3] * len(y_values_outlier)  # Set a uniform size for all outliers
)

# Customize y-axis label
chart.get_default_y_axis().set_title("Amplitude")

# Display the chart
chart.open()
