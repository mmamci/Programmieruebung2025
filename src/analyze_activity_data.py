#%% Zelle 1
import pandas as pd

dataframe = pd.read_csv("../data/activities/activity.csv")
dataframe.index

# %%

dataframe["HeartRate"].min()
dataframe["HeartRate"].max()
dataframe["HeartRate"].mean()
df_statistics = dataframe[["HeartRate" , "PowerOriginal"]].describe()
df_statistics

# %%

dataframe["PowerOriginal"].mean()
dataframe["PowerOriginal"].max()

#%%

dataframe["PowerOriginal"].plot()

# %% Wie lange mehr als 300 Watt?

dataframe["PowerOriginal"] > 300

dataframe["High Power"] = dataframe["PowerOriginal"] > 300
dataframe["High Power"].sum()
dataframe["High Power"].value_counts()

#%%
dataframe["Zone"] = None

hr_max = dataframe["HeartRate"].max()
hr_max

# %%

untergrenzen_zonen = {}

zone = 1
for faktor in range(50, 100, 10):

    untergrenzen_zonen[f"Zone {zone}"] = float(hr_max * faktor/100)
    zone = zone + 1

untergrenzen_zonen

# %% Füge eine neue Splate Zone hinzu, die die Zone basierend auf der Herzfrequenz angibt

list_zone = []

dataframe["Zone"] = None

for index, row in dataframe.iterrows():
    #print(row["HeartRate"])
    current_hr = row["HeartRate"]

    if current_hr >= untergrenzen_zonen["Zone 5"]:
        list_zone.append("Zone 5")
    elif current_hr >= untergrenzen_zonen["Zone 4"]:
        list_zone.append("Zone 4")
    elif current_hr >= untergrenzen_zonen["Zone 3"]:
        list_zone.append("Zone 3")
    elif current_hr >= untergrenzen_zonen["Zone 2"]:
        list_zone.append("Zone 2")
    elif current_hr >= untergrenzen_zonen["Zone 1"]:
        list_zone.append("Zone 1")
    else:
        list_zone.append("Zone 0")

dataframe["Zone"] = list_zone   
dataframe["Zone"].value_counts()


# %%

df_groups = dataframe.groupby("Zone").mean()
df_groups[["HeartRate", "PowerOriginal"]]

# %%

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x = dataframe.index, y = dataframe["PowerOriginal"], name = "Power (W)", line = dict(color="blue")),
    secondary_y=False, 
)

fig.add_trace(
    go.Scatter(x = dataframe.index, y = dataframe["HeartRate"], name = "Herzfrequenz", line = dict(color = "red")), 
    secondary_y = True,
)

fig.update_layout(
    xaxis_title = "Zeit",
    yaxis_title = "Watt",
    yaxis2_title = "Herzfrequenz",
    width = 800,
    height = 800,
)

fig.show()
#fig = px.line(dataframe, y = "HeartRate")




# %%
