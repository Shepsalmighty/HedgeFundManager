import yfinance
import yfinance as yf
from PySide6.QtCharts import QCandlestickSeries, QScatterSeries
from PySide6.QtGui import QColor


class Stock:
    def __init__(self, ticker, from_date, to_date):
        self.name = ticker
        self.ticker = yf.Ticker(ticker)
        self.from_date = from_date
        self.to_date = to_date
        self.stock_series = QCandlestickSeries()
        #create and set size/colour for buy signals
        self.buy_signal_series = QScatterSeries()
        self.buy_signal_series.setMarkerShape(QScatterSeries.MarkerShapeTriangle)
        self.buy_signal_series.setColor(QColor(0, 255, 113, 255))
        self.buy_signal_series.setMarkerSize(15)
        #create and set size/colour for sell signals
        self.sell_signal_series = QScatterSeries()
        self.sell_signal_series.setMarkerShape(QScatterSeries.MarkerShapeTriangle)
        self.sell_signal_series.setColor(QColor(255, 42, 69, 255))
        self.sell_signal_series.setMarkerSize(15)

        self.stock_data = self.ticker.history(start=self.from_date, end=self.to_date)
        self.opens = self.stock_data["Open"].tolist()
        self.highs = self.stock_data['High'].tolist()
        self.lows = self.stock_data['Low'].tolist()
        self.closes = self.stock_data['Close'].tolist()
        # INFO self.dates int was prev float() but caused issues as a chart func requires ints
        self.dates = [int(timestamp.timestamp() * 1000) for timestamp in self.stock_data.index]  # Convert to milliseconds
        self.index = 0


