import csv
import os
import datetime
import typing


class CsvParser:
    def _convert_datestr_to_datetime(self, date_str: str) -> datetime.datetime:
        """Converts a date string into a datetime object
        
        Args:
            date_str (str)
        
        Returns:
            datetime.datetime
        """

        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def parse_csv(
        self, path_to_csv: str
    ) -> typing.Tuple[str, typing.List[datetime.datetime]]:
        """Parse CSV file matching format:

        licence_plate,date_of_pass
        str, YYYY-mm-dd HH:MM:SS
        
        Args:
            path_to_csv (str)
        
        Raises:
            FileNotFoundError: If CSV file is not found
        
        Returns:
            typing.Tuple[str, typing.List[datetime.datetime]]
        """
        if os.path.isfile(path_to_csv):
            passes = []
            licence_plate = None
            with open(path_to_csv) as f:
                reader = csv.DictReader(f, delimiter=",")
                for row in reader:
                    if not licence_plate:
                        licence_plate = row["licence_plate"]
                    passes.append(
                        self._convert_datestr_to_datetime(row["date_of_pass"])
                    )
            return licence_plate, passes
        else:
            raise FileNotFoundError("CSV file doest not exist")
