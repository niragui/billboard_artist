import datetime


TITLE_FIELD = "title"
ARTIST_FIELD = "artist"

DEBUT_DATE_FIELD = "debut-date"

PEAK_FIELD = "peak-pos"
PEAK_WEEKS_FIELD = "peak-week"
PEAK_DATE_FIELD = "peak-date"

WEEKS_FIELD = "week-on-chart"

PEAK_DATE_ATTR = "peak_date"
DEBUT_DATE_ATTR = "debut_date"


def read_date_from_html(html_code: str):
    """
    Given an html code of the debut or peak date,
    it returns the date

    Parameters:
        - html_code: HTML Code of the date to read
    """
    link_start = html_code.find("\"") + 1
    link_end = html_code.find("\"", link_start)

    link_date = html_code[link_start: link_end]

    date_start = link_date.rfind("/") + 1
    found_date = link_date[date_start:]

    return datetime.date.fromisoformat(found_date)


class ChartEntry():
    def __init__(self,
                 entry_data: dict) -> None:
        self.title = entry_data[TITLE_FIELD]
        self.artist = entry_data[ARTIST_FIELD]

        self.peak = entry_data[PEAK_FIELD]
        peak_weeks_data = entry_data[PEAK_WEEKS_FIELD]
        peak_weeks_data = peak_weeks_data.split()

        peak_weeks = peak_weeks_data[0]
        if peak_weeks.isnumeric():
            self.peak_weeks = int(peak_weeks)
        else:
            self.peak_weeks = 0

        self.weeks = entry_data[WEEKS_FIELD]

        self.debut_date = read_date_from_html(entry_data[DEBUT_DATE_FIELD])
        self.peak_date = read_date_from_html(entry_data[DEBUT_DATE_FIELD])

    def create_json(self):
        """
        Returns a readable json for for the given website
        """
        data_dict = vars(self)
        data_dict[PEAK_DATE_ATTR] = data_dict[PEAK_DATE_ATTR].isoformat()
        data_dict[DEBUT_DATE_ATTR] = data_dict[DEBUT_DATE_ATTR].isoformat()

        return data_dict

    def __repr__(self) -> str:
        repr_str = f"#{self.peak}"

        if self.peak == 1:
            repr_str += f" x{self.peak_weeks}"

        repr_str += f" - {self.title} [{self.weeks} weeks]"

        return repr_str

    def __eq__(self, other):
        return self.weeks == other.weeks

    def __lt__(self, other):
        return self.weeks < other.weeks

    def __le__(self, other):
        return self.weeks <= other.weeks

    def __gt__(self, other):
        return self.weeks > other.weeks

    def __ge__(self, other):
        return self.weeks >= other.weeks


if __name__ == "__main__":
    test_data = {
        "title": "Thriller",
        "artist": "Michael Jackson",
        "debut-date": "\u003Ca href=\"https://www.billboard.com/charts/hot-100/2005-11-12\"\u003E11.12.05\u003C/a\u003E",
        "peak-pos": 1,
        "peak-week": "4 WKS",
        "peak-date": "\u003Ca href=\"https://www.billboard.com/charts/hot-100/2008-11-15\"\u003E11.15.08\u003C/a\u003E",
        "week-on-chart": 25,
        "aria-labels": [
            "Name - Thriller Michael Jackson",
            "Debut Date - 11 12 2005",
            "Peak Position - 1 for 4 Weeks",
            "Peak Date - 11 15 2008",
            "Weeks on Chart 25"
        ]
    }

    chart_data = ChartEntry(test_data)

    print(vars(chart_data))
