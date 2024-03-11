import asyncio, time, numpy as np, pandas as pd, matplotlib,ccxt.async_support as ccxt ,dataclasses
matplotlib.use('Agg')
import matplotlib.pyplot as plt
@dataclasses.dataclass
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
        plt.savefig(f'{pair}-plot.png')
pair = 'DOGEUSDT'#######
duration = 36000########
plot(pair.upper(),duration)
