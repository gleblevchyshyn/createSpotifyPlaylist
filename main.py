from bs4 import BeautifulSoup
import requests
import spotipy

CLIENT_ID = "your_id"
CLIENT_SECRET = "your_secret"
REDIRECT_URI = 'http://example.com'

oauth = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    redirect_uri=REDIRECT_URI,
                                    scope="playlist-modify-private",
                                    show_dialog=True,
                                    cache_path="token.txt"
                                    )

sp = spotipy.Spotify(auth_manager=oauth)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type date in this format YYYY-MM-DD:")
request = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
request.raise_for_status()
text = request.text

soup = BeautifulSoup(text, "html.parser")

song_names_headers = soup.find_all("h3", class_="a-no-trucate")
song_names = [song.getText().strip() for song in song_names_headers]

year = date.split('-')[0]
songs = []
for song in song_names:
    try:
        searched = sp.search(q={"name": song,
                                "year": year}, type="track")
        songs.append(searched["tracks"]["items"][0]["uri"])
        print(song)
    except IndexError:
        print(f"The song {song} is not found!")

playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{date} Billboard 100",
                                   public=False)

sp.playlist_add_items(playlist_id=playlist["id"],
                      items=songs
                      )
