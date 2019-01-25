import typing
import datetime


class TollCalculator:
    def __init__(self, config: dict):
        self.config = config
        self.taxes = None
        self.max_daily_tax = None

    def _load_tax_mappings(self) -> None:
        """Initiate tax mappings from config file into the instance
        
        Returns:
            None
        """
        self.taxes = []
        for period in self.config["tax"]:
            self.taxes.append(
                {
                    "start_time": datetime.time.fromisoformat(period["start_time"]),
                    "end_time": datetime.time.fromisoformat(period["end_time"]),
                    "price": period["price"],
                }
            )
        self.max_daily_tax = self.config["max_daily_tax"]

    def _get_toll_for_time(self, current_time: datetime.datetime) -> int:
        """Returns the cost of passing at a certain time
        
        Args:
            current_time (datetime.datetime): Time of pass
        
        Returns:
            int: Cost of pass
        """
        if not self.taxes:
            self._load_tax_mappings()
        for period in self.taxes:
            if period["start_time"] <= current_time.time() <= period["end_time"]:
                return period["price"]

    def _calculate_max_toll_for_interval(
        self, passes: typing.List[datetime.datetime]
    ) -> int:
        """Returns the maximum toll for a list of datetimes (passes)
        
        Args:
            passes (typing.List[datetime.datetime]): Passes that should be considered in the current interval
        
        Returns:
            int: Maximum cost inside that interval
        """
        return max([self._get_toll_for_time(p) for p in passes])

    def _build_date_intervals(
        self, passes: typing.List[datetime.datetime]
    ) -> typing.List[list]:
        """Groups all datetime objects in a list of 60 minute groups.
        Starting with the first item, all items inside 60 minutes after that will be grouped.
        When an item passes 60 minutes after the initiator of the last group a new group will be generated.
        
        Args:
            passes (typing.List[datetime.datetime])
        
        Returns:
            typing.List[list]: A list with lists where each included list are inside a 60 minute interval from the first item
        """
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
        """Based on a list of passes (datetime objects) generate the cost for those passes that day.

        Based on the specification:
        Fees will differ between 9 SEK and 22 SEK, depending on the time of day.
        The maximum fee for one day is 60 SEK.
        Only the highest fee should be charged for multiple passages within a 60 minute period.
        Fee-free days are; Saturdays, Sundays, holidays and day before holidays and the whole month of July. See Transportstyrelsen for details.

        Args:
            passes (typing.List[datetime.datetime]): All passes one day
        
        Returns:
            int: Total cost
        """
        total_fee = 0
        intervals = self._build_date_intervals(passes)
        for interval in intervals:
            total_fee += self._calculate_max_toll_for_interval(interval)
        return min(total_fee, self.max_daily_tax)
