# import lightningchart as lc
# import numpy as np
# import trimesh

# lc.set_license(open('../license-key').read()) 

# # Load the 3D brain model
# brain_model_path = 'Dataset/Brain/Brain_OBJ.obj'  # Replace with the path to your actual brain model file
# brain_scene = trimesh.load(brain_model_path)

# # If the loaded brain model is a scene, extract the mesh
# if isinstance(brain_scene, trimesh.Scene):
#     brain_mesh = brain_scene.dump(concatenate=True)
# else:
#     brain_mesh = brain_scene

# # Extract vertices, indices, and normals for LightningChart
# brain_vertices = brain_mesh.vertices.flatten().tolist()
# brain_indices = brain_mesh.faces.flatten().tolist()
# brain_normals = brain_mesh.vertex_normals.flatten().tolist()

# # Initialize the 3D chart
# chart = lc.Chart3D(
#     title="EEG Channel Visualization on Brain Model",
#     theme=lc.Themes.Dark
# )

# # Add the brain mesh model to the chart
# brain_model = chart.add_mesh_model()
# brain_model.set_model_geometry(vertices=brain_vertices, indices=brain_indices, normals=brain_normals)

# # Set the appearance of the brain model
# brain_model.set_scale(0.02)
# brain_model.set_model_location(0, 0, 40)
# brain_model.set_color_shading_style(
#     phong_shading=True,
#     specular_reflection=0.5,
#     specular_color=lc.Color(255, 255, 255)  # white specular color for highlights
# )
# brain_model.set_color(lc.Color(200, 200, 200, 100))  # semi-transparent gray

# # Define EEG channel positions (approximated)
# channel_positions = {
#     "Fp1": [16, 11, 13],
#     "Fp2": [-16, 11, 13],
#     "F3": [19, 31, 19.1],
#     "F4": [-19, 31, 19.1],
#     "F7": [30, 17, 18.1],
#     "F8": [-30, 17, 18.1],
#     "T3": [47, 10, 35.4],
#     "T4": [-47, 10, 35.4],
#     "C3": [32, 37, 40],
#     "C4": [-32, 37, 40],
#     "T5": [33, 9, 60],
#     "T6": [-33, 9, 60],
#     "P3": [17.5, 28, 60],
#     "P4": [-17.5, 28, 60],
#     "O1": [9, 14, 65.5],
#     "O2": [-9, 14, 65.5],
#     "Fz": [0, 36, 23],
#     "Cz": [0, 44, 42.4],
#     "Pz": [0, 25, 62.2]
# }

# # Generate random feature values for each channel (for example)
# feature_values = {ch: np.random.rand() * 2 - 1 for ch in channel_positions.keys()}  # Values between -1 and 1

# # Define the color palette for visualizing feature values
# min_value, max_value = -1, 1  # Define min and max values for the color map

# # # Color mapping function based on feature values
# def get_color_for_value(value):
#     if value <= 0:
#         # Interpolate between blue and white for negative values
#         blue_weight = (value - min_value) / -min_value
#         return lc.Color(
#             int(blue_weight * 0 + (1 - blue_weight) * 255),  # R
#             int(blue_weight * 0 + (1 - blue_weight) * 255),  # G
#             255  # B
#         )
#     else:
#         # Interpolate between white and red for positive values
#         red_weight = value / max_value
#         return lc.Color(
#             255,  # R
#             int((1 - red_weight) * 255),  # G
#             int((1 - red_weight) * 255)  # B
#         )

# # Add data points at each EEG channel position
# for channel, position in channel_positions.items():
#     feature_value = feature_values[channel]
#     color = get_color_for_value(feature_value)

#     # Create a point to represent the EEG channel
#     point_model = chart.add_point_series()
#     point_model.add({
#         'x': position[0],
#         'y': position[1],
#         'z': position[2]
#     })
#     point_model.set_point_color(color)
#     point_model.set_point_size(10)

# # Add a color legend based on the color palette
# color_palette = [
#     {'value': min_value, 'color': lc.Color('blue')},   # Blue for low values
#     {'value': 0, 'color': lc.Color('white')},          # White for mid values
#     {'value': max_value, 'color': lc.Color('red')}     # Red for high values
# ]
# brain_model.set_palette_coloring(
#     steps=color_palette,
#     look_up_property='value',
#     interpolate=True
# )
# x_axis = chart.get_default_x_axis().set_title("X").set_interval(-70, 70, stop_axis_after=True)
# y_axis = chart.get_default_y_axis().set_title("Y").set_interval(-90, 70, stop_axis_after=True)
# z_axis = chart.get_default_z_axis().set_title("Z").set_interval(10, 80, stop_axis_after=True)
# # Display the legend
# legend = chart.add_legend(data=brain_model)
# legend.set_margin(20)

