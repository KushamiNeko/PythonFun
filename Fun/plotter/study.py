import json
import os
import re
from datetime import datetime, timedelta
from typing import Optional, Callable

import pandas as pd
from matplotlib import axes
from matplotlib import font_manager as fm

from Fun.data.source import (
    FREQUENCY,
    DAILY,
    WEEKLY,
    INTRADAY_60MINUTES,
    INTRADAY_30MINUTES,
    INTRADAY_15MINUTES,
)
from Fun.plotter.plotter import Plotter, TextPlotter
from Fun.utils import colors, pretty


def read_notes(
    notes_root: str,
    frequency: FREQUENCY,
    func: Callable[[str, datetime, str, str], bool],
):

    # note_regex = r"^([$#%@&]*)\s*(Entrance|Exit|Study):*\s*(\d{4}-*\d{2}-*\d{2})(?:[T\s](\d{2}:\d{2})\s*[~-]\s*(\d{2}:\d{2}))*$"
    # note_regex = r"^\s*([!¥$#%@&+?*X]*)\s*(Entrance|Exit|Note|Study|Long|Short|Close):*\s*(\d{4}-*\d{2}-*\d{2})(?:[T\s](\d{2}:\d{2})\s*[~-]\s*(\d{2}:\d{2}))*\s*(?:\s*@\s*([\d'.]+)\s*\$\s*([LSXlsx]\d+))*$"
    # note_regex = r"^\s*([!¥$€£#%@&+?*X]*)\s*(Entrance|Exit|Note|Study|Long|Short|Close):*\s*(\d{4}-*\d{2}-*\d{2})(?:[T\s](\d{2}:\d{2})\s*(?:[~-]\s*(\d{2}:\d{2}))*)*\s*(?:\s*@\s*([\d'.]+)\s*\$\s*([LSXlsx]\d+))*$"
    # note_regex = r"^\s*([!¥$€£#%@&+?*X]*)\s*(Entrance|Exit|Note|Study|Long|Short|Close):*\s*(\d{4}-*\d{2}-*\d{2})(?:[T\s](\d{2}:\d{2})\s*(?:[~-]\s*(\d{2}:\d{2}))*)*\s*(?:\s*@\s*([\d'.]+)\s*\$\s*([LSXlsx]\d+))*\s*([#%]\s*[-0-9.]+)*\s*$"
    note_regex = r"^\s*([!¥$€£#%@&+?*XLS]*)\s*(Entrance|Exit|Note|Study|Long|Short|Close)*:*\s*(\d{4}-*\d{2}-*\d{2})(?:[T\s](\d{2}:\d{2})\s*(?:[~-]\s*(\d{2}:\d{2}))*)*\s*(?:\s*@\s*([\d'.]+)\s*\$\s*([LSXlsx]\d+))*\s*([#%]\s*[-0-9.]+)*\s*$"

    fs = os.listdir(notes_root)
    fs.sort()

    def sort_note(m):
        date = m[2].strip().replace("-", "")
        time = m[3].strip()

        if time != "":
            dt = datetime.strptime(f"{date}T{time}", "%Y%m%dT%H:%M")
        else:
            dt = datetime.strptime(date, "%Y%m%d")

        return dt

    for f in fs:
        with open(os.path.join(notes_root, f)) as nf:
            content = nf.read()

            regex = re.compile(note_regex, re.MULTILINE)
            match = regex.findall(content)

            match.sort(key=lambda m: sort_note(m))

            for m in match:
                pattern = m[0].strip()
                op = m[1].strip()
                date = m[2].strip().replace("-", "")
                time = m[3].strip()
                # price = m[5].strip()
                leverage = m[6].strip()

                pattern = "&" if pattern == "" else pattern
                if leverage != "":
                    if (
                        frequency == INTRADAY_60MINUTES
                        or frequency == INTRADAY_30MINUTES
                        or frequency == INTRADAY_15MINUTES
                    ):
                        pattern = f"{leverage[:1]}\n{leverage[1:]}"
                    else:
                        if op == "Entrance":
                            pattern = "&"
                        elif op == "Exit":
                            pattern = "!"
                        else:
                            pattern = "#"

                if time != "":
                    dt = datetime.strptime(f"{date}T{time}", "%Y%m%dT%H:%M")
                else:
                    dt = datetime.strptime(date, "%Y%m%d")

                if frequency == INTRADAY_30MINUTES:
                    if dt.minute == 15:
                        dt = dt.replace(minute=0, second=0)
                    if dt.minute == 45:
                        dt = dt.replace(minute=30, second=0)

                if frequency == INTRADAY_60MINUTES:
                    dt = dt.replace(minute=0, second=0)

                elif frequency == DAILY or frequency == WEEKLY:
                    if dt.hour > 16:
                        dt = dt + timedelta(days=1)

                    dt = dt.replace(hour=0, minute=0, second=0)

                    if frequency == WEEKLY:
                        dt = dt - timedelta(days=dt.weekday())

                if func(f, dt, pattern, content):
                    break


