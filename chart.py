import sys

from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QChart, QChartView, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, QDateTime, QTimer, QRect, QPoint, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from typing import Callable
from functools import partial




def run_animation(steps: list[tuple[Callable[[], None], int]]):
    """Tranq - Callable[[], None] takes no arguments and returns nothing"""
    for func, delay in steps:

        timer = QTimer()
        timer.singleShot(delay, func)

class Chart():
    def __init__(self, stock, info_label, window):
        self.chart = QChart()
        self.stock = stock
        self.info_label = info_label
        self.window = window
        self.candles_on_screen = 0
        self.candlestick_high = self.stock.highs[0]
        self.candlestick_low = self.stock.lows[0]
        self.yaxis_lower_range = 0
        self.yaxis_upper_range = 0
        self.y_axis = QValueAxis()
        # create starting candle stick data of 30 candles - line 43
        self.create_candles(self)



    def create_candles(self, chart_window):

        self.stock.stock_series.setName(self.stock.name)
        # setting colour for bull/bear candles
        self.stock.stock_series.setIncreasingColor(QColor(0, 255, 113, 255))
        self.stock.stock_series.setDecreasingColor(QColor(218, 13, 79, 255))

        # creates the initial chart data - currently set to 30 candles and increments self.index by same
        for i in range(30):
            self.add_new_candle(chart_window)

    # Helper function to create a hover handler without using a lambda
    def create_hover_handler(self, cs, idx):
        def handler(hovered):
            # chart_window.update_label(hovered, cs, idx)
            self.update_label(hovered, cs, idx)

        return handler

    def add_new_candle(self, chart_window):

        def lower_and_upper_range(low, high):
            middle = (low + high) / 2
            half_span = (high - low) / 2
            new_half_span = half_span * 1.1
            lower = middle - new_half_span
            upper = middle + new_half_span
            # print(low, high, lower, upper)
            return lower, upper

        if self.stock.index < len(self.stock.dates):
            candlestickSet = QCandlestickSet(self.stock.dates[self.stock.index])
            candlestickSet.setOpen(self.stock.opens[self.stock.index])
            candlestickSet.setHigh(self.stock.highs[self.stock.index])
            candlestickSet.setLow(self.stock.lows[self.stock.index])
            candlestickSet.setClose(self.stock.closes[self.stock.index])

            candlestickSet.hovered.connect(self.create_hover_handler(candlestickSet, self.stock.index))
            self.stock.stock_series.append(candlestickSet)
            self.stock.index += 1
            if self.candles_on_screen < 25:
                self.candles_on_screen += 1

            self.candlestick_high = max(self.stock.highs[self.stock.index - self.candles_on_screen:self.stock.index])
            self.candlestick_low = min(self.stock.lows[self.stock.index - self.candles_on_screen:self.stock.index])

            self.yaxis_lower_range, self.yaxis_upper_range = lower_and_upper_range(self.candlestick_low, self.candlestick_high)
            self.y_axis.setRange(self.yaxis_lower_range, self.yaxis_upper_range)


    def create_view(self):
        """displays the candlestick charts, and sets the legend, axes etc.
        returns chart_view"""
        self.chart.addSeries(self.stock.stock_series)

        # TODO newly generated candlesticks do not have hover-over data
        # creating a arg-less function using partial as run_animation() cannot take funcs with args
        new_candle = partial(self.add_new_candle, self.window)

        self.chart.setTitle(f"{self.stock.name} data from {self.stock.from_date}")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # create X axis and set range
        x_axis = QDateTimeAxis()
        x_axis.setFormat("MMM-yy")
        x_axis.setTitleText("Date")

        min_date = QDateTime.fromSecsSinceEpoch(
            self.stock.dates[0] // 1000)  # this function expects milliseconds
        max_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[-1] // 1000)

        # adds 1 day to start and end so candlesticks don't go up to the borders (visually more pleasing)
        min_date = min_date.addSecs(-3600 * 24)
        max_date = max_date.addSecs(3600 * 24)

        x_axis.setRange(min_date, max_date)

        x_axis.setTickCount(7)
        self.chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.stock.stock_series.attachAxis(x_axis)

        self.y_axis = QValueAxis()
        self.y_axis.setTitleText("Stock Price")
        self.y_axis.setLabelFormat("%.2f")
        # self.chart.setPlotArea(self, QRect(QPointF, self.yaxis_upper_range, QPointF, max_date))
        # self.y_axis.setRange(self.yaxis_lower_range, self.yaxis_upper_range)
        self.chart.addAxis(self.y_axis, Qt.AlignmentFlag.AlignLeft)
        self.stock.stock_series.attachAxis(self.y_axis)

        # make chart legend visible and place at bottom
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # creating the list of steps to pass to run_animation() using the loop below
        animation_list = []
        for i in range(self.stock.index):
            j = (i + 1) * 1000
            animation_list.append((new_candle, j))

        run_animation(animation_list)

        # Create and return chart view
        chart_view = QChartView(self.chart)
        # adding antialiasing
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view


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
