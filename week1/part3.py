import pandas as pd

tracks = pd.read_json("files/Tracks.json")
track_details = pd.read_csv("files/TracksDetail.csv")

print("\n - - - - - Part 3.1 - - - - - \n")

print(tracks.value_counts(subset='artist'))

print("\n - - - - - Part 3.2 - - - - - \n")

albums = tracks.value_counts(subset='album')

print(albums[albums > 5])

print("\n - - - - - Part 3.3 - - - - - \n")

track_details = track_details.iloc[: , 1:]
track_details = track_details.drop(columns=["artistName", "trackName"])
track_details = track_details.rename(columns={"albumName": "track"})

merged = tracks.merge(track_details, how='inner', on='track')

print(merged)

print("\n - - - - - Part 3.4 - - - - - \n")

genres_dict = dict()
for genres in merged['genres']:
    for genre in eval(genres):

        if genre in genres_dict:
            genres_dict[genre] += 1
        else:
            genres_dict[genre] = 1

print(sorted(genres_dict.items(), key=lambda x:x[1], reverse=True)[0:10])
print(merged[merged["genres"].str.contains("electropop")]["track"])
print(merged[merged["artist"].str.contains("Matisyahu")]["track"])