class StudyZone(Plotter):
    def __init__(
        self,
        symbol: str,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        candlesticks_body_width: float = 0.6,
        color_entry: str = colors.PAPER_BROWN_700,
        color_close: str = colors.PAPER_GREEN_700,
        color_warning: str = colors.PAPER_LIME_900,
        alpha: float = 0.3,
    ) -> None:
        assert quotes is not None

        root = os.path.join(
            os.getenv("HOME"), "Documents", "TRADING_NOTES", "study_zone"
        )

        self._symbol = symbol
        self._quotes = quotes
        self._frequency = frequency

        self._candlesticks_body_width = candlesticks_body_width

        self._color_entry = color_entry
        self._color_close = color_close
        self._color_warning = color_warning

        self._alpha = alpha

        self._studies = None

        for r in os.listdir(root):
            pattern = r"[&_,|]"
            targets = re.split(pattern, r)
            targets = list(map(lambda x: x.strip(), targets))

            if self._symbol.lower() in targets:
                path = os.path.join(root, r)
                assert os.path.exists(path)
                for f in os.listdir(path):
                    with open(os.path.join(path, f), "r") as src:
                        try:
                            if self._studies is None:
                                self._studies = json.load(src)
                            else:
                                self._studies.extend(json.load(src))
                        except json.JSONDecodeError:
                            pretty.color_print(
                                colors.PAPER_RED_400,
                                f"invalid json file for trading study zone: {path}",
                            )
                            self._studies = None

                break

    def plot(self, ax: axes.Axes) -> None:
        if self._studies is None:
            return

        if (
            self._frequency != DAILY
            and self._frequency != WEEKLY
            and self._frequency != INTRADAY_60MINUTES
        ):
            return

        mn, mx = ax.get_ylim()

        regex = re.compile(r"^(\d{8})(?:[T\s](\d{2}:\d{2}))*$")

        for study in self._studies:
            match = regex.match(study["start"])
            start = datetime.strptime(match.group(1), "%Y%m%d")

            match = regex.match(study["end"])
            end = datetime.strptime(match.group(1), "%Y%m%d")

            if self._frequency == WEEKLY:
                start = start - timedelta(days=start.weekday())
                end = end - timedelta(days=end.weekday())

            if self._frequency == INTRADAY_60MINUTES:
                match = regex.match(study["start"])
                if match.group(2) is not None:
                    start = datetime.strptime(
                        f"{match.group(1)}T{match.group(2)}", "%Y%m%dT%H:%M"
                    )
                else:
                    continue

                match = regex.match(study["end"])
                if match.group(2) is not None:
                    end = datetime.strptime(
                        f"{match.group(1)}T{match.group(2)}", "%Y%m%dT%H:%M"
                    )
                else:
                    continue

            assert start is not None
            assert end is not None

            try:

                start_index = self._quotes.index.get_loc(
                    start,
                )

                end_index = self._quotes.index.get_loc(
                    end,
                )

            except KeyError:
                continue

            color = ""
            if study["operation"] == "long":
                color = self._color_entry
            elif study["operation"] == "short":
                color = self._color_entry
            elif study["operation"] == "close":
                color = self._color_close
            elif study["operation"] == "warning":
                color = self._color_warning
            else:
                raise ValueError(f"invalid study operation: {study['operation']}")

            ax.bar(
                start_index - (self._candlesticks_body_width / 2.0),
                width=(end_index - start_index) + self._candlesticks_body_width,
                bottom=mn,
                height=mx - mn,
                align="edge",
                color=color,
                alpha=self._alpha,
            )


class NoteMarker(TextPlotter):
    def __init__(
        self,
        symbol: str,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        font_color: str = "w",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        super().__init__(
            font_color=font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._symbol = symbol

        self._quotes = quotes
        self._frequency = frequency

        root = os.path.join(
            os.getenv("HOME"),
            "Documents",
            "TRADING_NOTES",
            "notes",
        )

        self._notes_root = None
        for r in os.listdir(root):
            pattern = r"[&_,|]"

            targets = re.split(pattern, r)
            targets = list(map(lambda x: x.strip(), targets))

            if self._symbol.lower() in targets:
                path = os.path.join(root, r)
                if os.path.exists(path):
                    self._notes_root = path
                break

    def _plot_text(self, ax, highs, lows, middle, offset, x, text):
        high = highs.iloc[x]
        low = lows.iloc[x]
        m = (high + low) / 2.0

        # va = "bottom" if m > middle else "top"
        va = "top" if m > middle else "bottom"
        y = low - offset if va == "top" else high + offset

        ax.text(
            x,
            y,
            text,
            color=self._font_color,
            fontproperties=self._font_properties,
            ha="center",
            va=va,
        )

    def _append_note(self, notes, dt: datetime, text: str):
        try:
            if self._frequency == INTRADAY_60MINUTES:
                dt = dt.replace(minute=0)

            x = self._quotes.index.get_loc(
                dt,
            )

        except KeyError:
            return

        if x not in notes:
            notes[x] = [text]
        else:
            if text not in notes[x] or "\n" in text:
                notes[x].append(text)

    def plot(self, ax: axes.Axes) -> None:
        if self._notes_root is None:
            return

        if len(self._quotes) == 0:
            return

        if (
            self._frequency != DAILY
            and self._frequency != WEEKLY
            and self._frequency != INTRADAY_60MINUTES
            and self._frequency != INTRADAY_30MINUTES
            and self._frequency != INTRADAY_15MINUTES
        ):
            return

        assert ax is not None

        notes = {}

        read_notes(
            self._notes_root,
            self._frequency,
            lambda filename, dt, pattern, content: self._append_note(
                notes, dt, pattern
            ),
        )

        highs = self._quotes.loc[:, "high"]
        lows = self._quotes.loc[:, "low"]

        mx = highs.max()
        mn = lows.min()
        mr = mx - mn

        middle = (mx + mn) / 2.0
        offset = mr * 0.0075

        for x, text in notes.items():
            self._plot_text(
                ax,
                highs,
                lows,
                middle,
                offset,
                x,
                "\n".join(text),
            )
