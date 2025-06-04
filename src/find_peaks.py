# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/ekg_data/01_Ruhe.txt", sep = "	")

df.columns = ["Voltage in mV", "Time in ms"]
df

# %%

df["is_peak"] = None
df

# %%
threshold = 340

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

print(list_of_peaks)


# %%

df["is_peak"] = False
df.loc[list_of_peaks, "is_peak"] = True
df["is_peak"].value_counts()

# %%

fig = px.line(df, x="Time in ms", y = "Voltage in mV", title = "EKG Data with Detected Peaks")
fig.add_scatter(x = df[df["is_peak"]]["Time in ms"], y = df[df["is_peak"]]["Voltage in mV"], mode = "markers", name = "Peaks", marker=dict(color="red", size=5))
fig.show()

# %%

def find_peaks(df, threshold):

    list_of_peaks = []

    for index, row in df.iterrows():
        if index == df.index.max():
            break

        current_value = row["Voltage in mV"]

 # ist der current_value größer als Vorgänger und Nachfolger
        if current_value > df.iloc[index - 1]["Voltage in mV"] and current_value >= df.iloc[index + 1]["Voltage in mV"]:


            if current_value > threshold:
                list_of_peaks.append(index)

    return list_of_peaks

df = pd.read_csv("../data/ekg_data/01_Ruhe.txt", sep = "	")
df.columns = ["Voltage in mV", "Time in ms"]
df

list_of_peaks = find_peaks(df, 350)

df["is_peak"] = False
df.loc[list_of_peaks, "is_peak"] = True
df["is_peak"].value_counts()

fig = px.line(df, x="Time in ms", y = "Voltage in mV", title = "EKG Data with Detected Peaks")
fig.add_scatter(x = df[df["is_peak"]]["Time in ms"], y = df[df["is_peak"]]["Voltage in mV"], mode = "markers", name = "Peaks", marker=dict(color="red", size=5))
fig.show()

# %%