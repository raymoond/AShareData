import unittest

from AShareData.DateUtils import date_type2datetime
from AShareData.DBInterface import MySQLInterface
from AShareData.config import prepare_engine


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        config_loc = 'config.json'
        engine = prepare_engine(config_loc)
        set_global_config('config.json')
        self.db_interface = MySQLInterface(engine)

    def test_read_data(self):
        table_name = '合并资产负债表'
        factor_name = '期末总股本'
        start_date = date_type2datetime('20190101')
        end_date = date_type2datetime('20190101')
        report_period = date_type2datetime('20181231')
        print(self.db_interface.read_table(table_name, factor_name).head())
        print(self.db_interface.read_table(table_name, factor_name, start_date=start_date, end_date=end_date).head())
        print(self.db_interface.read_table(table_name, factor_name, start_date=start_date).head())
        print(self.db_interface.read_table(table_name, factor_name, report_period=report_period).head())

    def test_calendar(self):
        self.db_interface.read_table('交易日历')

    def test_db_timestamp(self):
        table_name = '合并资产负债表'
        print(self.db_interface.get_latest_timestamp(table_name))


if __name__ == '__main__':
    unittest.main()
