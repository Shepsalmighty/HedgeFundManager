import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, \
    QMessageBox, QInputDialog
from chart import Chart
from stock import Stock
from game_state import GameState
from buy_sell import BuySell as Trade
from portfolio import Portfolio

# def output():
#     msgBox = QMessageBox()
#     msgBox.setText("Order Size")
#     msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#     msgBox.setDefaultButton(QMessageBox.Ok)
#     msgBox.exec()

def buy_shares():
    i, ok = QInputDialog.getInt(central_widget, "Buy to Open",
                                "Order Size:", 0, 0, 100000000, 10)
    if ok:
        return i
    return 0

def sell_shares():
    i, ok = QInputDialog.getInt(central_widget, "Sell to Close",
                                "Shares to Sell:", 0, 0, 100000000, 10)
    if ok:
        return i
    return 0


if __name__ == "__main__":

    player_game_state = GameState('player_state.json')

    app = QApplication(sys.argv)
    window = QMainWindow()
    #TODO error handling for unknown tickers instead of breaking the program
    # try to avoid exceptions and use monadic errors (tell what the error is instead of throwing the error)
    my_stock = Stock("GOOG", "2024-11-03", "2025-02-08")
    trade = Trade(my_stock, player_game_state)
    cash = Portfolio(player_game_state)
    central_widget = QWidget()

    #creating a second widget that will dispaly candlestick data
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

    # add trade buttons
    button_layout = QHBoxLayout()
    buy_button = QPushButton("Buy")
    sell_button = QPushButton("Sell")
    close_button = QPushButton("Close")
    #formatting the button size with addStretch
    button_layout.addStretch()
    button_layout.addWidget(buy_button)
    # button_layout.addWidget(sell_button)
    button_layout.addWidget(close_button)

    layout.addLayout(button_layout)

    #add button signals when clicked
    #TODO dis vvvv
    # buy_button.clicked.connect(trade.buy_to_open(buy_shares()))
    buy_button.clicked.connect(lambda: trade.buy_to_open(buy_shares()))
    # sell_button.clicked.connect(lambda: trade.sell_to_close(sell_shares()))
    close_button.clicked.connect(lambda: trade.sell_to_close(sell_shares()))



    # set chart to be central widget and set chart size
    window.setCentralWidget(central_widget)
    window.resize(800, 600)
    window.show()



    sys.exit(app.exec())