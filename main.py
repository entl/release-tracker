from datetime import timedelta, datetime
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from art import tprint
from settings import CREDENTIALS
import warnings

warnings.filterwarnings("ignore")

class Client:
    
    def __init__(self, credentials: dict) -> None:
        self.credentials = credentials
        self.spotify = self.login()
        self.top_artists = self.get_user_top_artists()
        self.followed_artists = self.get_user_followed_artists()

    def login(self) -> Spotify:
        oauth = SpotifyOAuth(client_id=self.credentials["CLIENT_ID"], client_secret=self.credentials["CLIENT_SECRET"],
                            scope=self.credentials["SCOPE"], redirect_uri=self.credentials["REDIRECT_URI"])
        token = oauth.get_access_token()["access_token"]
        spotify = Spotify(auth=token)
        return spotify

    def get_user_top_artists(self) -> dict:
        top_long = self.spotify.current_user_top_artists(time_range="long_term", limit=100)
        top_medium = self.spotify.current_user_top_artists(time_range="medium_term", limit=100)
        top_short =  self.spotify.current_user_top_artists(time_range="short_term", limit=100)
        top = top_short | top_medium | top_long
        top_temp = {}
        for artist in top["items"]:
            top_temp.update({artist["name"]: artist["id"]})
        return top_temp

    def get_user_followed_artists(self) -> dict:
        followed_artists = self.spotify.current_user_followed_artists()
        followed_artists_formated = {}
        for artist in followed_artists["artists"]['items']:
            followed_artists_formated.update({artist["name"]: artist["id"]})

        return followed_artists_formated

    def get_releases(self, artists: dict, start: datetime) -> dict:
        for name, id_ in artists.items():
            artist_songs = self.spotify.artist_albums(artist_id=id_)
            for song in artist_songs["items"]:
                try:
                    date = datetime.strptime(song["release_date"], "%Y-%m-%d")
                    if start < date:
                        print(name+": "+song["name"]+" - "+song["release_date"]+" "+song["album_type"])
                except:
                    pass

    @staticmethod
    def get_time_period(delta: int) -> datetime:
        delta = timedelta(delta)
        start = datetime.today() - delta

        return start


def main():
    tprint("Release Tracker")
    while True:
        client = Client(credentials=CREDENTIALS)
        start = client.get_time_period(int(input("[+] Enter day period: ")))
        print("\n1. Releases from top artists\n2. Releases from followed artists\n3. Top and Followed\n4. Exit")
        choice = input("\n[+] Choose one: ")
        print("\n-----------------------------")
        match choice:
            case "1":
                client.get_releases(artists=client.top_artists, start=start)
            case "2":
                client.get_releases(artists=client.followed_artists, start=start)
            case "3":
                client.get_releases(artists=client.followed_artists|client.top_artists, start=start)
            case "4":
                exit(0)
        print("-----------------------------\n")
        
            
if __name__ == "__main__":
    main()
