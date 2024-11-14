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

# Read and process data
data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce').dropna()  # Convert all data to numeric and drop NaNs

# Compute correlation matrix
corr_matrix = data.corr()
corr_array = corr_matrix.to_numpy()

min_value = corr_array.min()
max_value = corr_array.max()

# Initialize LightningChart
chart = lc.ChartXY(
    title="Cross-Correlation Matrix of EEG Channels",
    theme=lc.Themes.Light
)

# Define grid dimensions based on correlation matrix
grid_size_x, grid_size_y = corr_array.shape

# Add heatmap series for displaying the correlation matrix
heatmap_series = chart.add_heatmap_grid_series(
    columns=grid_size_x,
    rows=grid_size_y,
)

# Configure heatmap boundaries and interpolation
heatmap_series.set_start(x=0, y=0)
heatmap_series.set_end(x=grid_size_x, y=grid_size_y)
heatmap_series.set_step(x=1, y=1)
heatmap_series.set_wireframe_stroke(thickness=1, color=lc.Color('lightgrey'))

# Set intensity values from the correlation matrix
heatmap_series.invalidate_intensity_values(corr_array.tolist())
heatmap_series.set_intensity_interpolation(False)

# Define color palette for the correlation matrix
palette_steps = [
    {"value": min_value, "color": lc.Color('blue')},     # Strong negative correlation
    {"value": 0, "color": lc.Color('white')},     # No correlation
    {"value": 1, "color": lc.Color('red')}        # Strong positive correlation
]

heatmap_series.set_palette_coloring(
    steps=palette_steps,
    look_up_property='value',
    interpolate=True
)

# Configure x and y axes
x_axis = chart.get_default_x_axis()
y_axis = chart.get_default_y_axis()

# Set axes to custom tick labels only
x_axis.set_tick_strategy('Empty')
y_axis.set_tick_strategy('Empty')

# Add custom ticks for channel names on both axes
for i, label in enumerate(channel_names):
    # X-axis custom ticks with rotation
    custom_tick_x = x_axis.add_custom_tick().set_tick_label_rotation(90)
    custom_tick_x.set_value(i + 0.5)  # Center tick in the grid cell
    custom_tick_x.set_text(label)
    
    # Y-axis custom ticks
    custom_tick_y = y_axis.add_custom_tick()
    custom_tick_y.set_value(i + 0.5)  # Center tick in the grid cell
    custom_tick_y.set_text(label)

# Optional: Add a legend for better interpretation of values
legend = chart.add_legend(data=heatmap_series).set_margin(-20)

# Display the chart
chart.open()
