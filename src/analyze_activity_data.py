import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ActivityData:
    def __init__(self, path = "data/activities/activity.csv"):
        self.dataframe = pd.read_csv(path)

        # self.print_key_values()
        self.define_zones()
   
    def print_key_values(self):
        print(self.dataframe.index)

        print(self.dataframe["HeartRate"].min())
        print(self.dataframe["HeartRate"].max())
        print(self.dataframe["HeartRate"].mean())
        df_statistics = self.dataframe[["HeartRate" , "PowerOriginal"]].describe()
        print(df_statistics)

        print(self.dataframe["PowerOriginal"].mean())
        print(self.dataframe["PowerOriginal"].max())

        print(self.dataframe["PowerOriginal"].plot())

        print(self.dataframe["PowerOriginal"] > 300)

        self.dataframe["High Power"] = self.dataframe["PowerOriginal"] > 300
        print(self.dataframe["High Power"].sum())
        print(self.dataframe["High Power"].value_counts())

        self.dataframe["Zone"] = None

        print(self.dataframe["HeartRate"].max())

    def define_zones(self, heartrate_max = None):
        untergrenzen_zonen = {}

        if heartrate_max == None:
            heartrate_max = self.dataframe["HeartRate"].max()
        else:
            heartrate_max = int(heartrate_max)
        
        zone = 1
        for faktor in range(50, 100, 10):
        
            untergrenzen_zonen[f"Zone {zone}"] = float(heartrate_max * faktor/100)
            zone = zone + 1

        untergrenzen_zonen

        # Füge eine neue Splate Zone hinzu, die die Zone basierend auf der Herzfrequenz angibt
        list_zone = []

        self.dataframe["Zone"] = None

        for index, row in self.dataframe.iterrows():
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

        self.zeit_pro_zone = self.dataframe.groupby("Zone").agg(
        Zeit_Sekunden=("Zone", "count"),  # Zählt die Zeilen pro Zone
        Durchschnittliche_Leistung =("PowerOriginal", "mean")  # Durchschnitt von PowerOriginal
        ).reset_index()

        self.zeit_pro_zone["Zeit in Minuten"] = self.zeit_pro_zone["Zeit_Sekunden"] / 60

        # Zeige das Ergebnis
        self.zeit_pro_zone[["Zone", "Zeit in Minuten", "Durchschnittliche_Leistung"]]

    def get_Zeitleistung_pro_Zone(self):
        self.zeit_pro_zone = self.dataframe.groupby("Zone").agg(
            Zeit_Sekunden=("Zone", "count"),  # Zählt die Zeilen pro Zone
            Durchschnittliche_Leistung =("PowerOriginal", "mean")  # Durchschnitt von PowerOriginal
            ).reset_index()

        self.zeit_pro_zone["Zeit in Minuten"] = self.zeit_pro_zone["Zeit_Sekunden"] / 60

        return self.zeit_pro_zone[["Zone", "Zeit in Minuten", "Durchschnittliche_Leistung"]].round(2)
    
    # Julians verbesserung
    def create_plot(self):
        self.plot = ActivityPlot(self.)

class ActivityPlot:
    def __init__(self, activity_data):
        self.activity_data = activity_data

        self.fig = make_subplots(specs=[[{"secondary_y": True}]])

        
    def add_traces(self):
        self.fig.add_trace(
            go.Scatter(
                x=self.activity_data.index,
                y=self.activity_data["PowerOriginal"],
                name="Power (W)",
                line=dict(color="#4169E1"),
            ),
            secondary_y=False,
        )
    
    def zone_colors(self):
        self.default_colors = [
            "gray", "#B2DFEE", "#A2CD5A", "#EEE8AA", "#FF8247", "#CD3700",
        ]
        
        # Alle Zonen erkennen & Farben automatisch zuordnen
        unique_zones = sorted(self.activity_data["Zone"].fillna("Zone 0").unique())
        self.zone_colors = {
            zone: self.default_colors[i % len(self.default_colors)]
            for i, zone in enumerate(unique_zones)
        }
    
    def divide_traces(self):
        for i in range(len(self.activity_data) - 1):
            zone = self.activity_data["Zone"].iloc[i]
            x_vals = [self.activity_data.index[i], self.activity_data.index[i + 1]]
            y_vals = [self.activity_data["HeartRate"].iloc[i], self.activity_data["HeartRate"].iloc[i + 1]]

            self.fig.add_trace(
                go.Scatter(
                    x = x_vals,
                    y = y_vals,
                    mode = "lines",
                    line = dict(color=self.zone_colors.get(zone, "black"), width=2),
                    showlegend = False,
                    yaxis = "y2"
                )
            )

    def create_legend(self):
            # Farblegende erzeugen
        for zone_name, color in self.zone_colors.items():
            self.fig.add_trace(
                go.Scatter(
                    x = [None], y = [None],
                    mode = "lines",
                    line = dict(color=color, width=2),
                    name = zone_name
                )
        )
        
    def create_axis(self):
        # Achsen-Einstellungen
        hr_min = self.activity_data["HeartRate"].min()
        hr_max = self.activity_data["HeartRate"].max()

        self.fig.update_layout(
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

        self.fig.update_layout(
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

    def create_plot(self):
        self.add_traces()
        self.zone_colors()
        self.divide_traces()
        self.create_legend()
        self.create_axis()

        return self.fig