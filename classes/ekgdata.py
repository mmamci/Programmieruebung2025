import json
import pandas as pd

import plotly.express as px

class EKGData:
    def __init__ (self, id: int, date: str, result_link: str):
        self.id = id
        self.date = date
        self.result_link = result_link

    @staticmethod
    def load_by_id(id):
        with open("data/person_db.json", "r", encoding="utf-8") as file:
            for person in json.load(file):
                for ekg in person["ekg_tests"]:
                    if ekg["id"] == id:
                        return EKGData(
                            ekg["id"],
                            ekg["date"],
                            ekg["result_link"]
                        )

    def find_peaks(self, threshold = 340):
        df = pd.read_csv(self.result_link, sep = "	")

        df.columns = ["Voltage in mV", "Time in ms"]
        df["is_peak"] = None



        df = df.iloc[0 : 5000]
        list_of_peaks = []

        for index, row in df.iterrows():
            if index == df.index.max():
                break

            current_value = row["Voltage in mV"]
            #print("current value: ", current_value)

         # ist der current_value größer als Vorgänger und Nachfolger
            if current_value > df.iloc[index - 1]["Voltage in mV"] and current_value >= df.iloc[index + 1]["Voltage in mV"]:


                if current_value > threshold:
                    list_of_peaks.append(index)

        df["is_peak"] = False
        df.loc[list_of_peaks, "is_peak"] = True
        df["is_peak"].value_counts()

        return df

    def plot_time_series(self):
        df = EKGData.load_by_id(2).find_peaks()
        fig = px.line(df, x="Time in ms", y="Voltage in mV", title="EKG Data with Detected Peaks")
        fig.add_scatter(
            x=df[df["is_peak"]]["Time in ms"],
            y=df[df["is_peak"]]["Voltage in mV"],
            mode="markers",
            name="Peaks",
            marker=dict(color="red", size=5)
        )
        fig.show(renderer="browser")

    def calculate_heartrate(self, threshold=340):
        df = self.find_peaks(threshold)
        peak_times = df[df["is_peak"]]["Time in ms"].values

        if len(peak_times) < 2:
            return 0 
        
        rr_intervals = (peak_times[1:] - peak_times[:-1]) / 1000.0

        if len(rr_intervals) == 0 or rr_intervals.mean() == 0:
            return 0

        heartrate = 60 / rr_intervals.mean()
        return heartrate
    



