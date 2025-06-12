import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

import matplotlib.pyplot as plt


# Implementiert einen anderen Algorithmus. Wir haben darüber am 12.06. 2025. im Unterricht gesprochen.

def convert_power_data(delta_time, power_data):
    power_data = pd.DataFrame(power_data)
    # Add a 'Seconds' column based on the index and delta_time
    power_data['Seconds'] = power_data.index * delta_time
    return power_data
    
powerdata = convert_power_data(1, pd.read_csv("data/activities/activity.csv")["PowerOriginal"])["PowerOriginal"]

timewindows = [2,5,10,30,1*60, 2*60, 5*60, 10*60, 20*60, 30*60]

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
    labels={'x': 'Zeit in Sekunden', 'y': 'Leistung in Watt'},
)

fig.add_trace(go.Line(
    x=[x[1] for x in result],
    y=[x[0] for x in result],
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(128, 128, 128, 0.3)',
    showlegend=False,
))

fig.update_traces(line=dict(color="#8B0000", width=2))



fig.update_xaxes(
    type="linear"
)

fig.update_layout(template="plotly_white")

fig.update_yaxes(range=[180, 440])

fig.write_html("power_plot.html", auto_open=True)