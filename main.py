import yfinance as yf
import matplotlib.pyplot as plt
import utils as ut
import numpy as np

spy = yf.Ticker("SPY")
print(spy)
"""
returns
<yfinance.Ticker object at 0x1a1715e898>
"""

# get stock info
spy.info

"""
returns:
{
 'quoteType': 'EQUITY',
 'quoteSourceName': 'Nasdaq Real Time Price',
 'currency': 'USD',
 'shortName': 'Microsoft Corporation',
 'exchangeTimezoneName': 'America/New_York',
  ...
 'symbol': 'MSFT'
}
"""

# get historical market data, here max is 5 years.
print(spy.history(period="max"))
print(spy.options)

n = len(spy.options)
rows = int(np.ceil(np.sqrt(n)))
cols = int(n/rows) + (n % rows != 0)


fig, axes = plt.subplots(nrows=rows, ncols=cols)

i = 0
for r in range(rows):
    for c in range(cols):
        if i > len(spy.options):
            break
        opt_date = spy.options[i]
        opt = spy.option_chain(opt_date)
        puts = opt.puts
        puts['break_even'] = ut.put_break_even(puts.strike, puts.lastPrice)
        puts.plot(y='break_even', x='strike', title=opt_date, ax=axes[r,c])
        i += 1

plt.show()





"""
returns:
              Open    High    Low    Close      Volume  Dividends  Splits
Date
1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
...
2019-11-12  146.28  147.57  146.06  147.07    18641600        0.0     0.0
2019-11-13  146.74  147.46  146.30  147.31    16295622        0.0     0.0
"""