
from .charts_parser import ChartParser
from .id_finder import ArtistIdFinder
from .artist_website import ArtistWebsite


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

        chart_id = self.chart_parser.get_chart_id(chart)

        website = ArtistWebsite(artist_id, chart_id)

        return website