import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from chart import Chart
from stock import Stock
from game_state import GameState

if __name__ == "__main__":

    player_game_state = GameState('player_state.json')

    app = QApplication(sys.argv)
    window = QMainWindow()
    #TODO error handling for unknown tickers instead of breaking the program
    # try to avoid exceptions and use monadic errors (tell what the error is instead of throwing the error)
    my_stock = Stock("GOOG", "2024-11-03", "2025-02-08")
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