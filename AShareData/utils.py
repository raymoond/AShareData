import datetime as dt
import json
from typing import Union, Optional, Sequence

import sqlalchemy as sa
from sqlalchemy.engine.url import URL

DateType = Union[str, dt.datetime, dt.date]

STOCK_EXCHANGES = ['SSE', 'SZSE']
FUTURE_EXCHANGES = ['CFFEX', 'DCE', 'CZCE', 'SHFE', 'INE']
ALL_EXCHANGES = STOCK_EXCHANGES + FUTURE_EXCHANGES
STOCK_INDEXES = {'上证指数': '000001.SH', '深证成指': '399001.SZ', '中小板指': '399005.SZ', '创业板指': '399006.SZ',
                 '上证50': '000016.SH', '沪深300': '000300.SH', '中证500': '000905.SH'}
TRADING_DAYS_IN_YEAR = 252


def date_type2str(date: DateType, delimiter: str = '') -> str:
    formatter = delimiter.join(['%Y', '%m', '%d'])
    return date.strftime(formatter) if not isinstance(date, str) else date


def date_type2datetime(date: str) -> Optional[dt.datetime]:
    if isinstance(date, dt.datetime):
        return date
    if isinstance(date, dt.date):
        return dt.datetime.combine(date, dt.time())
    if isinstance(date, str) & (date not in ['', 'nan']):
        return dt.datetime.strptime(date, '%Y%m%d')


def select_dates(date_list: Sequence[dt.datetime],
                 start_date: DateType = None, end_date: DateType = None) -> Sequence[dt.datetime]:
    if start_date:
        start_date = date_type2datetime(start_date)
        date_list = [it for it in date_list if it >= start_date]

    end_date = date_type2datetime(end_date) if end_date else dt.datetime.now()
    date_list = [it for it in date_list if it <= end_date]
    return date_list


def stock_code2ts_code(stock_code: Union[int, str]) -> str:
    stock_code = int(stock_code)
    return f'{stock_code:06}.SH' if stock_code >= 600000 else f'{stock_code:06}.SZ'


def ts_code2stock_code(ts_code: str) -> str:
    return ts_code.split()[0]


def prepare_engine(config_loc: str) -> sa.engine.Engine:
    with open(config_loc, 'r') as f:
        config = json.load(f)
    url = URL(drivername=config['driver'], host=config['host'], port=config['port'], database=config['database'],
              username=config['username'], password=config['password'],
              query={'charset': 'utf8mb4'})
    return sa.create_engine(url)


def _prepare_example_json(config_loc, example_config_loc) -> None:
    with open(config_loc, 'r') as f:
        config = json.load(f)
    for key in config.keys():
        config[key] = '********' if isinstance(config[key], str) else 0
    with open(example_config_loc, 'w') as fh:
        json.dump(config, fh, indent=4)

# _prepare_example_json('data.json', 'config_example.json')