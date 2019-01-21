import typing
import datetime


class TollCalculator:
    def __init__(self, config: dict):
        self.config = config
        self.max_daily_tax = self.config["max_daily_tax"]
        self.taxes = []
        self._initiate_tax_mappings()

    def _initiate_tax_mappings(self):
        """
        Parses string times into datetime objects for easier comparison
        """
        for period in self.config["tax"]:
            self.taxes.append(
                {
                    "start_time": datetime.time.fromisoformat(period["start_time"]),
                    "end_time": datetime.time.fromisoformat(period["end_time"]),
                    "price": period["price"],
                }
            )

    def _get_toll_for_time(self, current_time: datetime.datetime) -> int:
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

        for next_pass in passes:
            diff = next_pass - interval_start
            if diff <= datetime.timedelta(minutes=60):
                # Add to current interval as long as in the same 60 minutes
                intervals[current_interval_index].append(next_pass)
            else:
                # If bypassing 60 minutes, create new interval, change interval_start for new chunk
                current_interval_index += 1
                intervals.append([next_pass])
                interval_start = next_pass
        return intervals

    def _get_daily_total_toll_fee(self, passes: typing.List[datetime.datetime]) -> int:
        """
        Calculate the total toll fee for one day

        Args:
            passes (list): Date and time (:py:class:`datetime.datetime`)
                of all passes on one day, assumes being sorted by date, lower first.

        Returns:
            int: The total toll fee for that day.
        """

        total_fee = 0
        intervals = self._build_date_intervals(passes)
        for interval in intervals:
            total_fee += self._calculate_max_toll_for_interval(interval)
        return min(total_fee, self.max_daily_tax)


if __name__ == "__main__":
    cfg = {
        "max_daily_tax": 60,
        "tax": [
            {"start_time": "06:00", "end_time": "06:29", "price": 9},
            {"start_time": "06:30", "end_time": "06:59", "price": 16},
            {"start_time": "07:00", "end_time": "07:59", "price": 22},
            {"start_time": "08:00", "end_time": "08:29", "price": 16},
            {"start_time": "08:30", "end_time": "14:59", "price": 9},
            {"start_time": "15:00", "end_time": "15:29", "price": 16},
            {"start_time": "15:30", "end_time": "16:59", "price": 22},
            {"start_time": "17:00", "end_time": "17:59", "price": 16},
            {"start_time": "18:00", "end_time": "18:29", "price": 9},
            {"start_time": "18:30", "end_time": "05:59", "price": 0},
        ],
    }
    tc = TollCalculator(cfg)
    test_data = [
        datetime.datetime.now(),
        datetime.datetime.now() + datetime.timedelta(minutes=20),
        datetime.datetime.now() + datetime.timedelta(minutes=40),
        datetime.datetime.now() + datetime.timedelta(minutes=59),
        # Second
        datetime.datetime.now() + datetime.timedelta(minutes=60),
        datetime.datetime.now() + datetime.timedelta(minutes=65),
        # Third
        datetime.datetime.now() + datetime.timedelta(minutes=150),
    ]
    r = tc._get_daily_total_toll_fee(test_data)
    print(r)
