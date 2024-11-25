import pandas as pd
import numpy as np
from scipy.signal import welch
import lightningchart as lc

lc.set_license('my-license-key')

channel_names = [
    "Fp1", "Fp2", "F3", "F4", "F7", "F8", "T3", "T4", "C3", "C4", 
    "T5", "T6", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"
]

file_path = 'Dataset/all_data_combined.csv'

data = pd.read_csv(file_path, header=None, names=channel_names, sep=',', dtype=str, low_memory=False)
data = data.apply(pd.to_numeric, errors='coerce').dropna()

chart = lc.ChartXY()
chart.set_title("Power Spectral Density (PSD) of EEG Channels")
chart.get_default_y_axis().set_title("Log(Power Spectral Density) (log(uV^2/Hz))")
chart.get_default_x_axis().set_title("Frequency (Hz)")

fs = 256
legend = chart.add_legend()
for channel in channel_names:
    
    freqs, psd = welch(data[channel], fs=fs, nperseg=512)
    
    log_psd = np.log10(psd + 1e-10)  

    line_series = chart.add_line_series()
    line_series.set_name(channel)
    legend.add(line_series)
    
    for f, p in zip(freqs, log_psd):
        line_series.add(f, p)

chart.open()
