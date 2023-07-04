from typing import List


def fit_sql_response(data: List[tuple], columns: list) -> List[dict]:
    """
    Fit data by columns
    :param data: data. Example [
    ('Petya', 800.0, datetime.datetime(2023, 7, 5, 0, 0, tzinfo=datetime.timezone.utc)),
    ('Vasya', 300.0, datetime.datetime(2023, 7, 5, 0, 0, tzinfo=datetime.timezone.utc))
    ]
    :param columns: columns. Example ['name', 'price_value', 'date']
    :return: fitted data Example:
    {'rating':
        [{'name': 'Petya', 'price_value': 800.0, 'date': '2023-07-05T00:00:00Z'},
        {'name': 'Vasya', 'price_value': 300.0, 'date': '2023-07-05T00:00:00Z'}]
    }
    """
    result = []
    for item in data:
        result.append(dict(zip(columns, item)))
    return result