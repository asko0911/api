
import pprint
import sys
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from search_symbol import total_code_list, total_company_list, total_country_list

def main(code, company, country):
    my_share = share.Share(code)
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR, 2,
                                            share.FREQUENCY_TYPE_DAY, 1)
        df = pd.DataFrame(symbol_data.values(), index=symbol_data.keys()).T
        df.timestamp = pd.to_datetime(df.timestamp, unit='ms')
        df.index = pd.DatetimeIndex(df.timestamp, name='timestamp')

    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    after_covid19 = df[(df.index >= dt.datetime(2020,11,1)) & (df.index <= dt.datetime(2021,4,30))]
    after_covid19 = round(after_covid19.close.mean())
    before_covid19 = df[(df.index >= dt.datetime(2019,6,1)) & (df.index <= dt.datetime(2019,12,31))]
    before_covid19 = round(before_covid19.close.mean())
    ratio = round(after_covid19 / before_covid19, 2)

    print("code: {}. company: {}. country: {}".format(code, company, country))
    print(before_covid19, after_covid19, ratio)
    stock_df.loc[i] = [code, company, country, before_covid19, after_covid19, ratio]

stock_df = pd.DataFrame(columns=['シンボル', '企業名', '国名', 'コロナ前平均', 'コロナ後平均', '成長率'])
for i in range(len(total_code_list)):
    try:
        main(total_code_list[i], total_company_list[i], total_country_list[i])
    except Exception as e:
        print(e)

stock_df.to_csv("stock_world.csv", encoding='utf_8_sig', index=False)
print(stock_df)



