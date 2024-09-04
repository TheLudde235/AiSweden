import pandas as pd
import numpy as np

print(" - - - - - Part 2.1 - - - - - \n")

df = pd.read_csv("files/Dummytracks.csv", usecols=["populartySong", "artistName", "populartyArtist", "trackName"])
# df = pd.read_csv("Dummytracks.csv", header=0, usecols=["populartyArtist"])

popularitySong_arr = df["populartySong"].to_numpy()
artistName_arr = df["artistName"].to_numpy()
popularityArtist_arr = df["populartyArtist"].to_numpy()
trackName_arr = df["trackName"].to_numpy()

print("Song Popularity:", popularitySong_arr)
print("Artist Name:", artistName_arr)
print("Artist Popularity:", popularityArtist_arr)

print("\n - - - - - Part 2.2 - - - - - \n")

print("Artist:", round(popularityArtist_arr.mean()))
print("Song:", round(popularitySong_arr.mean()))

print("\n - - - - - Part 2.3 - - - - - \n")

rg_artists = set(artistName_arr[popularityArtist_arr >= 70])

for artist in rg_artists:
    print(artist)

print("\n - - - - - Part 2.4 - - - - - \n")

sum_rg_songs = 0
for i in range(len(popularitySong_arr)):
    if artistName_arr[i] in rg_artists and popularitySong_arr[i] >= 70:
        print('{}:'.format(trackName_arr[i]), popularitySong_arr[i])
        sum_rg_songs += 1

print("Amount of real good songs:", sum_rg_songs)

print("\n - - - - - Part 2.5 - - - - - \n")

rg_tracks = popularitySong_arr[popularityArtist_arr >= 70]
print("Popularity of tracks by real good artists:", rg_tracks)
print("Mean popularity of those tracks:", rg_tracks.mean())
print("Amount of tracks above 70 popularity score:", len(popularitySong_arr[popularitySong_arr > 70]))
