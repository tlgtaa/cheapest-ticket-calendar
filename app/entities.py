import asyncio
import datetime

# import json
import time
from typing import Iterable, List, Dict, Any
from pydantic import BaseModel

import aiohttp

from .utils import (
    get_routes,
    get_flight_days_dates,
    get_routes_with_flight_days,
    make_request_urls,
)


class Route(BaseModel):
    fly_from: str
    fly_to: str
    currency: str = "KZT"
    price: float
    booking_token: str
    pnum: int = 1
    adults: int = 1
    children: int = 0
    infants: int = 0


def make_price_confirmation_url(
    *,
    booking_token: str,
    pnum: int,
    currency: str,
    adults: int,
    children: str,
    infants: str,
) -> str:
    url = (
        f"https://booking-api.skypicker.com/api/v0.1/check_flights?v=2&booking_token={booking_token}&bnum=0&pnum={pnum}&currency={currency}&adults={adults}&children={children}&infants={infants}"
        + "&affily=picky_{market}/"
    )
    # confirmation_urls = []

    # for obj in data:
    #     confirmation_urls.append(
    #         f"{url}&booking_token={obj['booking_token']}&bnum=0&pnum=1&currency=KZT&adults=1"
    #         + "&affily=picky_{market}"
    #     )
    return url


def get_price_confirmation_url(datas: Dict[Any, Any]) -> List[str]:

    lst = []
    for key, values in datas.items():
        for value in values:
            url = make_price_confirmation_url(
                booking_token=value.booking_token,
                pnum=value.pnum,
                currency=value.currency,
                adults=value.adults,
                children=value.children,
                infants=value.infants,
            )
            lst.append(url)
    return lst


async def get_data(url: str):
    print(f"Start getting data from {url}")
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
    ) as session:
        response = await session.get(url,)
        await response.read()
        resp = await response.json()
    return resp


async def fetch_data(urls: Iterable[str]):
    return await asyncio.gather(*[get_data(url) for url in urls])


def load_cheapest_routes():
    start_time = time.monotonic()

    # GET possible routes
    routes = get_routes()

    # Get month days
    today = datetime.date.today()
    dates = get_flight_days_dates(today, 31)

    # compute days and possible routes
    routes_with_flight_days = get_routes_with_flight_days(
        routes=routes, flight_days=dates
    )

    # Создаем лист url-ов для каждого роута на месяц
    urls = make_request_urls(routes_with_flight_days, result_limit=5)

    # в результат получаем json со списком цен. [по 5 ответов для каждого url-а т.к. установили result_limit]
    # reduced = urls[:10]
    flights = asyncio.run(fetch_data(urls[:10]))

    datas = [flight["data"] for flight in flights if len(flight["data"]) > 0]

    flight_representation = {}
    for data in datas:
        for val in data:
            # print(val["route"])
            date_from = datetime.datetime.fromtimestamp(
                val["route"][0]["dTime"]
            ).strftime("%d/%m/%Y")

            flight_representation.setdefault(date_from, []).append(
                Route(
                    fly_from=val["flyFrom"],
                    fly_to=val["flyTo"],
                    price=val["price"],
                    booking_token=val["booking_token"],
                ),
            )

    flight_confirmation_urls = get_price_confirmation_url(
        flight_representation
    )

    # urls_to_valid_confirmation = asyncio.run(
    #     fetch_data(flight_confirmation_urls[:10])
    # )

    # for flight_confirmation_url in flight_confirmation_urls:
    #     r = asyncio.run(
    #         get_data(
    #             "https://booking-api.skypicker.com/api/v0.1/check_flights?v=2&booking_token=TjFsU9KOyjpEDqm5dNSrO1ZjuRMVMgZrERrSppD325T6P8+P9w468E+3gYirNKm0xjFEaQ8brFkJXYHcFnHHQP5fINbkDjCTreeWig4WZ7B4fBYYSUgmpu0Cq8+F75sB1L9aQ+cDGm5LObGbRYN0pwUDk5LuVOHkDPT1Qmo6XhmrtXw4mLqlylxVlpY+8jS2/eBYqLA7CPIQyfcUqPhx/F26+QR/TnuLRGUvd7cpYS88pyKmqcUiqIMz9FvuwQTxaTrPz8tES/e8I0br2Ukn4YrIvIX3jo30Rxwts1D64ZSjKrZne87kU+PYeizs0RTIYiVu5Zux/kNlWRTw4GuQENl5maQY+cvTyNeEmsSFNAnncJjC9hZeaAE665S2m17ZkQoH5qOydbZF321QBC3qXDzTZS6JFct/tS48NzvLd9u9vfull8wo3cBVl29GyOpSjdY+NJ3UzagFZOpNCT+tjIgElPELVzuzMAy7sqqvGk5b0SAO0D+xBuiOg3NIggZfHyZ+clsgRcMiTj33hVaSuL9PLtkvHV3xMgufu6AdAnVUQdv4qsWH3S4aXckyEVSpuVH1VxzYPm1ikRrUSup8lV/xJsITBR6v/IlkwTuWn6S4oasaojMW6sjrPrZObC0xtQ7jZ53BYcnYD+RGXeT6pTBfWjjjlgq45g5Hi2ta9fo=&bnum=3&pnum=2&affily=picky_{market}&currency=USD&adults=1&children=0&infants=1"
    #         )
    #     )
    #     print(r)
    print(f"[Finished time]::{time.monotonic() - start_time}")

    return flight_representation


def get_deals_list(datas) -> list:
    lst = []
    for i, arr in enumerate(datas):
        for idx, val in enumerate(arr):
            lst.append(val)
    return lst


# def is_valid_offer(url: str) -> bool:
#     data = asyncio.run(check_data(url))
#     # pass
#     # print("========> ", data)
#     return True
