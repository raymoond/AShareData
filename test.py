import json
import logging

from Tushare2MySQL import Tushare2MySQL

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    config_loc = 'config.json'
    with open(config_loc, 'r') as f:
        config = json.load(f)

    tushare_token = config['tushare_token']
    ip, port = config['ip'], config['port']
    username, password = config['username'], config['password']

    tushare_parameters_db = 'param.json'
    downloader = Tushare2MySQL(tushare_token, param_json=tushare_parameters_db)
    downloader.add_mysql_db(ip, port, username, password, db_name='tushare')
    downloader.initialize_db_table()
    # downloader.mysql_writer.db_maintenance()
    # downloader.get_financial(['300146.SZ'])
    # downloader.get_daily_hq(start_date='20080103', end_date='20180105')
    # downloader.update_index_daily()
    # downloader.get_ipo_info()
    # downloader.get_all_stocks()
    # downloader.get_calendar()
    # downloader.get_all_past_names()
    # downloader.get_company_info()
    # print(downloader.select_dates('20180505', '20180612'))