# # Show the chart
# chart.open()

















# import lightningchart as lc
# import pandas as pd
# import numpy as np
# import trimesh
# import time

# # Set the LightningChart license
# lc.set_license(open('../license-key').read())

# # Load the dataset
# file_path = 'Dataset/all_data_combined.csv'
# sampling_interval = 4  # Sampling interval in milliseconds (assuming 4 ms as an example)

# # Define channel names as columns
# channels = ["Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
#             "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"]

# # Load data with specified dtype and handle non-numeric values
# df = pd.read_csv(file_path, header=None, names=channels, dtype=str)

# # Convert all data to numeric, forcing errors to NaN
# df[channels] = df[channels].apply(pd.to_numeric, errors='coerce')

# # Drop rows with any NaN values, which may have resulted from non-numeric values
# df.dropna(inplace=True)

# # Generate a time axis in milliseconds
# df['time_ms'] = np.arange(len(df)) * sampling_interval

# # Load and configure the 3D brain model
# brain_model_path = 'Dataset/Brain/Brain_OBJ.obj'  # Replace with actual path to brain model file
# brain_scene = trimesh.load(brain_model_path)
# brain_mesh = brain_scene if isinstance(brain_scene, trimesh.Trimesh) else brain_scene.dump(concatenate=True)

# # Extract vertices, indices, and normals
# brain_vertices = brain_mesh.vertices.flatten().tolist()
# brain_indices = brain_mesh.faces.flatten().tolist()
# brain_normals = brain_mesh.vertex_normals.flatten().tolist()

# # Initialize the dashboard
# dashboard = lc.Dashboard(columns=2, rows=1, theme=lc.Themes.Dark)

# # Left side: EEG Channel Line Chart
# chart_xy = dashboard.ChartXY(row_index=0, column_index=0, title="EEG Channel Activity Over Time")
# chart_xy.get_default_x_axis().set_title("Time (ms)")
# chart_xy.get_default_y_axis().dispose()  # Remove default y-axis

# legend = chart_xy.add_legend()
# channel_series = {}

# # Add each channel as a separate line series with its own y-axis
# for i, channel in enumerate(channels):
#     axis_y = chart_xy.add_y_axis(stack_index=i)
#     axis_y.set_title(channel).set_interval(-10, 10, stop_axis_after=True)
#     series = chart_xy.add_line_series(y_axis=axis_y, data_pattern='ProgressiveX')
#     series.set_name(channel)
#     channel_series[channel] = series
#     legend.add(series)

# # Right side: 3D Brain Model with EEG Channels
# chart_3d = dashboard.Chart3D(row_index=0, column_index=1, title="EEG Channel Visualization on 3D Brain Model")

# # Add the brain model mesh
# brain_model = chart_3d.add_mesh_model()
# brain_model.set_model_geometry(vertices=brain_vertices, indices=brain_indices, normals=brain_normals)
# brain_model.set_scale(0.02)
# brain_model.set_model_location(0, 0, 40)
# brain_model.set_color(lc.Color(200, 200, 200, 100))  # Semi-transparent brain color

# # Define EEG channel positions on the brain
# channel_positions = {
#     "Fp1": [16, 11, 13], "Fp2": [-16, 11, 13], "F3": [19, 31, 19.1],
#     "F4": [-19, 31, 19.1], "F7": [30, 17, 18.1], "F8": [-30, 17, 18.1],
#     "T3": [47, 10, 35.4], "T4": [-47, 10, 35.4], "C3": [32, 37, 40],
#     "C4": [-32, 37, 40], "T5": [33, 9, 60], "T6": [-33, 9, 60],
#     "P3": [17.5, 28, 60], "P4": [-17.5, 28, 60], "O1": [9, 14, 65.5],
#     "O2": [-9, 14, 65.5], "Fz": [0, 36, 23], "Cz": [0, 44, 42.4], "Pz": [0, 25, 62.2]
# }

# # Initialize series for each EEG channel point on the 3D brain model
# channel_points = {}
# for channel, pos in channel_positions.items():
#     point_series = chart_3d.add_point_series()
#     point_series.add({"x": pos[0], "y": pos[1], "z": pos[2]})
#     point_series.set_point_size(15)
#     channel_points[channel] = point_series

# # Update function to simulate real-time data streaming
# def update_dashboard():
#     # Iterate through each row (time point) in the dataset
#     for idx, row in df.iterrows():
#         time_ms = row['time_ms']

