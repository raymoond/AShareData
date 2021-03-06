import unittest

from AShareData import set_global_config, TradingCalendar
from AShareData.Factor import *
from AShareData.Tickers import *
from AShareData.utils import StockSelectionPolicy


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        set_global_config('config.json')
        self.db_interface = get_db_interface()
        self.calendar = TradingCalendar()
        self.start_date = dt.datetime(2020, 12, 1)
        self.end_date = dt.datetime(2020, 12, 18)
        self.ids = ['000001.SZ', '000002.SZ']
        # self.ids = StockTickers().ticker(dt.date(2005, 1, 1))
        self.close = ContinuousFactor('股票日行情', '收盘价', self.db_interface)
        self.adj = CompactFactor('复权因子', self.db_interface)

    def test_compact_record_factor(self):
        compact_factor = CompactFactor('证券名称', self.db_interface)
        compact_factor.data = compact_factor.data.map(lambda x: 'PT' in x or 'ST' in x or '退' in x)
        compact_record_factor = CompactRecordFactor(compact_factor, 'ST')
        print(compact_record_factor.get_data(date=dt.datetime(2015, 5, 15)))

    def test_compact_factor(self):
        compact_factor = CompactFactor('证券名称', self.db_interface)
        print(compact_factor.get_data(dates=[dt.datetime(2015, 5, 15)]))
        policy = StockSelectionPolicy(select_st=True)
        print(compact_factor.get_data(dates=[dt.datetime(2015, 5, 15)], ticker_selector=StockTickerSelector(policy)))

    def test_industry(self):
        print('')
        industry_factor = IndustryFactor('中信', 2, self.db_interface)
        print(industry_factor.list_constitutes(dt.datetime(2019, 1, 7), '白酒'))
        print('')
        print(industry_factor.all_industries)

    def test_latest_accounting_factor(self):
        f = LatestAccountingFactor('未分配利润', self.db_interface)
        a = f.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(a)

    def test_latest_quarter_report_factor(self):
        f = LatestQuarterAccountingFactor('未分配利润', self.db_interface)
        a = f.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(a)

    def test_yearly_report_factor(self):
        f = YearlyReportAccountingFactor('未分配利润', self.db_interface)
        ids = list(set(self.ids) - set(['600087.SH', '600788.SH', '600722.SH']))
        a = f.get_data(start_date=self.start_date, end_date=self.end_date, ids=ids)
        print(a)

    def test_qoq_report_factor(self):
        f = QOQAccountingFactor('未分配利润', self.db_interface)
        a = f.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(a)

    def test_yoy_period_report_factor(self):
        f = YOYPeriodAccountingFactor('未分配利润', self.db_interface)
        a = f.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(a)

    def test_yoy_quarter_factor(self):
        f = YOYQuarterAccountingFactor('未分配利润', self.db_interface)
        a = f.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(a)

    def test_ttm_factor(self):
        f = TTMAccountingFactor('营业总收入', self.db_interface)
        a = f.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(a)

    def test_index_constitute(self):
        index_constitute = IndexConstitute(self.db_interface)
        print(index_constitute.get_data('000300.SH', '20200803'))

    def test_sum_factor(self):
        sum_hfq = self.close + self.adj
        sum_hfq_close_data = sum_hfq.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(sum_hfq_close_data)
        uni_sum = self.close + 1
        print(uni_sum.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids))

    def test_mul_factor(self):
        hfq = self.close * self.adj
        hfq_close_data = hfq.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(hfq_close_data)

    def test_factor_pct_change(self):
        hfq = self.close * self.adj
        hfq_chg = hfq.pct_change()
        pct_chg_data = hfq_chg.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(pct_chg_data)

    def test_factor_max(self):
        f = self.adj.max()
        f_max = f.get_data(start_date=self.start_date, end_date=self.end_date, ids=self.ids)
        print(f_max)


if __name__ == '__main__':
    unittest.main()
