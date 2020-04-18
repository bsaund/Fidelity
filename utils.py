import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import yfinance as yf
from datetime import datetime


def put_break_even(strike, cost):
    """
    :param strike: strike price of the put option
    :param cost: cost of the put option
    :return: price of stock where this put option will break even
    """
    return strike - cost


def put_profit_ratio(strike, cost, value):
    """
    :param strike: strike price of the put option
    :param cost: cost of the put option
    :param value: value of the stock when exercising the option
    :return: ratio of profit of the put option (between -1 and inf)
    """
    sale = max(strike - value, 0.0)
    return (sale - cost)/cost

def call_profit_ratio(strike, cost, value):
    """
    :param strike: strike price of the option
    :param cost: cost of the call option
    :param value: value of the stock when exercising the option
    :return: ratio of profit of the call option (between -1 and inf)
    """
    sale = max(value - strike, 0.0)
    return (sale - cost)/cost


def plot_puts_graphs_grid(ticker):
    """
    :param ticker:
    :return:
    """
    n = len(ticker.options)
    rows = int(np.ceil(np.sqrt(n)))
    cols = int(n / rows) + (n % rows != 0)

    fig, axes = plt.subplots(nrows=rows, ncols=cols)
    fig.set_size_inches(14, 14)

    i = 0
    for r in range(rows):
        for c in range(cols):
            if i >= len(ticker.options):
                break
            opt_date = ticker.options[i]
            opt = ticker.option_chain(opt_date)
            puts = opt.puts
            puts['break_even'] = put_break_even(puts.strike, puts.lastPrice)
            puts.plot(y='break_even', x='strike', title=opt_date, ax=axes[r, c])
            i += 1
    plt.tight_layout()
    plt.show()


def plot_puts_graphs_overlay(ticker):
    s = yf.Ticker(ticker)
    value = s.info['previousClose']
    """
    :param ticker:
    :return:
    """
    n = len(s.options)

    fig, axes = plt.subplots()
    fig.suptitle('{} puts'.format(ticker))
    axes.set_ylabel('break even stock value ($)')
    axes.set_xlabel('strike ($)')
    fig.set_size_inches(14, 14)

    cmap = matplotlib.cm.get_cmap('plasma')

    i = 0
    for opt_date in s.options:
        opt = s.option_chain(opt_date)
        puts = opt.puts
        puts['break_even'] = put_break_even(puts.strike, puts.lastPrice)
        puts.plot(y='break_even', x='strike', label=opt_date, ax=axes, color=cmap(i/n))
        i += 1
    plt.scatter(x=value,y=value, marker='+', c='k', s=100)
    plt.tight_layout()
    plt.show()


def plot_puts_percentage_gain(ticker, relative_delta):
    """
    :param ticker: (string) ticker symbol
    :param relative_delta: (datetime.relativedelta) the puts closest to now() + relative_delta are plotted
    :return:
    """
    s = yf.Ticker(ticker)
    value = s.info['previousClose']
    nearest = min(s.options, key=lambda x: abs(datetime.strptime(x, "%Y-%m-%d") - (datetime.now() + relative_delta)))
    puts = s.option_chain(nearest).puts

    possible_values = np.linspace(value/2, value*1.1, 100)
    fig, axes = plt.subplots()
    fig.suptitle('Profit ratios for {} put contracts ending on {}'.format(ticker, nearest))
    cmap = matplotlib.cm.get_cmap('plasma')

    n = puts.shape[0]
    for index, row in puts.iterrows():
        prs = [put_profit_ratio(row['strike'], row['lastPrice'], v) for v in possible_values]
        axes.plot(possible_values, prs, label='strike: {}'.format(row['strike']), color=cmap(index/n))
    axes.plot(possible_values, np.zeros(len(possible_values)), ':', color='k', label='break even')
    axes.plot(possible_values, np.ones(len(possible_values)), '--', color='g', label='double money')
    axes.set_ylabel("Profit ratio (profit / cost)")
    axes.set_xlabel("If {} reaches x before {}".format(ticker, nearest))
    plt.scatter(x=value,y=0, marker='+', c='k', s=500)
    axes.legend()
    plt.show()


def plot_calls_percentage_gain(ticker, relative_delta):
    """
    :param ticker: (string) ticker symbol
    :param relative_delta: (datetime.relativedelta) the puts closest to now() + relative_delta are plotted
    :return:
    """
    s = yf.Ticker(ticker)
    value = s.info['previousClose']
    nearest = min(s.options, key=lambda x: abs(datetime.strptime(x, "%Y-%m-%d") - (datetime.now() + relative_delta)))
    calls = s.option_chain(nearest).calls

    possible_values = np.linspace(value * 0.8, value * 1.5, 100)
    fig, axes = plt.subplots()
    fig.suptitle('Profit ratios for {} call contracts ending on {}'.format(ticker, nearest))
    cmap = matplotlib.cm.get_cmap('inferno')

    n = calls.shape[0]
    for index, row in calls.iterrows():
        prs = [call_profit_ratio(row['strike'], row['lastPrice'], v) for v in possible_values]
        axes.plot(possible_values, prs, label='strike: {}'.format(row['strike']), color=cmap(index / n))
    axes.plot(possible_values, np.zeros(len(possible_values)), ':', color='k', label='break even')
    axes.plot(possible_values, np.ones(len(possible_values)), '--', color='g', label='double money')
    axes.set_ylabel("Profit ratio (profit / cost)")
    axes.set_xlabel("If {} reaches x before {}".format(ticker, nearest))
    axes.set_ylim(bottom=-1.5, top=30)
    # plt.scatter(x=value, y=0, marker='+', c='k', s=500)
    axes.axvline(x=value, ymin=0, ymax=.5)
    axes.legend()
    plt.show()


def plot_options_percentage_gain(ticker, delta_time):
    """
    :param ticker: (string) ticker symbol
    :param delta_time: (datetime.relativedelta) the puts closest to now() + relative_delta are plotted
    :return:
    """
    s = yf.Ticker(ticker)
    value = s.info['previousClose']
    nearest = min(s.options,
                  key=lambda x: abs(datetime.strptime(x, "%Y-%m-%d") - (datetime.now() + delta_time)))
    calls = s.option_chain(nearest).calls
    puts = s.option_chain(nearest).puts

    possible_values = np.linspace(value * 0.5, value * 1.5, 100)
    fig, axes = plt.subplots()
    fig.suptitle('Profit ratios for {} options contracts ending on {}'.format(ticker, nearest))


    cmap = matplotlib.cm.get_cmap('cool')
    n = calls.shape[0]
    for index, row in calls.iterrows():
        prs = [call_profit_ratio(row['strike'], row['lastPrice'], v) for v in possible_values]
        axes.plot(possible_values, prs, color=cmap(index / n))

    cmap = matplotlib.cm.get_cmap('hot')
    n = puts.shape[0]
    for index, row in puts.iterrows():
        prs = [put_profit_ratio(row['strike'], row['lastPrice'], v) for v in possible_values]
        axes.plot(possible_values, prs, color=cmap(index / n))


    axes.plot(possible_values, np.zeros(len(possible_values)), ':', color='k', label='break even')
    axes.plot(possible_values, np.ones(len(possible_values)), '--', color='g', label='double money')
    axes.set_ylabel("Profit ratio (profit / cost)")
    axes.set_xlabel("If {} reaches x before {}".format(ticker, nearest))
    axes.set_ylim(bottom=-1.5, top=30)
    # plt.scatter(x=value, y=0, marker='+', c='k', s=500)
    axes.axvline(x=value, ymin=0, ymax=.5)
    axes.legend()
    plt.show()




