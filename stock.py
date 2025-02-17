import yfinance
import yfinance as yf
from PySide6.QtCharts import QCandlestickSeries

class Stock():
    def __init__(self, ticker, from_date, to_date):
        self.name = ticker
        self.ticker = yf.Ticker(ticker)
        self.from_date = from_date
        self.to_date = to_date
        self.stock_series = QCandlestickSeries()
        self.stock_data = self.ticker.history(start=self.from_date, end=self.to_date)
        self.opens = self.stock_data["Open"].tolist()
        self.highs = self.stock_data['High'].tolist()
        self.lows = self.stock_data['Low'].tolist()
        self.closes = self.stock_data['Close'].tolist()
        # INFO self.dates int was prev float() but caused issues as a chart func requires ints
        self.dates = [int(timestamp.timestamp() * 1000) for timestamp in self.stock_data.index]  # Convert to milliseconds
        self.index = 0
        self.candlestick_high = 0
        self.candlestick_low = 694200000000
        # print(self.candlestick_low, self.candlestick_high)
