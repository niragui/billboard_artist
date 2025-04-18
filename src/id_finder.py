from typing import Optional

import os

import requests

import json

from .exceptions import FileError, MissingArtist, ConnectionError
from .utils import standarize_name, parse_name_for_request
from .constants import BASE_ARTIST_URL

ARTIST_ID_HEADER = "data-artist-id"

THIS_FOLDER = os.path.dirname(__file__)

ARTISTS_FILE = os.path.join(THIS_FOLDER, "artists.json")


class ArtistIdFinder():
    def __init__(self,
                 file: Optional[str] = ARTISTS_FILE) -> None:
        self.file = file
        if file is None:
            self.artists = {}
        elif not os.path.isfile(file):
            self.artists = {}
        else:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    self.artists = json.load(f)
            except json.JSONDecodeError:
                raise FileError(f"Could Not Read JSON Data From File [{file}]")

            if not isinstance(self.artists, dict):
                raise FileError(f"JSON file must have a dict stored [{file}]")

    def update_file(self):
        """
        Update the storing file with the new ids
        """
        if self.file is None:
            return

        with open(self.file, "w") as f:
            f.write(json.dumps(self.artists, indent=4))


    def get_artist_url(self,
                       artist: str):
        """
        Generates the URL of the artist asked

        Parameters:
            - artist: Artist to get the website url from
        """
        parsed_name = parse_name_for_request(artist)

        artist_url = f"{BASE_ARTIST_URL}{parsed_name}"

        return artist_url

    def get_artist_wb_content(self,
                              artist: str):
        """
        Requests the Billboard Artist Website to retrieve the artist data

        Parameters:
            - artist: Name of the artist to ask for
        """
        artist_url = self.get_artist_url(artist)

        artist_data = requests.get(artist_url)

        if artist_data.status_code // 100 != 2:
            raise ConnectionError(f"Error Reading Artist Website [{artist_data.reason}]")

        return artist_data.content.decode("utf-8")

    def read_id_from_content(self,
                             artist_content: str):
        """
        Given an artist content from its website, it reads
        the artist id stored in it.

        Parameters:
            - artist_content: Content found in the artist website
        """
        artist_id = None

        for line in artist_content.split("\n"):
            start = line.find(ARTIST_ID_HEADER)

            if start < 0:
                continue

            real_start = line.find("\"", start) + 1
            end = line.find("\"", real_start)

            artist_id = line[real_start: end]

        return artist_id

    def read_artist_id(self,
                       artist: str):
        """
        Requests the Billboard Artist Website to retrueve the artist id

        Parameters:
            - artist: Name of the artist to ask for
        """
        try:
            artist_content = self.get_artist_wb_content(artist)
        except ConnectionError:
            return

        artist_id = self.read_id_from_content(artist_content)

        if artist_id is None:
            return

        self.artists[artist] = artist_id

        self.update_file()

    def get_artist(self,
                   artist: str):
        """
        Returns the billboard id for an asked artist

        Parameters:
            - artist: Artist to check for
        """
        std_artist = standarize_name(artist)
        artist_id = self.artists.get(std_artist, None)

        if artist_id is None:
            self.read_artist_id(std_artist)
        else:
            return artist_id

        artist_id = self.artists.get(std_artist, None)
        if artist_id is None:
            raise MissingArtist(f"Artist Not Present In BB Chart History DB [{artist}]")

        return artist_id

    def __getitem__(self,
                    artist: str):
        return self.get_artist(artist)