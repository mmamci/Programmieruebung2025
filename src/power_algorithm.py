import pandas as pd
import plotly.express as px
import numpy as np


def convert_power_data(delta_time, power_data):
    power_data = pd.DataFrame(power_data)
    # Add a 'Seconds' column based on the index and delta_time
    power_data['Seconds'] = power_data.index * delta_time
    return power_data
    
powerdata = convert_power_data(1, pd.read_csv("data/activities/activity.csv")["PowerOriginal"])["PowerOriginal"]

timewindows = [2,5,10,30,1*60, 2*60, 5*60, 10*60, 20*60, 60*60,2*60*60]

result = []

result.append([powerdata.max(), 1]) 

for timewindow in timewindows:
    slices = []
    for i in range(0, len(powerdata)-timewindow):
        slices.append(powerdata[i:i+timewindow].mean())
    
    if len(slices) != 0:
        result.append([slices[np.argmax(slices)], timewindow])



fig = px.line(
    x=[x[1] for x in result],
    y=[x[0] for x in result],
    labels={'x': 'Time Window (s)', 'y': 'Max Mean Power'}
)
fig.update_xaxes(type="log")

fig.write_html("power_plot.html", auto_open=True)
