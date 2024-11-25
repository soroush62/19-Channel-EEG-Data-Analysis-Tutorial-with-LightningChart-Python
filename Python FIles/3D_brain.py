import lightningchart as lc
import pandas as pd
import numpy as np
import trimesh
import time

lc.set_license('my-license-key')

file_path = 'Dataset/all_data_combined.csv'
sampling_interval = 4

channels = ["Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
            "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"]

df = pd.read_csv(file_path, header=None, names=channels, dtype=str)

df[channels] = df[channels].apply(pd.to_numeric, errors='coerce')

df[channels] = df[channels].apply(lambda x: x.fillna(x.mean()), axis=0)

df['time_ms'] = np.arange(len(df)) * sampling_interval

global_min_value = np.percentile(df[channels].values, 5)
global_max_value = np.percentile(df[channels].values, 95)

brain_model_path = 'Dataset/Brain/Brain_OBJ.obj'
brain_scene = trimesh.load(brain_model_path)
brain_mesh = brain_scene if isinstance(brain_scene, trimesh.Trimesh) else brain_scene.dump(concatenate=True)
brain_vertices = brain_mesh.vertices.flatten().tolist()
brain_indices = brain_mesh.faces.flatten().tolist()
brain_normals = brain_mesh.vertex_normals.flatten().tolist()

dashboard = lc.Dashboard(columns=2, rows=1, theme=lc.Themes.Dark)

chart_xy = dashboard.ChartXY(row_index=0, column_index=0, title="EEG Channel Activity Over Time")
chart_xy.get_default_x_axis().set_title("Time (ms)")
chart_xy.get_default_y_axis().dispose()

legend = chart_xy.add_legend()
channel_series = {}

for i, channel in enumerate(channels):
    channel_min = df[channel].min() * 0.6
    channel_max = df[channel].max() * 0.6

    axis_y = chart_xy.add_y_axis(stack_index=i).set_tick_strategy("Empty")
    axis_y.set_title(channel).set_interval(channel_min, channel_max, stop_axis_after=True)
    series = chart_xy.add_line_series(y_axis=axis_y, data_pattern='ProgressiveXY') 
    series.set_name(channel)
    channel_series[channel] = series
    legend.add(series)

chart_3d = dashboard.Chart3D(row_index=0, column_index=1, title="EEG Channel Visualization on 3D Brain Model")

brain_model = chart_3d.add_mesh_model()
brain_model.set_model_geometry(vertices=brain_vertices, indices=brain_indices, normals=brain_normals)
brain_model.set_scale(0.02)
brain_model.set_model_location(0, 0, 40)
brain_model.set_color(lc.Color(200, 200, 200, 100))

channel_positions = {
    "Fp1": [16, 11, 13], "Fp2": [-16, 11, 13], "F3": [19, 31, 19.1],
    "F4": [-19, 31, 19.1], "F7": [30, 17, 18.1], "F8": [-30, 17, 18.1],
    "T3": [47, 10, 35.4], "T4": [-47, 10, 35.4], "C3": [32, 37, 40],
    "C4": [-32, 37, 40], "T5": [33, 9, 60], "T6": [-33, 9, 60],
    "P3": [17.5, 28, 60], "P4": [-17.5, 28, 60], "O1": [9, 14, 65.5],
    "O2": [-9, 14, 65.5], "Fz": [0, 36, 23], "Cz": [0, 44, 42.4], "Pz": [0, 25, 62.2]
}

channel_points = {}
for channel, pos in channel_positions.items():
    point_series = chart_3d.add_point_series()
    point_series.add({"x": pos[0], "y": pos[1], "z": pos[2]})
    point_series.set_point_size(15)
    channel_points[channel] = point_series

def get_color_for_value(value, min_value=global_min_value, max_value=global_max_value):
    color_ratio = max(0, min((value - min_value) / (max_value - min_value), 1))
    return lc.Color(
        int((1 - color_ratio) * 0 + color_ratio * 255),  # R
        int((1 - color_ratio) * 255 + color_ratio * 0),  # G
        int((1 - color_ratio) * 255 + color_ratio * 0)   # B
    )

def update_dashboard():
    for idx, row in df.iterrows():
        time_ms = row['time_ms']

        for channel in channels:
            value = row[channel]
            channel_series[channel].add(time_ms, value)

        for channel, value in row[channels].items():
            color = get_color_for_value(value, min_value=global_min_value, max_value=global_max_value)
            channel_points[channel].set_point_color(color)
        
        brain_model.set_model_rotation(0, 1, 0)
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

x_axis = chart_3d.get_default_x_axis().set_title("X").set_interval(-70, 70, stop_axis_after=True)
y_axis = chart_3d.get_default_y_axis().set_title("Y").set_interval(-90, 70, stop_axis_after=True)
z_axis = chart_3d.get_default_z_axis().set_title("Z").set_interval(10, 80, stop_axis_after=True)

dashboard.open(live=True)

update_dashboard()





