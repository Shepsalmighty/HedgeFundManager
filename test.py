import sys

import yfinance as yf
from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QChart, QChartView, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, QDateTime, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from typing import Callable
from functools import partial



def create_animation(steps: list[tuple[Callable[[], None], int]]):
    """Tranq - Callable[[], None] takes no arguments and returns nothing

    stderr - def create_delayed_function( window ):
                        def handler():
                            add_new_handler( window )
    this function takes one argument and makes a new function that doesn't take arguments,
    but calls a function with the one argument given to create_delayed_function."""

    #TODO - this function should start a timer for each animation step using the corresponding delay
    for func, delay in steps:

        timer = QTimer()  # needs a Qobject and self.chart is one shrug emoji goes here
        timer.singleShot(delay, func)



#TODO - mess wid dis
def create_argless_function(window):
    def argless():
        Stock.add_new_candle
    return argless


class Chart():
    def __init__(self, stock, info_label):
        self.chart = QChart()
        self.stock = stock
        #create starting candle stick data
        self.stock.create_candles(self)
        self.info_label = info_label


    def create_view(self):
        """displays the candlestick charts, and sets the legend, axes etc.

        returns chart_view"""
        self.chart.addSeries(self.stock.stock_series)

        new_candle = partial(self.stock.add_new_candle, window)


        create_animation([(new_candle, 1000), (new_candle, 2000),(new_candle, 3000),(new_candle, 4000),(new_candle, 5000)])

        # def single_candle():
        #     self.stock.add_new_candle(self)
        # #
        # timer = QTimer(self.chart) #needs a Qobject and self.chart is one shrug emoji goes here
        # timer.singleShot(5000, single_candle)

        self.chart.setTitle(f"{self.stock.name} data from {self.stock.from_date}")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # create X axis and set range
        x_axis = QDateTimeAxis()
        x_axis.setFormat("MMM-yy")
        x_axis.setTitleText("Date")

        min_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[0] // 1000)  # this function expects milliseconds
        max_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[-1] // 1000)

        #adds 1 day to start and end so candlesticks don't go up to the borders (visually more pleasing)
        min_date = min_date.addSecs(-3600 * 24)
        max_date = max_date.addSecs(3600 * 24)

        x_axis.setRange(min_date, max_date)

        x_axis.setTickCount(7)
        self.chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.stock.stock_series.attachAxis(x_axis)

        y_axis = QValueAxis()
        y_axis.setTitleText("Stock Price")
        y_axis.setLabelFormat("%.2f")
        self.chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
        self.stock.stock_series.attachAxis(y_axis)

        # make chart legend visible and place at bottom
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # Create and return chart view
        chart_view = QChartView(self.chart)
        #adding antialiasing
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    # creating label when candle stick is moused-over
    def update_label(self, hovered, candlestick_set, index):
        if hovered:
            date = QDateTime.fromMSecsSinceEpoch(self.stock.dates[index]).toString("yyyy-MM-dd")
            open_price = candlestick_set.open()
            close_price = candlestick_set.close()
            high = candlestick_set.high()
            low = candlestick_set.low()

            self.info_label.setText(
                f"Date: {date} | Open: {open_price:.2f} | Close: {close_price:.2f} | High: {high:.2f} | Low: {low:.2f}")
        else:
            self.info_label.setText("Hover over a candlestick to see details")

    # def play_data(self):
    #     if self.index >= len(Stock.dates)

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

    # importing yfinance data as floats to be used by candlestickSet series object
    def create_candles(self, chart_window):

        self.stock_series.setName(self.name)
        #setting colour for bull/bear candles
        self.stock_series.setIncreasingColor(QColor(0, 255, 113, 255))
        self.stock_series.setDecreasingColor(QColor(218, 13, 79, 255))

        #creates the initial chart data - currently set to 30 candles and increments self.index by same
        for i in range(30):
            self.add_new_candle(chart_window)



    def add_new_candle(self, chart_window):

        # Helper function to create a hover handler without using a lambda
        def create_hover_handler(cs, idx):
            def handler(hovered):
                chart_window.update_label(hovered, cs, idx)

            return handler

        if self.index < len(self.dates):
            candlestickSet = QCandlestickSet(self.dates[self.index])
            candlestickSet.setOpen(self.opens[self.index])
            candlestickSet.setHigh(self.highs[self.index])
            candlestickSet.setLow(self.lows[self.index])
            candlestickSet.setClose(self.closes[self.index])

            candlestickSet.hovered.connect(create_hover_handler(candlestickSet, self.index))
            self.stock_series.append(candlestickSet)
            self.index += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    stock = Stock("AAPL", "2024-11-03", "2025-02-08")
    central_widget = QWidget()

    info_label = QLabel("Hover over a candlestick to see details")
    info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # layout stacks the widgets vertically so our stock data is under the candlestick chart
    layout = QVBoxLayout()
    #adding chart_view to central widget
    mychart = Chart(stock, info_label)
    layout.addWidget(mychart.create_view())
    # layout.addWidget(Chart(stock, info_label).create_view())

    # feeding data into the second/lower (candlestick data) box
    layout.addWidget(info_label)
    central_widget.setLayout(layout)

    # set chart to be central widget and set chart size
    window.setCentralWidget(central_widget)
    window.resize(800, 600)
    window.show()



    sys.exit(app.exec())




