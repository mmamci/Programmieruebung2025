# %%
import pandas as pd
import plotly.express as px


def find_peaks(ekg, threshold = 340):
    df = pd.read_csv(ekg.result, sep = "	")

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



df = find_peaks()
fig = px.line(df, x="Time in ms", y = "Voltage in mV", title = "EKG Data with Detected Peaks")
fig.add_scatter(x = df[df["is_peak"]]["Time in ms"], y = df[df["is_peak"]]["Voltage in mV"], mode = "markers", name = "Peaks", marker=dict(color="red", size=5))
fig.show()
