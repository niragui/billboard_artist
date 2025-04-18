
from .charts_parser import ChartParser
from .id_finder import ArtistIdFinder
from .artist_website import ArtistWebsite
from .exceptions import MissingChart
from .utils import parse_name_for_request
from .constants import BASE_ARTIST_URL


class ArchiveChecker():
    def __init__(self) -> None:
        self.id_parser = ArtistIdFinder()
        self.chart_parser = ChartParser()

    def check_artist(self,
                     artist: str,
                     chart: str):
        """
        Get an artist website object loaded

        Parameters:
            - artist: Artist to ask for
            - chart: Chart to ask for
        """
        artist_id = self.id_parser.get_artist(artist)

        try:
            chart_id = self.chart_parser.get_chart_id(chart)
        except MissingChart as e:
            if not self.chart_parser.is_saved_id(chart.upper()):
                raise e
            else:
                chart_id = chart.upper()

        website = ArtistWebsite(artist_id, chart_id)

        return website

    def get_archive_url(self,
                        artist: str,
                        chart: str):
        """
        Get an artist website url loaded

        Parameters:
            - artist: Artist to ask for
            - chart: Chart to ask for
        """
        try:
            chart_id = self.chart_parser.get_chart_id(chart)
        except MissingChart as e:
            if not self.chart_parser.is_saved_id(chart.upper()):
                raise e
            else:
                chart_id = chart.upper()

        artist_url = parse_name_for_request(artist)

        url = f"{BASE_ARTIST_URL}{artist_url}/chart-history/{chart_id}"

        return url
