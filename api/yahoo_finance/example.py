
import pandas as pd
import matplotlib.pyplot as plt
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

share_data = "4755.T"
fig, ax = plt.subplots(1, 1, figsize=(16, 8))

my_share = share.Share(share_data)
try:
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR, 2,
                                          share.FREQUENCY_TYPE_MONTH, 1)
    df = pd.DataFrame(symbol_data.values(), index=symbol_data.keys()).T
    df.timestamp = pd.to_datetime(df.timestamp, unit='ms')
    df.index = pd.DatetimeIndex(df.timestamp, name='timestamp').tz_localize('UTC').tz_convert('Asia/Tokyo')

    # ax[i].set_title( "TSE {} ({})".format(company_name, company_code))
    ax.plot(df.index, df.close, 'o-')
    ax.grid(True)
    ax.set_ylabel("Stock Price [Yen]")
    ax.label_outer()
except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)


plt.show()


