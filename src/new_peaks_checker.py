import json

import os
import sys
from bisect import insort

from .exceptions import MissingChart, MissingArtist
from .archive_checker import ArchiveChecker

IMPORT_PATH = os.path.join(__file__, os.pardir, os.pardir, os.pardir)
sys.path.append(IMPORT_PATH)

from FileData.filereader import FileReader

from Billboard.billboardrecordcreator import BillboardRecordCreator

from Utils.artists import ArtistName

THIS_FOLDER = os.path.join(__file__, os.pardir)
FILES_FILE = os.path.join(THIS_FOLDER, "files.json")

CHECK_CHARTS = ["HSI"]


class NewPeaksChecker():
    def __init__(self,
                 chart: str):
        chart = chart.upper()
        chart_files = {}

        with open(FILES_FILE, "r") as f:
            chart_files = json.load(f)

        self.file = chart_files.get(chart)

        if self.file is None:
            raise MissingChart(f"Can't Find File For {chart}")

        self.chart = chart
        self.checker = ArchiveChecker()

    def get_reader(self):
        """
        Get A FileReader instance of the chart
        """
        creator = BillboardRecordCreator()

        reader = FileReader(self.file, creator)

        return reader

    def get_check_artists(self):
        """
        Get a list of the last artists in an asked chart

        Parameters:
            - chart: Chart to check for
        """
        reader = self.get_reader()

        last_date = reader.get_last_date_records()

        artists = []

        for record in last_date:
            rec_artists = record.artist_names
            rec_artists = ArtistName(rec_artists).get_most_accurate_separated()

            for artist in rec_artists:
                if artist not in artists:
                    artists.append(artist)
            
        artists.append("Ed Sheeran")
        artists.append("Miley Cyrus")

        return artists

    def loop_for_artists(self):
        """
        Check all artists charting last week for new peaks
        """
        artists = self.get_check_artists()

        reader = self.get_reader()
        last_date = reader.get_last_loaded_date()

        new_peaks = []

        for artist in artists:
            print(f"Checking {artist}")
            try:
                website = self.checker.check_artist(artist, self.chart)

                for entry in website.entries:
                    if entry.title.upper() == "NOKIA":
                        print(vars(entry))
                    if entry.peak_date > last_date:
                        insort(new_peaks, entry)
            except MissingArtist:
                continue

        return new_peaks