#         # Update line chart for each channel
#         for channel in channels:
#             value = row[channel]
#             channel_series[channel].add(time_ms, value)

#         # Update 3D brain model channel colors based on the latest EEG values
#         min_value, max_value = -10, 10
#         for channel, value in row[channels].items():
#             # Interpolate color based on EEG amplitude value
#             color_ratio = max(0, min((value - min_value) / (max_value - min_value), 1))
#             color = lc.Color(
#                 int((1 - color_ratio) * 0 + color_ratio * 255),  # R (interpolates from blue to red)
#                 int((1 - color_ratio) * 255 + color_ratio * 0),  # G (interpolates from white to red)
#                 int((1 - color_ratio) * 255 + color_ratio * 0)   # B (interpolates from white to red)
#             )
#             channel_points[channel].set_point_color(color)

#         # Sleep for a short interval to simulate real-time update (e.g., 50 ms)
#         time.sleep(0.05)

# # Set axis titles and intervals for the 3D chart
# x_axis = chart_3d.get_default_x_axis().set_title("X").set_interval(-70, 70, stop_axis_after=True)
# y_axis = chart_3d.get_default_y_axis().set_title("Y").set_interval(-90, 70, stop_axis_after=True)
# z_axis = chart_3d.get_default_z_axis().set_title("Z").set_interval(10, 80, stop_axis_after=True)


# # Run the update function
# dashboard.open(live=True)
# update_dashboard()





# import lightningchart as lc
# import pandas as pd
# import numpy as np
# import trimesh
# import time

# # Set the LightningChart license
# lc.set_license(open('../license-key').read())

# # Load the dataset
# file_path = 'Dataset/all_data_combined.csv'
# sampling_interval = 4  # Sampling interval in milliseconds

# # Define channel names as columns
# channels = ["Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
#             "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"]

# # Load data with specified dtype and handle non-numeric values
# df = pd.read_csv(file_path, header=None, names=channels, dtype=str)

# # Convert all data to numeric, forcing errors to NaN
# df[channels] = df[channels].apply(pd.to_numeric, errors='coerce')

# # Replace NaNs with the mean of each channel
# df[channels] = df[channels].apply(lambda x: x.fillna(x.mean()), axis=0)

# # Generate a time axis in milliseconds and add it to the dataframe
# df['time_ms'] = np.arange(len(df)) * sampling_interval

# # Load and configure the 3D brain model
# brain_model_path = 'Dataset/Brain/Brain_OBJ.obj'
# brain_scene = trimesh.load(brain_model_path)
# brain_mesh = brain_scene if isinstance(brain_scene, trimesh.Trimesh) else brain_scene.dump(concatenate=True)

# # Extract vertices, indices, and normals
# brain_vertices = brain_mesh.vertices.flatten().tolist()
# brain_indices = brain_mesh.faces.flatten().tolist()
# brain_normals = brain_mesh.vertex_normals.flatten().tolist()

# # Initialize the dashboard
# dashboard = lc.Dashboard(columns=2, rows=1, theme=lc.Themes.Dark)

# # Left side: EEG Channel Line Chart
# chart_xy = dashboard.ChartXY(row_index=0, column_index=0, title="EEG Channel Activity Over Time")
# chart_xy.get_default_x_axis().set_title("Time (ms)")
# chart_xy.get_default_y_axis().dispose()  # Remove default y-axis

# legend = chart_xy.add_legend()
# channel_series = {}

# # Add each channel as a separate line series with its own y-axis, based on min/max values of each channel
# for i, channel in enumerate(channels):
#     channel_min = df[channel].min()*0.6
#     channel_max = df[channel].max()*0.6

#     axis_y = chart_xy.add_y_axis(stack_index=i).set_tick_strategy("Empty")
#     axis_y.set_title(channel).set_interval(channel_min, channel_max, stop_axis_after=True)
#     series = chart_xy.add_line_series(y_axis=axis_y, data_pattern='ProgressiveXY')  # Ensures lines are connected in order
#     series.set_name(channel)
#     channel_series[channel] = series
#     legend.add(series)

# # Right side: 3D Brain Model with EEG Channels
# chart_3d = dashboard.Chart3D(row_index=0, column_index=1, title="EEG Channel Visualization on 3D Brain Model")

# # Add the brain model mesh
# brain_model = chart_3d.add_mesh_model()
# brain_model.set_model_geometry(vertices=brain_vertices, indices=brain_indices, normals=brain_normals)
# brain_model.set_scale(0.02)
# brain_model.set_model_location(0, 0, 40)
# brain_model.set_color(lc.Color(200, 200, 200, 100))  # Semi-transparent brain color

