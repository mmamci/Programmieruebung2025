import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ActivityData:
    def __init__(self):
        self.dataframe = pd.read_csv("data/activities/activity.csv")
        
    def print_key_values(self):
        self.dataframe.index

        self.dataframe["HeartRate"].min()
        self.dataframe["HeartRate"].max()
        self.dataframe["HeartRate"].mean()
        df_statistics = self.dataframe[["HeartRate" , "PowerOriginal"]].describe()
        df_statistics

        self.dataframe["PowerOriginal"].mean()
        self.dataframe["PowerOriginal"].max()

        self.dataframe["PowerOriginal"].plot()

        # Wie lange mehr als 300 Watt?

        self.dataframe["PowerOriginal"] > 300

        self.dataframe["High Power"] = self.dataframe["PowerOriginal"] > 300
        self.dataframe["High Power"].sum()
        self.dataframe["High Power"].value_counts()

        self.dataframe["Zone"] = None

        hr_max = self.dataframe["HeartRate"].max()
        hr_max

untergrenzen_zonen = {}

zone = 1
for faktor in range(50, 100, 10):

    untergrenzen_zonen[f"Zone {zone}"] = float(hr_max * faktor/100)
    zone = zone + 1

untergrenzen_zonen

# Füge eine neue Splate Zone hinzu, die die Zone basierend auf der Herzfrequenz angibt

list_zone = []

self.dataframe["Zone"] = None

for index, row in self.dataframe.iterrows():
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

self.dataframe["Zone"] = list_zone   
self.dataframe["Zone"].value_counts()

df_groups = self.dataframe.groupby("Zone").mean()
df_groups[["HeartRate", "PowerOriginal"]]

def Zeit_Leistung_pro_Zone():

    zeit_pro_zone = self.dataframe.groupby("Zone").agg(
        Zeit_Sekunden=("Zone", "count"),  # Zählt die Zeilen pro Zone
        Durchschnittliche_Leistung =("PowerOriginal", "mean")  # Durchschnitt von PowerOriginal
    ).reset_index()

    zeit_pro_zone["Zeit in Minuten"] = zeit_pro_zone["Zeit_Sekunden"] / 60

    # Zeige das Ergebnis
    zeit_pro_zone[["Zone", "Zeit in Minuten", "Durchschnittliche_Leistung"]]


def erstelle_plot():

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    default_colors = [
        "gray", "#B2DFEE", "#A2CD5A", "#EEE8AA", "#FF8247", "#CD3700",
    ]
    # Alle Zonen erkennen & Farben automatisch zuordnen
    unique_zones = sorted(self.dataframe["Zone"].fillna("Zone 0").unique())
    zone_colors = {
        zone: default_colors[i % len(default_colors)]
        for i, zone in enumerate(unique_zones)
    }


    # Power 
    fig.add_trace(
        go.Scatter(
            x=self.dataframe.index,
            y=self.dataframe["PowerOriginal"],
            name="Power (W)",
            line=dict(color="#4169E1"),
        ),
        secondary_y=False,
    )

    # Herzfrequenz in Segmenten zeichnen
    for i in range(len(self.dataframe) - 1):
        zone = self.dataframe["Zone"].iloc[i]
        x_vals = [self.dataframe.index[i], self.dataframe.index[i + 1]]
        y_vals = [self.dataframe["HeartRate"].iloc[i], self.dataframe["HeartRate"].iloc[i + 1]]
    
        fig.add_trace(
            go.Scatter(
                x = x_vals,
                y = y_vals,
                mode = "lines",
                line = dict(color=zone_colors.get(zone, "black"), width=2),
                showlegend = False,
                yaxis = "y2"
            )
        )

    # Farblegende erzeugen
    for zone_name, color in zone_colors.items():
        fig.add_trace(
            go.Scatter(
                x = [None], y = [None],
                mode = "lines",
                line = dict(color=color, width=2),
                name = zone_name
            )
        )

    # Achsen-Einstellungen
    hr_min = self.dataframe["HeartRate"].min()
    hr_max = self.dataframe["HeartRate"].max()

    fig.update_layout(
        xaxis_title = "Zeit",
        yaxis_title = "Watt",
        yaxis2 = dict(
            title = "Herzfrequenz",
            overlaying = "y",
            side = "right",
        ),

        width = 700,
        height = 500,
        legend = dict(orientation="v", x=1.1, y=1)
    )

    fig.show()
