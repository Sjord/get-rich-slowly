import sys
import matplotlib.pyplot as plt
import schemes
from models import Fund


fn = sys.argv[1]
fund = Fund.load(fn)

prices = [d for d in fund.prices]
e = schemes.Ema()
e.updateAll(prices[0:1])
shorts = []
longs = []
for p in prices:
    e.update(p)
    shorts.append(e.emaShort)
    longs.append(e.emaLong)

dates = [d.date for d in prices]
pricepoints = [d.price for d in prices]

plt.plot(dates, pricepoints, 'b-',
         dates, shorts, 'r-',
         dates, longs, 'g-')
plt.show()