# # Define EEG channel positions on the brain
# channel_positions = {
#     "Fp1": [16, 11, 13], "Fp2": [-16, 11, 13], "F3": [19, 31, 19.1],
#     "F4": [-19, 31, 19.1], "F7": [30, 17, 18.1], "F8": [-30, 17, 18.1],
#     "T3": [47, 10, 35.4], "T4": [-47, 10, 35.4], "C3": [32, 37, 40],
#     "C4": [-32, 37, 40], "T5": [33, 9, 60], "T6": [-33, 9, 60],
#     "P3": [17.5, 28, 60], "P4": [-17.5, 28, 60], "O1": [9, 14, 65.5],
#     "O2": [-9, 14, 65.5], "Fz": [0, 36, 23], "Cz": [0, 44, 42.4], "Pz": [0, 25, 62.2]
# }

# # Initialize series for each EEG channel point on the 3D brain model
# channel_points = {}
# for channel, pos in channel_positions.items():
#     point_series = chart_3d.add_point_series()
#     point_series.add({"x": pos[0], "y": pos[1], "z": pos[2]})
#     point_series.set_point_size(15)
#     channel_points[channel] = point_series

# # Function to interpolate colors
# def get_color_for_value(value, min_value=-10, max_value=10):
#     # Interpolates color based on EEG amplitude value (blue to red)
#     color_ratio = max(0, min((value - min_value) / (max_value - min_value), 1))
#     return lc.Color(
#         int((1 - color_ratio) * 0 + color_ratio * 255),  # R
#         int((1 - color_ratio) * 255 + color_ratio * 0),  # G
#         int((1 - color_ratio) * 255 + color_ratio * 0)   # B
#     )

# # Update function to simulate real-time data streaming
# def update_dashboard():
#     # Iterate through each row (time point) in the dataset
#     for idx, row in df.iterrows():
#         time_ms = row['time_ms']

#         # Update line chart for each channel
#         for channel in channels:
#             value = row[channel]
#             channel_series[channel].add(time_ms, value)

#         # Update 3D brain model channel colors based on the latest EEG values
#         for channel, value in row[channels].items():
#             color = get_color_for_value(value)
#             channel_points[channel].set_point_color(color)
        
#         brain_model.set_model_rotation(0, 1, 0)
#         # Sleep for a short interval to simulate real-time update (e.g., 50 ms)
#         time.sleep(0.05)

# # Set axis titles and intervals for the 3D chart
# x_axis = chart_3d.get_default_x_axis().set_title("X").set_interval(-70, 70, stop_axis_after=True)
# y_axis = chart_3d.get_default_y_axis().set_title("Y").set_interval(-90, 70, stop_axis_after=True)
# z_axis = chart_3d.get_default_z_axis().set_title("Z").set_interval(10, 80, stop_axis_after=True)

# # Open the dashboard in live mode
# dashboard.open(live=True)

# # Run the update function
# update_dashboard()









import lightningchart as lc
import pandas as pd
import numpy as np
import trimesh
import time

# Set the LightningChart license
lc.set_license(open('../license-key').read())

# Load the dataset
file_path = 'Dataset/all_data_combined.csv'
sampling_interval = 4  # Sampling interval in milliseconds

# Define channel names as columns
channels = ["Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
            "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"]

# Load data with specified dtype and handle non-numeric values
df = pd.read_csv(file_path, header=None, names=channels, dtype=str)

# Convert all data to numeric, forcing errors to NaN
df[channels] = df[channels].apply(pd.to_numeric, errors='coerce')

# Replace NaNs with the mean of each channel
df[channels] = df[channels].apply(lambda x: x.fillna(x.mean()), axis=0)

# Generate a time axis in milliseconds and add it to the dataframe
df['time_ms'] = np.arange(len(df)) * sampling_interval

global_min_value = np.percentile(df[channels].values, 5)
global_max_value = np.percentile(df[channels].values, 95)

# Load and configure the 3D brain model
brain_model_path = 'Dataset/Brain/Brain_OBJ.obj'
brain_scene = trimesh.load(brain_model_path)
brain_mesh = brain_scene if isinstance(brain_scene, trimesh.Trimesh) else brain_scene.dump(concatenate=True)
brain_vertices = brain_mesh.vertices.flatten().tolist()
brain_indices = brain_mesh.faces.flatten().tolist()
brain_normals = brain_mesh.vertex_normals.flatten().tolist()

# Initialize the dashboard
dashboard = lc.Dashboard(columns=2, rows=1, theme=lc.Themes.Dark)

