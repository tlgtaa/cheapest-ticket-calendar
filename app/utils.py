import datetime
import time
from itertools import combinations, product
from typing import Any, List, Tuple

from fastapi import HTTPException

from dateutil.rrule import rrule, DAILY

from .constants import CITIES, BASE_URL, PARTNER


def validate_date_format(date_text):
    """
    Валидация даты.
    формат даты: dd/mm/yyyy

    """
    try:
        datetime.datetime.strptime(date_text, "%d/%m/%Y")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Incorrect date format, should be dd/mm/yyyy",
        )


def get_routes() -> List[Tuple[Any, ...]]:
    routes = list(combinations([city.value for city in CITIES], r=2))
    return routes


def get_flight_days_dates(from_date: datetime.date, to_days: int) -> List[str]:
    flight_dates = [
        d.strftime("%d/%m/%Y")
        for d in rrule(freq=DAILY, dtstart=from_date, count=to_days)
    ]
    return flight_dates


def get_routes_with_flight_days(
    routes: List[Tuple[Any, ...]], flight_days: List[str]
) -> List[Tuple[Tuple[str], str]]:
    flight_routes_and_days = list(product(routes, flight_days))
    return flight_routes_and_days


def make_request_urls(
    routes_with_days: List[Tuple[Tuple[str], str]], result_limit: int = 50,
) -> List[str]:
    urls = []
    for route, date in routes_with_days:
        urls.append(
            f"{BASE_URL}?fly_from={route[0]}&fly_to={route[1]}&date_from={date}&partner={PARTNER}&curr=KZT&=locale=ru&oneway&max_fly_duration=24&one_per_date=1&sort=price&asc=1&limit={result_limit}"
        )
    return urls
