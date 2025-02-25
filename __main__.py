import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from chart import Chart
from stock import Stock

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    my_stock = Stock("AAPL", "2024-11-03", "2025-02-08")
    central_widget = QWidget()

    info_label = QLabel("Hover over a candlestick to see details")
    info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # layout stacks the widgets vertically so our stock data is under the candlestick chart
    layout = QVBoxLayout()
    #adding chart_view to central widget
    mychart = Chart(my_stock, info_label, window)
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