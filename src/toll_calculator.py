import typing
import datetime


class TollCalculator:
    def __init__(self, config: dict):
        self.config = config
        self.taxes = None
        self.max_daily_tax = None

    def _load_tax_mappings(self, year: str) -> None:
        """
        Lad tax mappings from config into more usable datetime objects, set max_daily_tax
        """
        self.taxes = []
        for period in self.config[year]["tax"]:
            self.taxes.append(
                {
                    "start_time": datetime.time.fromisoformat(period["start_time"]),
                    "end_time": datetime.time.fromisoformat(period["end_time"]),
                    "price": period["price"],
                }
            )
        self.max_daily_tax = self.config[year]["max_daily_tax"]

    def _get_toll_for_time(self, current_time: datetime.datetime) -> int:
        if not self.taxes:
            self._load_tax_mappings(str(current_time.year))
        for period in self.taxes:
            if period["start_time"] <= current_time.time() <= period["end_time"]:
                return period["price"]

    def _calculate_max_toll_for_interval(
        self, passes: typing.List[datetime.datetime]
    ) -> int:
        return max([self._get_toll_for_time(p) for p in passes])

    def _build_date_intervals(
        self, passes: typing.List[datetime.datetime]
    ) -> typing.List[list]:

        interval_start = passes[0]
        intervals = [[interval_start]]
        current_interval_index = 0

        # Start next pass, skip first item already added to first interval array
        for next_pass in passes[1:]:
            diff = next_pass - interval_start
            if diff <= datetime.timedelta(minutes=60):
                intervals[current_interval_index].append(next_pass)
            else:
                current_interval_index += 1
                intervals.append([next_pass])
                interval_start = next_pass
        return intervals

    def get_daily_total_toll_fee(self, passes: typing.List[datetime.datetime]) -> int:
        # Toll taxes and mapping needs to be fetched based on which year is requested, 2018, 2019 etc, initiate mapping based on that.
        total_fee = 0
        intervals = self._build_date_intervals(passes)
        for interval in intervals:
            total_fee += self._calculate_max_toll_for_interval(interval)
        return min(total_fee, self.max_daily_tax)
