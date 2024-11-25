import pandas as pd
import numpy as np
import lightningchart as lc

lc.set_license('my-license-key')

channel_names = [
    "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
    "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
]

file_path = 'Dataset/all_data_combined.csv'

data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce').dropna()

chart = lc.ChartXY(
    theme=lc.Themes.Light,
    title="Box Plot of Amplitude Distribution by Channel"
)

x_axis = chart.get_default_x_axis()
x_axis.set_title("EEG Channels")
x_axis.set_tick_strategy('Empty')

dataset = []
x_values_outlier = []
y_values_outlier = []
gap = 3 

for i, channel in enumerate(channel_names):
    column_data = data[channel].values

    start = i * gap
    end = start + 1

    lower_quartile = float(np.percentile(column_data, 25))
    upper_quartile = float(np.percentile(column_data, 75))
    median = float(np.median(column_data))
    lower_extreme = float(np.min(column_data))
    upper_extreme = float(np.max(column_data))

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

    custom_tick = x_axis.add_custom_tick()
    custom_tick.set_value((start + end) / 2)
    custom_tick.set_text(channel)

    iqr = upper_quartile - lower_quartile
    lower_bound = lower_quartile - 1.5 * iqr
    upper_bound = upper_quartile + 1.5 * iqr
    outliers = [y for y in column_data if y < lower_bound or y > upper_bound]

    for outlier in outliers:
        x_values_outlier.append((start + end) / 2)
        y_values_outlier.append(outlier)

box_series = chart.add_box_series()
box_series.add_multiple(dataset)

outlier_series = chart.add_point_series(
    sizes=True,
    rotations=True,
    lookup_values=True
)
outlier_series.set_point_color(lc.Color('red'))
outlier_series.append_samples(
    x_values=x_values_outlier,
    y_values=y_values_outlier,
    sizes=[3] * len(y_values_outlier)
)

chart.get_default_y_axis().set_title("Amplitude")

chart.open()
