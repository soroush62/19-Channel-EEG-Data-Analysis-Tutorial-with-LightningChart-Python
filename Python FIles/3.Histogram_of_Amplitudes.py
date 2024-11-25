import pandas as pd
import numpy as np
import lightningchart as lc

lc.set_license('my-license-key')

channel_names = [
    "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
    "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
]

file_path = 'Dataset/all_data_combined.csv'

data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce').dropna()

dashboard = lc.Dashboard(rows=5, columns=4, theme=lc.Themes.Dark)

def create_histogram(column_data, channel_name, row_index, col_index):
 
    counts, bin_edges = np.histogram(column_data, bins=20)
    bar_data = [{'category': f'{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}', 'value': int(counts[i])} for i in range(len(counts))]

    chart = dashboard.BarChart(
        row_index=row_index,
        column_index=col_index
    )
    chart.set_title(f'Histogram of {channel_name}')
    
    chart.set_data(bar_data)

    chart.set_palette_colors(
        steps=[
            {'value': 0, 'color': lc.Color('blue')}, 
            {'value': 0.5, 'color': lc.Color('yellow')}, 
            {'value': 1, 'color': lc.Color('red')}  
        ],
        percentage_values=True 
    )

for i, channel in enumerate(channel_names):
    row_index = i // 4  #
    col_index = i % 4  
    
    create_histogram(data[channel].dropna(), channel, row_index, col_index)

dashboard.open()