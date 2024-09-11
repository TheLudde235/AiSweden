import json
from numpy import nan
import pandas as pd
from pandas._libs.sparse import IntIndex

df = pd.DataFrame()

file = 0

if file == 0:
    df = pd.read_csv("files/housedata.csv")
else:
    try:
        df = pd.read_csv("output/housedata2024.csv")
    except:
        print("Have you ran part1.py yet?")

missing_size_arr = df.loc[df["Size"] == "?"].to_numpy()
missing_room_arr = df.loc[df["Room"] == "?"].to_numpy()

size_dict = {}
room_dict = {}

for broken in missing_size_arr:
    df2 = df.loc[(df["name"] == broken[0]) & (df["Size"] != "?")]

    for index, arr in df2.iterrows():
        size_dict[arr["name"].upper()] = arr["Size"] # To uppercase in case of wierd capitalization

for broken in missing_room_arr:
    df2 = df.loc[(df["name"] == broken[0]) & (df["Room"] != "?")]

    for index, arr in df2.iterrows():
        room_dict[arr["name"].upper()] = arr["Room"] # To uppercase in case of wierd capitalization

df_copy = df

for i in range(len(df)):
    if df["Size"][i] == "?":
        if str(df["name"][i]).upper() in size_dict:
            df_copy.loc[i, "Size"] = size_dict[str(df["name"][i]).upper()]
        else:
            df_copy = df_copy.drop(i)

    if df["Room"][i] == "?":
        if str(df["name"][i]).upper() in room_dict:
            df_copy.loc[i, "Room"] = room_dict[str(df["name"][i]).upper()]
        else:
            df_copy = df_copy.drop(i)

for i, row in df_copy.iterrows():
    if int(df_copy["Room"][i]) > int(df_copy["Size"][i]):
        x = df_copy["Room"][i]
        df_copy.loc[i, "Room"] = df_copy["Size"][i]
        df_copy.loc[i, "Size"] = x

    df_copy.loc[i, "KvMPrice"] = round(int(row["Endprice"]) / int(row["Size"]))

    df_copy.loc[i, "District"] = str(row["District"]).lower().capitalize().split('/')[0].split(',')[0]

df_copy.replace("?", 0, inplace=True)
df_copy.replace(nan, 0, inplace=True)

for index, row in df_copy.iterrows():

    match row["TypeOfProperty"]:

        case type if "rätt" in row["TypeOfProperty"].lower():
            df_copy.loc[index, "TypeOfProperty"] = "Bostadsrättslägenhet"

        case type if "par/rad/kedjehus" in row["TypeOfProperty"].lower():
            df_copy.loc[index, "TypeOfProperty"] = "Radhus"

        case type if "illa" in row["TypeOfProperty"].lower():
            df_copy.loc[index, "TypeOfProperty"] = "Villa"

        case type if "ård" in row["TypeOfProperty"].lower():
            df_copy.loc[index, "TypeOfProperty"] = "Gård"

        case type if "hus" in row["TypeOfProperty"].lower():
            df_copy.loc[index, "TypeOfProperty"] = "Fritidshus"

        case _:
            df_copy.loc[index, "TypeOfProperty"] = "Other"
if file == 0:
    df_copy.to_csv("files/housing_clean.csv", index=False)
else:
    df_copy.to_csv("files/housing_clean2024.csv", index=False)
