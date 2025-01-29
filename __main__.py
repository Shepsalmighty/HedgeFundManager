import sys
import yfinance as yf
from PySide6 import Qt
from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QChart, QChartView, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QApplication

app = QApplication(sys.argv)
window = QMainWindow()
chart = QChart()


class Chart():
    def __init__(self, stock):
        self.chart = QChart()
        self.stock = stock
        self.stock_series = self.stock.create_candles()

    def window(self, stock):
        self.chart.addSeries(stock.create_candles())
        self.chart.setTitle(f"{stock.name} data from {stock.from_date}")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # create default axes and set range
        self.chart.createDefaultAxes()

        x_axis = QDateTimeAxis()
        x_axis.setFormat("MMM-yy")
        x_axis.setTitleText("Date")

        min_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[0])
        max_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[-1])

        min_date = min_date.addSecs(-3600 * 24)
        max_date = max_date.addSecs(3600 * 24)

        x_axis.setRange(min_date, max_date)

        x_axis.setTickCount(7)
        self.chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.stock_series.attachAxis(x_axis)

        y_axis = QValueAxis()
        y_axis.setTitleText("Stock Price")
        y_axis.setLabelFormat("%.2f")
        self.chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
        self.stock_series.attachAxis(y_axis)

        # make chart legend visible and place at bottom
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # add chart to a View and add anti-aliasing
        return QChartView(self.chart)  # chartView.setRenderHint(QPainter.Antialiasing)

"""if you get to the mouse stuff, 
u need to use the hover function and connect the hovering over the candlestickset with the window. 
That means if you hover over a candlestickset (one of the bars on a screen) you can call a function 
to display a label of the data u want to represent"""
class Stock():
    def __init__(self, ticker, from_date, to_date):
        self.name = ticker
        self.ticker = yf.Ticker(ticker)
        self.from_date = from_date
        self.to_date = to_date
        self.values = ['Open', 'High', 'Low', 'Close']
        self.stock_data = self.ticker.history(start=self.from_date, end=self.to_date)
        self.opens = self.stock_data["Open"].tolist()
        self.highs = self.stock_data['High'].tolist()
        self.lows = self.stock_data['Low'].tolist()
        self.closes = self.stock_data['Close'].tolist()
        #INFO self.dates int was prev float() but caused issues as a chart func requires ints
        self.dates = [int(timestamp.timestamp()) for timestamp in self.stock_data.index]

    # importing yfinance data as floats to be used by candlestickSet series object
    def create_candles(self):
        stock_series = QCandlestickSeries()
        stock_series.setName(self.name)
        stock_series.setIncreasingColor(QColor(0, 255, 113, 255))
        stock_series.setDecreasingColor(QColor(218, 13, 79, 255))

        for i in range(len(self.dates)):
            candlestickSet = QCandlestickSet(self.dates[i])
            candlestickSet.setOpen(self.opens[i])
            candlestickSet.setHigh(self.highs[i])
            candlestickSet.setLow(self.lows[i])
            candlestickSet.setClose(self.closes[i])

            stock_series.append(candlestickSet)
        return stock_series


apple = Stock("AAPL", "2024-12-03", "2025-01-27")

if __name__ == "__main__":
    # set chart to be central widget and set chart size
    window.setCentralWidget(Chart(apple).window(apple))
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())

# print(Stock("AAPL","2024-12-03", "2025-01-27").create_candles())

# print(apple.closes)

#TODO
# #1) DONEZO - Classify this whole shit
# 2) Add mouse hover over (OHLC) + DONE add date x-axis
# 3) play live data
