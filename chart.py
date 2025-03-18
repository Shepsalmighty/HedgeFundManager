import time
from typing import Callable

from PySide6.QtCharts import QCandlestickSet, QChart, QChartView, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, QDateTime, QTimer
from PySide6.QtGui import QColor, QPainter
import threading


class Animation:
    def __init__(self, steps: list[tuple[Callable[[], None], float]]):
        """Callable[[], None] takes no arguments and returns nothing
                takes our animation step (new candlesticks) and a time delay"""
        self.steps = steps
        # self.timer = QTimer()
        # self.pause_animation = threading.Event()
        self.thread = None
        self.__pause_lock = threading.Lock()




    def __run(self):
        """ this function runs in the separate animation thread and actually executes things """
        # where the sleep happens, loop that goes through all the steps and uses sleep() to ensure
        # they are executed at the right time
        for func, delay in self.steps:
            # start_time = time.time()
            time.sleep(delay)
            #creating a lock/unlock cycle interrupted by pause() and resume() calls in buy window - pausing animation
            with self.__pause_lock:
                func()


    def join(self):
        """ waits for the animation to complete or instantly returns if it is not started/running """
        # joins threads once animation is completed
        if self.thread:
            self.thread.join()

    def start(self):
        """ starts a new thread that executes the specified steps at the right time """
        # create a new thread that executes all the specified animation steps and store thread-handle
        self.thread = threading.Thread(target=self.__run)
       # start the animation thread
        self.thread.start()


    def pause(self):
        """ pauses the timer thread that was started using the start() method
        (if no timer is running, this method does nothing) """

        if self.thread:
            self.__pause_lock.acquire()

        # if self.thread:
        # #INFO first attempt at getting the god damn animation going again >.<
        #     self.pause.set()

    def resume(self):
        """resumes a paused timer thread as if it was exactly at the point in time that it was paused at
        (does nothing if no paused timer thread exists)"""

        if self.thread:
            self.__pause_lock.release()



class Chart:

    def __init__(self, stock, info_label, window, cash):
        """
        :param stock: stock data from yfinance - from ``stock.py``
        :param window: inherited from ``__main__`` see QMainWindow
        """

        self.chart = QChart()
        self.stock = stock
        self.cash = cash
        self.info_label = info_label
        self.window = window
        self.candles_on_screen = 0
        self.candlestick_high = self.stock.highs[0]
        self.candlestick_low = self.stock.lows[0]
        self.yaxis_lower_range = 0
        self.yaxis_upper_range = 0
        self.y_axis = QValueAxis()
        self.animation = None
        # create starting candle stick data of 30 candles - line 43
        self.create_candles()
        # event thread to stop/start candle stick animations while an order is being placed



    def create_candles(self):
        self.stock.stock_series.setName(self.stock.name)
        # setting colour for bull/bear candles
        self.stock.stock_series.setIncreasingColor(QColor(0, 255, 113, 255))
        self.stock.stock_series.setDecreasingColor(QColor(218, 13, 79, 255))

        # creates the initial chart data - currently set to 30 candles and increments self.stock.index by same
        for i in range(30):
            self.add_new_candle()

    # Helper function to create a hover handler without using a lambda
    def create_hover_handler(self, cs, idx):
        def handler(hovered):
            self.update_label(hovered, cs, idx)

        return handler

    def add_new_candle(self):

        # used to create the offset for our Y-axis upper and lower range candles see 76-78
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


            self.yaxis_lower_range, self.yaxis_upper_range = lower_and_upper_range(self.candlestick_low,
                                                                                   self.candlestick_high)
            #updates y_axis to the candle high/low of the currently shown candles
            self.y_axis.setRange(self.yaxis_lower_range, self.yaxis_upper_range)

    def create_view(self):
        """displays the candlestick charts, and sets the legend, axes etc.
        returns chart_view"""
        self.chart.addSeries(self.stock.stock_series)

        self.chart.setTitle(f"{self.stock.name} data from {self.stock.from_date}")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # create X axis and set range
        x_axis = QDateTimeAxis()
        x_axis.setFormat("MMM-yy")
        x_axis.setTitleText("Date")

        min_date = QDateTime.fromSecsSinceEpoch(
            self.stock.dates[0] // 1000)  # this function expects milliseconds
        max_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[-1] // 1000)

        # adds leading/trailing space in "days" so candlesticks don't go up to the borders (visually more pleasing)
        min_date = min_date.addSecs(-7200 * 24)
        max_date = max_date.addSecs(3600 * 24)

        x_axis.setRange(min_date, max_date)

        #setting the value spacing of the x-axis to 7 - TickCount(7)
        x_axis.setTickCount(7)
        self.chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.stock.stock_series.attachAxis(x_axis)

        self.y_axis = QValueAxis()
        self.y_axis.setTitleText("Stock Price")
        self.y_axis.setLabelFormat("%.2f")
        self.chart.addAxis(self.y_axis, Qt.AlignmentFlag.AlignLeft)
        self.stock.stock_series.attachAxis(self.y_axis)

        # make chart legend visible and place at bottom
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # creating the list of steps to pass to run_animation() using the loop below
        animation_list = []
        for i in range(self.stock.index):
            # j = (i + 1) * 1000
            #set time interval to 1.5 sec instead of using J as J was increasing time interval exponentionally
            animation_list.append((self.add_new_candle, 1.5))


        # for i in range(self.stock.index):
        #     for func, delay in animation_list:
        #         # self.timer.start()
        #         j = (i + 1) * 1000
        #         self.add_new_candle()
        #         time.sleep(j)

        self.animation = Animation(animation_list)
        self.animation.start()

        # Create and return chart view with antiailiasing
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

# updates the OHLC data in a new widget if the candle is moused over
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

