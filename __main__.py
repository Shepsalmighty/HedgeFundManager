# import sys
# import yfinance as yf
# from PySide6 import Qt
# from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QChart, QChartView, QValueAxis, QDateTimeAxis
# from PySide6.QtCore import Qt, QDateTime
# from PySide6.QtGui import QColor, QPainter
# from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel
import sys
import yfinance as yf
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QChart, QChartView, QValueAxis, QDateTimeAxis
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


class Chart():
    def __init__(self, stock, info_label):
        self.chart = QChart()
        self.stock = stock
        self.stock_series = self.stock.create_candles(self)
        self.info_label = info_label


    def window(self):
        self.chart.addSeries(self.stock_series)
        self.chart.setTitle(f"{self.stock.name} data from {self.stock.from_date}")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # create axes and set range
        x_axis = QDateTimeAxis()
        x_axis.setFormat("MMM-yy")
        x_axis.setTitleText("Date")


        min_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[0] // 1000)  # this function expects milliseconds
        max_date = QDateTime.fromSecsSinceEpoch(self.stock.dates[-1] // 1000)

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
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # Create and return chart view
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        # add chart to a View and add anti-aliasing
        return chart_view

    def update_label(self, hovered, candlestick_set, index):
        if hovered:
            date = QDateTime.fromMSecsSinceEpoch(self.stock.dates[index]).toString("yyyy-MM-dd")
            open_price = candlestick_set.open()
            close_price = candlestick_set.close()
            high = candlestick_set.high()
            low = candlestick_set.low()

            self.info_label.setText(f"Date: {date} | Open: {open_price:.2f} | Close: {close_price:.2f} | High: {high:.2f} | Low: {low:.2f}")
        else:
            self.info_label.setText("Hover over a candlestick to see details")

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


        self.dates = [int(timestamp.timestamp() * 1000) for timestamp in self.stock_data.index]  # Convert to milliseconds
        # self.dates = [int(timestamp.timestamp()) for timestamp in self.stock_data.index]

    # importing yfinance data as floats to be used by candlestickSet series object
    def create_candles(self, chart_window):
        stock_series = QCandlestickSeries()
        stock_series.setName(self.name)
        stock_series.setIncreasingColor(QColor(0, 255, 113, 255))
        stock_series.setDecreasingColor(QColor(218, 13, 79, 255))

        # Helper function to create a hover handler without using a lambda
        def create_hover_handler(cs, idx):
            def handler(hovered):
                chart_window.update_label(hovered, cs, idx)
            return handler
    # def handler(self, hovered):
    #     chart_window.update_label(hovered, cs, idx)
    #         # return handler

        for i in range(len(self.dates)):
            candlestickSet = QCandlestickSet(self.dates[i])
            candlestickSet.setOpen(self.opens[i])
            candlestickSet.setHigh(self.highs[i])
            candlestickSet.setLow(self.lows[i])
            candlestickSet.setClose(self.closes[i])
            # stock_series.append(candlestickSet)

        #mouse-over event handler to show candlestick data
            candlestickSet.hovered.connect(create_hover_handler(candlestickSet, i))
            stock_series.append(candlestickSet)

        return stock_series


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = QMainWindow()
    stock = Stock("AAPL", "2024-12-03", "2025-01-27")
    print(stock.dates[0])
    central_widget = QWidget()
    layout = QVBoxLayout()

    info_label = QLabel("Hover over a candlestick to see details")
    info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(Chart(stock, info_label).window())
    layout.addWidget(info_label)
    central_widget.setLayout(layout)


    # set chart to be central widget and set chart size
    # window.setCentralWidget(Chart(stock, window).window())
    window.setCentralWidget(central_widget)
    window.resize(800, 600)
    window.show()


    sys.exit(app.exec())

# print(Stock("AAPL","2024-12-03", "2025-01-27").create_candles())



#TODO
# #1) DONEZO - Classify this whole shit
# 2) Add mouse hover over (OHLC) + DONE add date x-axis
# 3) play live data
