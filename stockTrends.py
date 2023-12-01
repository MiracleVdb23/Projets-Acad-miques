pip install yahoofinancials

from yahoofinancials import YahooFinancials
from matplotlib import pyplot as plt
import pandas as pd
import datetime
from matplotlib import pyplot as plt, dates as mdates
import numpy as np
import urllib
import sys


if len(sys.argv) != 2:
    print("Invalid no of arguments. We need exactly two arguments!!!")
    sys.exit()
else:

    def get_inputs(url):
        arr = []
        file = urllib.request.urlopen(url)
        for line in file:
            decoded_line = line.decode("utf-8")
            arr.append(decoded_line.split(":")[1].strip())
        return arr[0], arr[1], arr[2], arr[3], arr[4]
    #url = "https://adrianchifu.com/teachings/AMSE/MAG1/stocktrends/stock_parameters.txt"

    url = sys.argv[1]

    name, acronym, begin, end, freq = get_inputs(url)

    yahoo_financials = YahooFinancials(acronym)

    data = yahoo_financials.get_historical_price_data(begin, end, freq)

    def get_vals(data):
        high = [x['high'] for x in data['ETH-USD']['prices']]
        low = [x['low'] for x in data['ETH-USD']['prices']]
        open = [x['open'] for x in data['ETH-USD']['prices']]
        close = [x['close'] for x in data['ETH-USD']['prices']]
        date = [x['formatted_date'] for x in data['ETH-USD']['prices']]
        
        return high, low, open, close, date

    high, low, open, close, dates = get_vals(data)

    x_dates = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in dates]

    plt.rcParams["figure.figsize"] = (10,10)

    plt.xlabel('Date')
    plt.ylabel('Price')

    ax = plt.gca()
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)
    locator = mdates.DayLocator(interval=7)
    ax.xaxis.set_major_locator(locator)

    plt.plot(x_dates, open, label = 'Open Price')
    plt.plot(x_dates, close, label = 'Close Price')
    plt.plot(x_dates, high, ':', label = 'High Price', )
    plt.plot(x_dates, low, ':', label = 'Low Price', )
    plt.xticks(rotation=90)
    plt.title(f'Stock prices for {name}')
    ax.yaxis.set_major_formatter('{x:.0f}$')
    plt.yticks(range(2054,5055,250))
    plt.ylim(1900,5100)
    # plt.yticks(np.arange(min(low), max(high), 250))

    plt.tight_layout()
    plt.legend()
    plt.show()
