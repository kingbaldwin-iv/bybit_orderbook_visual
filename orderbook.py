import asyncio
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import ccxt.async_support as ccxt  # noqa: E402
from dataclasses import dataclass
@dataclass
class book:
    order_book :pd.DataFrame
    def normalize_orders(self):
        norm_orders = np.linalg.norm(self.order_book.iloc[:, 1])
        self.order_book['Normalized Amounts'] = self.order_book.iloc[:, 1] / norm_orders
        self.order_book['size plot'] = (self.order_book['Normalized Amounts'] * 10) ** 2.5
        return self.order_book
async def bybit_api(pair):
    exchange = ccxt.bybit({})
    try:
        orderbook = await exchange.fetch_order_book(pair)
        await exchange.close()
        return orderbook
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e
def plot(pair, duration):
    print("plotting...")
    plt.ioff()
    plt.rcParams['axes.facecolor']='black'
    plt.rcParams['savefig.facecolor']='black'
    start = time.time()
    d_time = 0
    while d_time<duration:
        book_p = asyncio.run(bybit_api(pair))
        book_bids = book(pd.DataFrame(book_p['bids'],columns=['Price','Amount']))
        book_asks = book(pd.DataFrame(book_p['asks'],columns=['Price','Amount']))
        book_bids.normalize_orders()
        book_asks.normalize_orders()
        d_time = time.time()-start
        x = [d_time] * len(book_bids.order_book['Price'])
        plt.scatter(x, book_asks.order_book['Price'], c=book_asks.order_book['size plot'], cmap='autumn_r',s=book_asks.order_book['size plot'])
        plt.scatter(x, book_bids.order_book['Price'], c=book_bids.order_book['size plot'], cmap='winter_r',s=book_bids.order_book['size plot'])
        plt.title(pair)
        plt.draw()
        file_name = f'{pair}-plot.png'
        file_name = file_name.replace('/', '_')
        plt.savefig(file_name)
def main():
# -------------------------#
    pair = 'DOGEUSDT'#######
    duration = 36000########
#--------------------------#
    plot(pair.upper(),duration)
    print('success')

if __name__ == "__main__":
    main()
