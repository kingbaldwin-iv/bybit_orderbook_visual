import asyncio
import os
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import time
from colorama import init
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')
import ccxt.async_support as ccxt  # noqa: E402
from dataclasses import dataclass
init(autoreset=True)
@dataclass
class book:
    order_book :pd.DataFrame
    def normalize_orders(self):
        norm_orders = np.linalg.norm(self.order_book.iloc[:, 1])
        self.order_book['Normalized Amounts'] = self.order_book.iloc[:, 1] / norm_orders
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

def plot(pair):
    print("plotting...")
    plt.ion()
    plt.rcParams['axes.facecolor']='black'
    plt.rcParams['savefig.facecolor']='black'
    start = time.time()
    while True:
        book_p = asyncio.run(bybit_api(pair))
        book_bids = book(pd.DataFrame(book_p['bids'],columns=['Price','Amount']),False)
        book_asks = book(pd.DataFrame(book_p['asks'],columns=['Price','Amount']),True)
        book_bids.normalize_orders()
        book_asks.normalize_orders()
        y_asks = book_asks.order_book['Price']
        y_bids = book_bids.order_book['Price']
        x = [time.time()-start] * len(y_asks)
        s_ask = book_asks.order_book['Normalized Amounts'] * 10
        s_bid = book_bids.order_book['Normalized Amounts'] * 10
        plt.scatter(x, y_asks, color='red',s=s_ask)
        plt.scatter(x, y_bids, color='lime',s=s_bid)
        plt.title(pair)
        plt.draw()
        plt.pause(0.0001)
    plt.show(block=True)
def main():
    pair = input("Enter the pair: ")
    plot(pair)


if __name__ == "__main__":
    main()
