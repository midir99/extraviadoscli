import datetime

SPANISH_MONTHS_MAP = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def parse_date(date_raw: str) -> datetime.date:
    date_raw = date_raw.strip()
    try:
        month, day, year = map(lambda s: s.strip(), date_raw.split(" "))
    except ValueError as e:
        raise ValueError(f'Unable to parse the date "{date_raw}"') from e

    try:
        month = SPANISH_MONTHS_MAP[month]
    except KeyError as e:
        raise ValueError(f'Unable to parse the date "{date_raw}"') from e

    try:
        day = int(day[:-1])
    except ValueError as e:
        raise ValueError(f'Unable to parse the date "{date_raw}"') from e

    try:
        year = int(year)
    except ValueError as e:
        raise ValueError(f'Unable to parse the date "{date_raw}"') from e

    try:
        return datetime.date(year, month, day)
    except ValueError as e:
        raise ValueError(f'Unable to parse the date "{date_raw}"') from e
