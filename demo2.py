import os

import datetime
import random

from tigeropen.common.consts import Language
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.tiger_open_config import TigerOpenClientConfig
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def get_client_config():
    """
    https://www.itiger.com/openapi/info 开发者信息获取
    :return:
    """
    is_sandbox = False
    client_config = TigerOpenClientConfig(sandbox_debug=is_sandbox)
    client_config.private_key = read_private_key(os.path.expanduser('~/.ssh/tigerbroker_rsa_private_key.pem'))
    client_config.tiger_id = '20150138'
    client_config.account = '20190130215629871'
    client_config.language = Language.en_US
    return client_config


def timestamp_2_str(arr):
    # convert = lambda a: datetime.utcfromtimestamp(a).strftime('%Y-%m-%d')
    temp = []
    for x in arr.tolist():
        temp.append(datetime.datetime.fromtimestamp(x / 1000.0).strftime('%Y-%m-%d'))
    return temp


def random_color():
    color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += color_arr[random.randint(0, 14)]
    return "#" + color


if __name__ == '__main__':
    config = get_client_config()
    quant_client = QuoteClient(config)

    stocks = ['QQQ', 'KWEB']
    data = quant_client.get_bars(stocks)

    years = mdates.YearLocator()  # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots()

    for stock in stocks:
        y1 = data.loc[(data["symbol"] == stock)]
        x_time = timestamp_2_str(y1['time'].values)
        ax.plot(x_time, y1['close'], color=random_color(), label=stock)

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    ax.autoscale_view()
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
    # ax.fmt_ydata = price
    ax.grid(True)
    plt.legend()
    plt.show()