# Left side: EEG Channel Line Chart
chart_xy = dashboard.ChartXY(row_index=0, column_index=0, title="EEG Channel Activity Over Time")
chart_xy.get_default_x_axis().set_title("Time (ms)")
chart_xy.get_default_y_axis().dispose()  # Remove default y-axis

legend = chart_xy.add_legend()
channel_series = {}

# Add each channel as a separate line series with its own y-axis, based on min/max values of each channel
for i, channel in enumerate(channels):
    channel_min = df[channel].min() * 0.6
    channel_max = df[channel].max() * 0.6

    axis_y = chart_xy.add_y_axis(stack_index=i).set_tick_strategy("Empty")
    axis_y.set_title(channel).set_interval(channel_min, channel_max, stop_axis_after=True)
    series = chart_xy.add_line_series(y_axis=axis_y, data_pattern='ProgressiveXY')  # Ensures lines are connected in order
    series.set_name(channel)
    channel_series[channel] = series
    legend.add(series)

# Right side: 3D Brain Model with EEG Channels
chart_3d = dashboard.Chart3D(row_index=0, column_index=1, title="EEG Channel Visualization on 3D Brain Model")

# Add the brain model mesh
brain_model = chart_3d.add_mesh_model()
brain_model.set_model_geometry(vertices=brain_vertices, indices=brain_indices, normals=brain_normals)
brain_model.set_scale(0.02)
brain_model.set_model_location(0, 0, 40)
brain_model.set_color(lc.Color(200, 200, 200, 100))  # Semi-transparent brain color

# Define EEG channel positions on the brain
channel_positions = {
    "Fp1": [16, 11, 13], "Fp2": [-16, 11, 13], "F3": [19, 31, 19.1],
    "F4": [-19, 31, 19.1], "F7": [30, 17, 18.1], "F8": [-30, 17, 18.1],
    "T3": [47, 10, 35.4], "T4": [-47, 10, 35.4], "C3": [32, 37, 40],
    "C4": [-32, 37, 40], "T5": [33, 9, 60], "T6": [-33, 9, 60],
    "P3": [17.5, 28, 60], "P4": [-17.5, 28, 60], "O1": [9, 14, 65.5],
    "O2": [-9, 14, 65.5], "Fz": [0, 36, 23], "Cz": [0, 44, 42.4], "Pz": [0, 25, 62.2]
}

# Initialize series for each EEG channel point on the 3D brain model
channel_points = {}
for channel, pos in channel_positions.items():
    point_series = chart_3d.add_point_series()
    point_series.add({"x": pos[0], "y": pos[1], "z": pos[2]})
    point_series.set_point_size(15)
    channel_points[channel] = point_series

# Function to interpolate colors based on dynamic min/max values
def get_color_for_value(value, min_value=global_min_value, max_value=global_max_value):
    # Interpolates color based on EEG amplitude value (blue to red)
    color_ratio = max(0, min((value - min_value) / (max_value - min_value), 1))
    return lc.Color(
        int((1 - color_ratio) * 0 + color_ratio * 255),  # R
        int((1 - color_ratio) * 255 + color_ratio * 0),  # G
        int((1 - color_ratio) * 255 + color_ratio * 0)   # B
    )

# Update function to simulate real-time data streaming
def update_dashboard():
    # Iterate through each row (time point) in the dataset
    for idx, row in df.iterrows():
        time_ms = row['time_ms']

        # Update line chart for each channel
        for channel in channels:
            value = row[channel]
            channel_series[channel].add(time_ms, value)

        # Update 3D brain model channel colors based on the latest EEG values
        for channel, value in row[channels].items():
            color = get_color_for_value(value, min_value=global_min_value, max_value=global_max_value)
            channel_points[channel].set_point_color(color)
        
        brain_model.set_model_rotation(0, 1, 0)
        # Sleep for a short interval to simulate real-time update (e.g., 50 ms)
        time.sleep(0.05)

color=point_series.set_palette_point_colors(
    steps=[
        {'value': -16, 'color': lc.Color('red')},
        {'value': 0, 'color': lc.Color('green')},
        {'value': 16, 'color': lc.Color('blue')}
    ]
)

legend = chart_3d.add_legend().set_title("EEG Amplitude")
legend.add(color)

# Set axis titles and intervals for the 3D chart
x_axis = chart_3d.get_default_x_axis().set_title("X").set_interval(-70, 70, stop_axis_after=True)
y_axis = chart_3d.get_default_y_axis().set_title("Y").set_interval(-90, 70, stop_axis_after=True)
z_axis = chart_3d.get_default_z_axis().set_title("Z").set_interval(10, 80, stop_axis_after=True)

# Open the dashboard in live mode
dashboard.open(live=True)

# Run the update function
update_dashboard()





