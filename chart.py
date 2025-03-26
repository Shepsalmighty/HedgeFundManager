import time
from collections import deque
from typing import Callable

from PySide6.QtCharts import QCandlestickSet, QChart, QChartView, QValueAxis, QDateTimeAxis, QScatterSeries
from PySide6.QtCore import Qt, QDateTime, QObject, Signal
from PySide6.QtGui import QColor, QPainter
import threading


class Animation(QObject):
    execute_step = Signal(object)

    def __init__(self, steps: list[tuple[Callable[[], None], float]]):
        """Callable[[], None] takes no arguments and returns nothing
                takes our animation step (new candlesticks) and a time delay"""
        super().__init__()
        self.steps: list[tuple[Callable[[], None], float]] = steps
        self.thread1: threading.Thread | None = None
        self.__pause_lock: threading.Lock = threading.Lock()
        self.execute_step.connect(lambda func: func())

    def __run(self):
        """ this function runs in the separate animation thread and actually executes things """
        # where the sleep happens, loop that goes through all the steps and uses sleep() to ensure
        # they are executed at the right time
        for func, delay in self.steps:
            time.sleep(delay)
            # creating a lock/unlock cycle interrupted by pause() and resume() calls in buy window - pausing animation
            with self.__pause_lock:
                self.execute_step.emit(func)

    def join(self):
        """ waits for the animation to complete or instantly returns if it is not started/running """
        # joins threads once animation is completed
        if self.thread1:
            self.thread1.join()

    def start(self):
        """ starts a new thread that executes the specified steps at the right time """
        # create a new thread that executes all the specified animation steps and store thread-handle
        self.thread1 = threading.Thread(target=self.__run)
        # start the animation thread
        self.thread1.start()

    def pause(self):
        """ pauses the timer thread that was started using the start() method
        (if no timer is running, this method does nothing) """
        if self.thread1:
            self.__pause_lock.acquire()

    def resume(self):
        """resumes a paused timer thread as if it was exactly at the point in time that it was paused at
        (does nothing if no paused timer thread exists)"""
        if self.thread1:
            self.__pause_lock.release()


class Chart:

    def __init__(self, stock, info_label, window, cash):
        """
        :param stock: stock data from yfinance - from ``stock.py``
        :param window: inherited from ``__main__`` see QMainWindow
        """
        # chart instance for candle sticks
        self.chart: QChart = QChart()
        self.stock = stock
        self.cash = cash
        self.info_label = info_label
        self.window = window
        self.candle_deque = deque(maxlen=30)
        self.candles_on_screen: int = 0
        self.candlestick_high = self.stock.highs[0]
        self.candlestick_low = self.stock.lows[0]
        #create x_axis and set legend
        self.x_axis: QDateTimeAxis = QDateTimeAxis()
        self.x_axis.setFormat("MMM-yy")
        self.x_axis.setTitleText("Date")
        # mark 7 dates on x_axis - TickCount(7)
        self.x_axis.setTickCount(7)
        #create y_axis and set starting ranges
        self.y_axis: QValueAxis = QValueAxis()
        self.yaxis_lower_range = 0
        self.yaxis_upper_range = 0
        # event thread to stop/start candle stick animations while an order is being placed
        self.animation: Animation | None = None
        #vars for later
        self.day_in_seconds = 86400
        self.off_set = 3
        # create starting candle stick data of 30 candles - line 43
        self.create_candles()


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

        if self.stock.index >= len(self.candle_deque):
            candlestickSet = QCandlestickSet(self.stock.dates[self.stock.index])
            candlestickSet.setOpen(self.stock.opens[self.stock.index])
            candlestickSet.setHigh(self.stock.highs[self.stock.index])
            candlestickSet.setLow(self.stock.lows[self.stock.index])
            candlestickSet.setClose(self.stock.closes[self.stock.index])

            candlestickSet.hovered.connect(self.create_hover_handler(candlestickSet, self.stock.index))

            if len(self.candle_deque) == 30:
                oldest_set = self.candle_deque.popleft()
                self.stock.stock_series.remove(oldest_set)

            self.candle_deque.append(candlestickSet)
            self.stock.stock_series.append(candlestickSet)
            self.stock.index += 1
            if self.candles_on_screen < 25:
                self.candles_on_screen += 1


            # self.candlestick_high = max(self.stock.highs[self.stock.index - self.candles_on_screen:self.stock.index])
            # self.candlestick_low = min(self.stock.lows[self.stock.index - self.candles_on_screen:self.stock.index])
            candle_high = [c.high() for c in self.candle_deque]
            candle_low = [c.low() for c in self.candle_deque]

            #if no values fetched from deque - 0 becomes default value
            self.candlestick_high = max(candle_high) if candle_high else 0
            self.candlestick_low = min(candle_low) if candle_low else 0

            self.yaxis_lower_range, self.yaxis_upper_range = lower_and_upper_range(self.candlestick_low,
                                                                                   self.candlestick_high)
            # updates y_axis to the candle high/low of the currently shown candles
            self.y_axis.setRange(self.yaxis_lower_range, self.yaxis_upper_range)

            min_date = QDateTime.fromSecsSinceEpoch(
                self.stock.dates[self.stock.index - self.candles_on_screen] //1000)
            max_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[self.stock.index - 1] // 1000)

            # add leading/trailing space in "days" to the chart
            min_date = min_date.addSecs(-(self.off_set * 3) * self.day_in_seconds)
            max_date = max_date.addSecs(self.off_set * self.day_in_seconds)

            self.x_axis.setRange(min_date, max_date)


    def create_view(self):
        """displays the candlestick charts, and sets the legend, axes etc.
        returns chart_view"""
        self.chart.addSeries(self.stock.stock_series)
        self.chart.addSeries(self.stock.buy_signal_series)
        self.chart.addSeries(self.stock.sell_signal_series)

        self.chart.setTitle(f"{self.stock.name} data from {self.stock.from_date}")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)


        self.chart.addAxis(self.x_axis, Qt.AlignmentFlag.AlignBottom)
        self.stock.stock_series.attachAxis(self.x_axis)
        self.stock.buy_signal_series.attachAxis(self.x_axis)
        self.stock.sell_signal_series.attachAxis(self.x_axis)

        self.y_axis = QValueAxis()
        self.y_axis.setTitleText("Stock Price")
        self.y_axis.setLabelFormat("%.2f")
        self.chart.addAxis(self.y_axis, Qt.AlignmentFlag.AlignLeft)
        self.stock.stock_series.attachAxis(self.y_axis)
        self.stock.buy_signal_series.attachAxis(self.y_axis)
        self.stock.sell_signal_series.attachAxis(self.y_axis)

        # make chart legend visible and place at bottom
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # creating the list of steps to pass to run_animation() using the loop below
        animation_list = []
        for i in range(len(self.stock.dates) - self.stock.index):
            # set time interval to 1.5 sec instead of using J as J was increasing time interval exponentionally
            animation_list.append((self.add_new_candle, 0.5))

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



