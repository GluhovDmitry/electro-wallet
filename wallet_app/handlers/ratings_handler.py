from datetime import date
from dateutil.relativedelta import relativedelta
from loguru import logger
from django.db import connection

from utils import fit_sql_response


def transaction_rating():
    """
    Handler top users data by transaction for the last six months
    :return: rating. Example:
    {'rating':
        [{'name': 'Petya', 'price_value': 800.0, 'date': '2023-07-05T00:00:00Z'},
        {'name': 'Vasya', 'price_value': 300.0, 'date': '2023-07-05T00:00:00Z'}]
    }
    """
    wallet_user_table = 'wallet_app_walletuser'
    transaction_table = 'wallet_app_transaction'
    cur_date = date.today() - relativedelta(months=6)
    columns = ['name', 'price_value', 'date']
    request_data = f"""
    SELECT {', '.join(columns)} FROM  {wallet_user_table} 
    JOIN {transaction_table} ON {wallet_user_table}.id = {transaction_table}.user_id
    WHERE {transaction_table}.date > '{cur_date}'
    ORDER BY {transaction_table}.price_value DESC
    LIMIT 10;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(request_data)
            resp = cursor.fetchall()
            return fit_sql_response(resp, columns)
    except Exception as ex:
        logger.error(ex)
        return []

