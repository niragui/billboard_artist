import requests

from bisect import insort

from .chart_entry import ChartEntry
from .exceptions import ConnectionError

BASE_URL = "https://www.billboard.com/pmc-ajax/billboard-get-artist-chart/post-1479786/code-"

ITEMS_FIELD = "items"
CHART_FIELD = "title"


class ArtistWebsite():
    def __init__(self,
                 artist_id: str,
                 chart_id: str) -> None:
        self.chart_id = chart_id
        self.artist_id = artist_id

        self.entries = []

        data = self.get_web_json()
        self.load_entries(data)

    def get_url(self):
        """
        Create the ask URL for the artist & chart
        """
        chart_url = f"{BASE_URL}{self.chart_id}/"
        chart_url += f"artist-{self.artist_id}/"
        chart_url += "type-full/"

        return chart_url

    def get_web_json(self):
        """
        Get the json of the chart asked.
        """
        chart_url = self.get_url()

        artist_data = requests.get(chart_url)

        if artist_data.status_code // 100 != 2:
            raise ConnectionError(f"Couldn't Retrieve Artist Website [{artist_data.reason}]")

        artist_data = artist_data.json()

        return artist_data

    def load_entries(self,
                     json_data: dict):
        """
        Given the json from the website, it creates all the instances
        for each item.

        Parameters:
            - json_data: JSON data retrieved from the website
        """
        items = json_data[ITEMS_FIELD]

        self.entries = []

        for item in items:
            entry = ChartEntry(item)
            self.entries.append(entry)

    def create_json(self):
        """
        Returns a readable json for for the given website
        """
        entries = []

        for entry in self.entries:
            entries.append(entry.create_json())

        return entries

    def __repr__(self) -> str:
        repr_str = ""

        entries = []

        for entry in self.entries:
            insort(entries, entry)

        top_10s = 0
        number_ones = 0
        weeks_one = 0

        for entry in entries[::-1]:
            repr_str += str(entry)
            repr_str += "\n"

            if entry.peak <= 10:
                top_10s += 1

            if entry.peak == 1:
                number_ones += 1
                weeks_one += entry.peak_weeks

        if len(entries) > 1:
            repr_str += "\n"
            repr_str += f"Total Entries: {len(entries)}\n"
            repr_str += f"Top 10s: {top_10s}\n"
            repr_str += f"Number Ones: {number_ones} [{weeks_one} Weeks]\n"

        return repr_str