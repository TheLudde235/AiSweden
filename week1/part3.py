import pandas as pd

tracks = pd.read_json("files/Tracks.json")
track_details = pd.read_csv("files/TracksDetail.csv")


# Part 1
print(tracks.value_counts(subset='artist'))

# Part 2
albums = tracks.value_counts(subset='album')

print(albums[albums > 5])

# Part 3

track_details = track_details.iloc[: , 1:]
track_details = track_details.drop(columns=["artistName", "trackName"])
track_details = track_details.rename(columns={"albumName": "track"})

merged = tracks.merge(track_details, how='inner', on='track')

print(merged)

# Part 4

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
