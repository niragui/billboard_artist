import json

import os

from .utils import standarize_name
from .exceptions import InvalidFile, InvalidID, MissingChart

THIS_FOLDER = os.path.dirname(__file__)

CHARTS_FILE = os.path.join(THIS_FOLDER, "charts.json")


class ChartParser():
    def __init__(self,
                 file: str = CHARTS_FILE) -> None:
        self.file = file

        if not os.path.isfile(file):
            raise OSError(f"Charts File Doesn't Exist [{file}]")

        try:
            with open(file, "r") as f:
                self.charts = json.load(f)
        except json.JSONDecodeError:
            raise InvalidFile(f"Charts File Not JSON Formatted [{file}]")

    def update_chart(self,
                     chart: str,
                     chart_id: str):
        """
        Given a new chart and its id, it adds it to the
        charts id base.

        Parameters:
            - chart: Name of the chart to add
            - chart_id: Id of the chart to add
        """
        chart = standarize_name(chart)
        chart_id = chart_id.upper()

        bef_id = self.charts.get(chart, None)

        if bef_id is not None and bef_id != chart_id:
            raise InvalidID(f"Chart Already Saved With Other ID [{bef_id} vs {chart_id}]")
        elif bef_id is not None:
            return

        self.charts[chart] = chart_id

        with open(self.file, "w") as f:
            f.write(json.dumps(self.charts, indent=4))

    def get_chart_id(self,
                     chart: str):
        """
        Get the chart id of an asked chart

        Parameters:
            - chart: Name of the chart to ask for
        """
        chart = standarize_name(chart)

        chart_id = self.charts.get(chart, None)

        if chart_id is None:
            raise MissingChart(f"Chart Couldn't Be Found [{chart}]")

        return chart_id
