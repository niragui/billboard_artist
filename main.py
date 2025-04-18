from src.new_peaks_checker import NewPeaksChecker

import datetime

import os
import sys

IMPORT_PATH = os.path.join(__file__, os.pardir, os.pardir, os.pardir)
sys.path.append(IMPORT_PATH)

from Publisher.publisher import Publisher

chart_id = "CAN"
chart_name = "Canada Hot 100"

chart_id = "HSI"
chart_name = "Hot 100"

checker = NewPeaksChecker(chart_id)

new_peaks = checker.loop_for_artists()


if len(new_peaks) > 0:
    subject = f"New Peaks/Debuts For {chart_name} [{datetime.date.today()}]"

    text = ""

    texts = []

    for new_peak in new_peaks[::-1]:
        new_text = str(new_peak) + "\n"
        if new_text in texts:
            continue
        texts.append(new_text)
        text += new_text

    publisher = Publisher(chart_name, subject, text)
    publisher.publish()