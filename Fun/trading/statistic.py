from __future__ import annotations

import math
from datetime import datetime
from typing import Dict, List

from Fun.trading.trade import FuturesTrade


class Statistic:
    _float_decimals = 2

    def __init__(self, trades: List[FuturesTrade]) -> None:

        if len(trades) == 0:
            raise ValueError("empty statistic trades")

        self._trades = trades

        self._winners: List[FuturesTrade] = []
        self._losers: List[FuturesTrade] = []

        self._long: List[FuturesTrade] = []
        self._short: List[FuturesTrade] = []

        self._long_winners: List[FuturesTrade] = []
        self._long_losers: List[FuturesTrade] = []

        self._short_winners: List[FuturesTrade] = []
        self._short_losers: List[FuturesTrade] = []

        for trade in self._trades:
            if trade.nominal_pl() > 0:
                self._winners.append(trade)
            elif trade.nominal_pl() < 0:
                self._losers.append(trade)

            if trade.operation() == "+":
                self._long.append(trade)
            elif trade.operation() == "-":
                self._short.append(trade)

            if trade.operation() == "+" and trade.nominal_pl() > 0:
                self._long_winners.append(trade)
            elif trade.operation() == "+" and trade.nominal_pl() < 0:
                self._long_losers.append(trade)

            if trade.operation() == "-" and trade.nominal_pl() > 0:
                self._short_winners.append(trade)
            elif trade.operation() == "-" and trade.nominal_pl() < 0:
                self._short_losers.append(trade)

    def statistic_start(self) -> datetime:
        return sorted([t.open_time() for t in self._trades])[0]

    def statistic_end(self) -> datetime:
        return sorted([t.close_time() for t in self._trades])[-1]

    def total_trades(self) -> int:
        return len(self._trades)

    def total_long_trades(self) -> int:
        return len(self._long)

    def total_short_trades(self) -> int:
        return len(self._short)

    def number_of_winners(self) -> int:
        return len(self._winners)

    def number_of_long_winners(self) -> int:
        return len(self._long_winners)

    def number_of_short_winners(self) -> int:
        return len(self._short_winners)

    def number_of_losers(self) -> int:
        return len(self._losers)

    def number_of_long_losers(self) -> int:
        return len(self._long_losers)

    def number_of_short_losers(self) -> int:
        return len(self._short_losers)

    def batting_average(self) -> float:
        length = self.total_trades()
        if length == 0:
            return math.nan

        return float(self.number_of_winners()) / float(length)

    def batting_average_long(self) -> float:
        length = self.total_long_trades()
        if length == 0:
            return math.nan

        return float(self.number_of_long_winners()) / float(length)

    def batting_average_short(self) -> float:
        length = self.total_short_trades()
        if length == 0:
            return math.nan

        return float(self.number_of_short_winners()) / float(length)

    def winners_holding_mean(self) -> float:
        length = self.number_of_winners()
        trades = self._winners

        if length == 0:
            return math.nan

        days = 0
        for t in trades:
            days += (t.close_time() - t.open_time()).days

        return float(days) / float(length)

    def winners_holding_mean_long(self) -> float:
        length = self.number_of_long_winners()
        trades = self._long_winners

        if length == 0:
            return math.nan

        days = 0
        for t in trades:
            days += (t.close_time() - t.open_time()).days

        return float(days) / float(length)

    def winners_holding_mean_short(self) -> float:
        length = self.number_of_short_winners()
        trades = self._short_winners

        if length == 0:
            return math.nan

        days = 0
        for t in trades:
            days += (t.close_time() - t.open_time()).days

        return float(days) / float(length)

    def losers_holding_mean(self) -> float:
        length = self.number_of_losers()
        trades = self._losers

        if length == 0:
            return math.nan

        days = 0
        for t in trades:
            days += (t.close_time() - t.open_time()).days

        return float(days) / float(length)

    def losers_holding_mean_long(self) -> float:
        length = self.number_of_long_losers()
        trades = self._long_losers

        if length == 0:
            return math.nan

        days = 0
        for t in trades:
            days += (t.close_time() - t.open_time()).days

        return float(days) / float(length)

    def losers_holding_mean_short(self) -> float:
        length = self.number_of_short_losers()
        trades = self._short_losers

        if length == 0:
            return math.nan

        days = 0
        for t in trades:
            days += (t.close_time() - t.open_time()).days

        return float(days) / float(length)

    def winners_nominal_pl_mean(self) -> float:
        length = self.number_of_winners()
        trades = self._winners

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.nominal_pl()

        return s / float(length)

    def winners_nominal_pl_mean_long(self) -> float:
        length = self.number_of_long_winners()
        trades = self._long_winners

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.nominal_pl()

        return s / float(length)

    def winners_nominal_pl_mean_short(self) -> float:
        length = self.number_of_short_winners()
        trades = self._short_winners

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.nominal_pl()

        return s / float(length)

    def winners_leveraged_pl_mean(self) -> float:
        length = self.number_of_winners()
        trades = self._winners

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.leveraged_pl()

        return s / float(length)

    def winners_leveraged_pl_mean_long(self) -> float:
        length = self.number_of_long_winners()
        trades = self._long_winners

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.leveraged_pl()

        return s / float(length)

    def winners_leveraged_pl_mean_short(self) -> float:
        length = self.number_of_short_winners()
        trades = self._short_winners

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.leveraged_pl()

        return s / float(length)

    def losers_nominal_pl_mean(self) -> float:
        length = self.number_of_losers()
        trades = self._losers

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.nominal_pl()

        return s / float(length)

    def losers_nominal_pl_mean_long(self) -> float:
        length = self.number_of_long_losers()
        trades = self._long_losers

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.nominal_pl()

        return s / float(length)

    def losers_nominal_pl_mean_short(self) -> float:
        length = self.number_of_short_losers()
        trades = self._short_losers

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.nominal_pl()

        return s / float(length)

    def losers_leveraged_pl_mean(self) -> float:
        length = self.number_of_losers()
        trades = self._losers

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.leveraged_pl()

        return s / float(length)

    def losers_leveraged_pl_mean_long(self) -> float:
        length = self.number_of_long_losers()
        trades = self._long_losers

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.leveraged_pl()

        return s / float(length)

    def losers_leveraged_pl_mean_short(self) -> float:
        length = self.number_of_short_losers()
        trades = self._short_losers

        if length == 0:
            return math.nan

        s = 0.0
        for o in trades:
            s += o.leveraged_pl()

        return s / float(length)

    def nominal_win_loss_ratio(self) -> float:
        return self.winners_nominal_pl_mean() / abs(self.losers_nominal_pl_mean())

    def nominal_win_loss_ratio_long(self) -> float:
        return self.winners_nominal_pl_mean_long() / abs(
                self.losers_nominal_pl_mean_long()
        )

    def nominal_win_loss_ratio_short(self) -> float:
        return self.winners_nominal_pl_mean_short() / abs(
                self.losers_nominal_pl_mean_short()
        )

    def leveraged_win_loss_ratio(self) -> float:
        return self.winners_leveraged_pl_mean() / abs(self.losers_leveraged_pl_mean())

    def leveraged_win_loss_ratio_long(self) -> float:
        return self.winners_leveraged_pl_mean_long() / abs(
                self.losers_leveraged_pl_mean_long()
        )

    def leveraged_win_loss_ratio_short(self) -> float:
        return self.winners_leveraged_pl_mean_short() / abs(
                self.losers_leveraged_pl_mean_short()
        )

    def nominal_adjusted_win_loss_ratio(self) -> float:
        ba = self.batting_average()

        return (self.winners_nominal_pl_mean() * ba) / (
                abs(self.losers_nominal_pl_mean()) * (1.0 - ba)
        )

    def nominal_adjusted_win_loss_ratio_long(self) -> float:
        ba = self.batting_average_long()

        return (self.winners_nominal_pl_mean_long() * ba) / (
                abs(self.losers_nominal_pl_mean_long()) * (1.0 - ba)
        )

    def nominal_adjusted_win_loss_ratio_short(self) -> float:
        ba = self.batting_average_short()

        return (self.winners_nominal_pl_mean_short() * ba) / (
                abs(self.losers_nominal_pl_mean_short()) * (1.0 - ba)
        )

    def leveraged_adjusted_win_loss_ratio(self) -> float:
        ba = self.batting_average()

        return (self.winners_leveraged_pl_mean() * ba) / (
                abs(self.losers_leveraged_pl_mean()) * (1.0 - ba)
        )

    def leveraged_adjusted_win_loss_ratio_long(self) -> float:
        ba = self.batting_average_long()

        return (self.winners_leveraged_pl_mean_long() * ba) / (
                abs(self.losers_leveraged_pl_mean_long()) * (1.0 - ba)
        )

    def leveraged_adjusted_win_loss_ratio_short(self) -> float:
        ba = self.batting_average_short()

        return (self.winners_leveraged_pl_mean_short() * ba) / (
                abs(self.losers_leveraged_pl_mean_short()) * (1.0 - ba)
        )

    def nominal_expected_value(self) -> float:
        ba = self.batting_average()

        return (self.winners_nominal_pl_mean() * ba) + (
                self.losers_nominal_pl_mean() * (1.0 - ba)
        )

    def nominal_expected_value_long(self) -> float:
        ba = self.batting_average_long()

        return (self.winners_nominal_pl_mean_long() * ba) + (
                self.losers_nominal_pl_mean_long() * (1.0 - ba)
        )

    def nominal_expected_value_short(self) -> float:
        ba = self.batting_average_short()

        return (self.winners_nominal_pl_mean_short() * ba) + (
                self.losers_nominal_pl_mean_short() * (1.0 - ba)
        )

    def leveraged_expected_value(self) -> float:
        ba = self.batting_average()

        return (self.winners_leveraged_pl_mean() * ba) + (
                self.losers_leveraged_pl_mean() * (1.0 - ba)
        )

    def leveraged_expected_value_long(self) -> float:
        ba = self.batting_average_long()

        return (self.winners_leveraged_pl_mean_long() * ba) + (
                self.losers_leveraged_pl_mean_long() * (1.0 - ba)
        )

    def leveraged_expected_value_short(self) -> float:
        ba = self.batting_average_short()

        return (self.winners_leveraged_pl_mean_short() * ba) + (
                self.losers_leveraged_pl_mean_short() * (1.0 - ba)
        )

    def nominal_kelly_criterion(self) -> float:
        ba = self.batting_average()

        return ba - ((1.0 - ba) / self.nominal_win_loss_ratio())

    def nominal_kelly_criterion_long(self) -> float:
        ba = self.batting_average_long()

        return ba - ((1.0 - ba) / self.nominal_win_loss_ratio_long())

    def nominal_kelly_criterion_short(self) -> float:
        ba = self.batting_average_short()

        return ba - ((1.0 - ba) / self.nominal_win_loss_ratio_short())

    def leveraged_kelly_criterion(self) -> float:
        ba = self.batting_average()

        return ba - ((1.0 - ba) / self.leveraged_win_loss_ratio())

    def leveraged_kelly_criterion_long(self) -> float:
        ba = self.batting_average_long()

        return ba - ((1.0 - ba) / self.leveraged_win_loss_ratio_long())

    def leveraged_kelly_criterion_short(self) -> float:
        ba = self.batting_average_short()

        return ba - ((1.0 - ba) / self.leveraged_win_loss_ratio_short())

    def to_entity(self) -> Dict[str, str]:
        return {
            "statistic_start":                         self.statistic_start().strftime("%Y%m%d"),
            "statistic_end":                           self.statistic_end().strftime("%Y%m%d"),
            "total_trades":                            f"{self.total_trades()}",
            "total_long_trades":                       f"{self.total_long_trades()}",
            "total_short_trades":                      f"{self.total_short_trades()}",
            "number_of_winners":                       f"{self.number_of_winners()}",
            "number_of_losers":                        f"{self.number_of_losers()}",
            "batting_average":                         f"{self.batting_average() * 100.0:.{self._float_decimals}f}%",
            "batting_average_long":                    f"{self.batting_average_long() * 100.0:.{self._float_decimals}f}%",
            "batting_average_short":                   f"{self.batting_average_short() * 100.0:.{self._float_decimals}f}%",
            "winners_holding_mean":                    f"{self.winners_holding_mean():.{self._float_decimals}f}",
            "winners_holding_mean_long":               f"{self.winners_holding_mean_long():.{self._float_decimals}f}",
            "winners_holding_mean_short":              f"{self.winners_holding_mean_short():.{self._float_decimals}f}",
            "losers_holding_mean":                     f"{self.losers_holding_mean():.{self._float_decimals}f}",
            "losers_holding_mean_long":                f"{self.losers_holding_mean_long():.{self._float_decimals}f}",
            "losers_holding_mean_short":               f"{self.losers_holding_mean_short():.{self._float_decimals}f}",
            "nominal_win_loss_ratio":                  f"{self.nominal_win_loss_ratio():.{self._float_decimals}f}",
            "nominal_win_loss_ratio_long":             f"{self.nominal_win_loss_ratio_long():.{self._float_decimals}f}",
            "nominal_win_loss_ratio_short":            f"{self.nominal_win_loss_ratio_short():.{self._float_decimals}f}",
            "leveraged_win_loss_ratio":                f"{self.leveraged_win_loss_ratio():.{self._float_decimals}f}",
            "leveraged_win_loss_ratio_long":           f"{self.leveraged_win_loss_ratio_long():.{self._float_decimals}f}",
            "leveraged_win_loss_ratio_short":          f"{self.leveraged_win_loss_ratio_short():.{self._float_decimals}f}",
            "nominal_adjusted_win_loss_ratio":         f"{self.nominal_adjusted_win_loss_ratio():.{self._float_decimals}f}",
            "nominal_adjusted_win_loss_ratio_long":    f"{self.nominal_adjusted_win_loss_ratio_long():.{self._float_decimals}f}",
            "nominal_adjusted_win_loss_ratio_short":   f"{self.nominal_adjusted_win_loss_ratio_short():.{self._float_decimals}f}",
            "leveraged_adjusted_win_loss_ratio":       f"{self.leveraged_adjusted_win_loss_ratio():.{self._float_decimals}f}",
            "leveraged_adjusted_win_loss_ratio_long":  f"{self.leveraged_adjusted_win_loss_ratio_long():.{self._float_decimals}f}",
            "leveraged_adjusted_win_loss_ratio_short": f"{self.leveraged_adjusted_win_loss_ratio_short():.{self._float_decimals}f}",
            "nominal_expected_value":                  f"{self.nominal_expected_value() * 100.0:.{self._float_decimals}f}%",
            "nominal_expected_value_long":             f"{self.nominal_expected_value_long() * 100.0:.{self._float_decimals}f}%",
            "nominal_expected_value_short":            f"{self.nominal_expected_value_short() * 100.0:.{self._float_decimals}f}%",
            "leveraged_expected_value":                f"{self.leveraged_expected_value() * 100.0:.{self._float_decimals}f}%",
            "leveraged_expected_value_long":           f"{self.leveraged_expected_value_long() * 100.0:.{self._float_decimals}f}%",
            "leveraged_expected_value_short":          f"{self.leveraged_expected_value_short() * 100.0:.{self._float_decimals}f}%",
            "winners_nominal_pl_mean":                 f"{self.winners_nominal_pl_mean() * 100.0:.{self._float_decimals}f}%",
            "winners_nominal_pl_mean_long":            f"{self.winners_nominal_pl_mean_long() * 100.0:.{self._float_decimals}f}%",
            "winners_nominal_pl_mean_short":           f"{self.winners_nominal_pl_mean_short() * 100.0:.{self._float_decimals}f}%",
            "winners_leveraged_pl_mean":               f"{self.winners_leveraged_pl_mean() * 100.0:.{self._float_decimals}f}%",
            "winners_leveraged_pl_mean_long":          f"{self.winners_leveraged_pl_mean_long() * 100.0:.{self._float_decimals}f}%",
            "winners_leveraged_pl_mean_short":         f"{self.winners_leveraged_pl_mean_short() * 100.0:.{self._float_decimals}f}%",
            "losers_nominal_pl_mean":                  f"{self.losers_nominal_pl_mean() * 100.0:.{self._float_decimals}f}%",
            "losers_nominal_pl_mean_long":             f"{self.losers_nominal_pl_mean_long() * 100.0:.{self._float_decimals}f}%",
            "losers_nominal_pl_mean_short":            f"{self.losers_nominal_pl_mean_short() * 100.0:.{self._float_decimals}f}%",
            "losers_leveraged_pl_mean":                f"{self.losers_leveraged_pl_mean() * 100.0:.{self._float_decimals}f}%",
            "losers_leveraged_pl_mean_long":           f"{self.losers_leveraged_pl_mean_long() * 100.0:.{self._float_decimals}f}%",
            "losers_leveraged_pl_mean_short":          f"{self.losers_leveraged_pl_mean_short() * 100.0:.{self._float_decimals}f}%",
        }
