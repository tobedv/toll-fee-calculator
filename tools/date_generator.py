import datetime
import json


def generate_july_dates(year):
    dates = []
    start = datetime.datetime(year=year, month=7, day=1)
    for day in range(2, 32):
        dates.append(start.date())
        start = start.replace(day=day)
    return dates


def generate_red_and_free_days(red_days):
    dates = []
    # The day before a red day should be included as free
    for day in red_days:
        current_day = datetime.datetime.strptime(day, "%Y-%m-%d")
        day_before = current_day - datetime.timedelta(days=1)
        dates.append(day_before.date())
        dates.append(current_day.date())
    return dates


if __name__ == "__main__":
    """
    Red days are taken from, https://publicholidays.se/sv/2019-dates/
    Free days from https://transportstyrelsen.se/sv/vagtrafik/Trangselskatt/Betalning/dagar-da-trangselskatt-inte-tas-ut/
    """
    year = 2019
    red_days = [
        "2019-01-01",
        "2019-01-06",
        "2019-04-19",
        "2019-04-21",
        "2019-04-22",
        "2019-05-01",
        "2019-05-30",
        "2019-06-06",
        "2019-06-09",
        "2019-06-22",
        "2019-11-02",
        "2019-12-25",
        "2019-12-26",
    ]
    free_days = [
        "2019-01-01",
        "2019-04-18",
        "2019-04-19",
        "2019-05-01",
        "2019-06-05",
        "2019-06-06",
        "2019-06-21",
        "2019-11-01",
        "2019-12-24",
        "2019-12-25",
        "2019-12-26",
        "2019-12-31",
    ]
    july = generate_july_dates(year)
    red_and_free = generate_red_and_free_days(red_days)
    all_dates = (
        july
        + red_and_free
        + [datetime.datetime.strptime(day, "%Y-%m-%d").date() for day in free_days]
    )
    # set to filter out duplicates, if clause to remove wrong year (should only be 2018-12-31)
    # sort, and get string representation for date, could be implemented as custom json decoder
    filtered_dates = list({date for date in all_dates if date.year == 2019})
    filtered_dates.sort()
    filtered_dates = [str(date) for date in filtered_dates]
    print(json.dumps(list(filtered_dates)))
