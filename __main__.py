import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, \
    QMessageBox, QInputDialog

import chart
from chart import Chart
from stock import Stock
from game_state import GameState
from buy_sell import BuySell as Trade
from portfolio import Portfolio
import threading

def buy_shares():
    order_box = QInputDialog
    mychart.pause_animation.set()
    i, ok = order_box.getInt(central_widget, "Buy to Open",
                                "Order Size:", 0, 1, 100000000, 10)

    # order_box.finished.connect(chart.pause_animation)

    if ok:
        mychart.pause_animation.clear()
        return i
    return 0

def sell_shares():
    order_box = QInputDialog
    i, ok = order_box.getInt(central_widget, "Sell to Close",
                                "Order Size:", 0, 1, 100000000, 10)
    if ok:
        return i
    return 0

def on_buy_button_clicked(trade):
    def inner():
        #trade_size becomes the return value of the order entered in the dialogue box
        trade_size = buy_shares()


        if trade_size > 0:
            trade.buy_to_open(trade_size)
            # update on screen portfolio cash display
            cash.setText(f"$$$ {trade.get_cash()}")
        else:
            print("Invalid or canceled trade size.")


    return inner


def on_sell_button_clicked(trade):
    def inner():
        # trade_size becomes the return value of the order entered in the dialogue box
        trade_size = sell_shares()
        if trade_size > 0:
            trade.sell_to_close(trade_size)
            #update on screen portfolio cash display
            cash.setText(f"$$$ {trade.get_cash()}")
        else:
            print("Invalid or canceled trade size.")


    return inner


def on_close_button_clicked(trade):
    def inner():
        trade_size = buy_shares()
        if trade_size > 0:
            trade.close_position(trade_size)
            # update on screen portfolio cash display
            cash.setText(f"$$$ {trade.get_cash()}")
        else:
            print("Invalid or canceled trade size.")

    return inner


if __name__ == "__main__":
    player_game_state = GameState('player_state.json')
    app = QApplication(sys.argv)
    window = QMainWindow()

    try:
        my_stock = Stock("GOOG", "2024-11-03", "2025-02-08")
    except Exception as e:
        print(f"Error loading stock data: {e}")
        sys.exit(1)

    trade = Trade(my_stock, player_game_state)

    # money = Portfolio(player_game_state)
    central_widget = QWidget()

    layout = QVBoxLayout()
    info_label = QLabel("Hover over a candlestick to see details")
    info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    cash = QLabel(f"$$$ {trade.get_cash()}")
    cash.setAlignment(Qt.AlignmentFlag.AlignCenter)

    mychart = Chart(my_stock, info_label, window, cash)
    chart_view = mychart.create_view()
    layout.addWidget(cash)
    layout.addWidget(chart_view)
    layout.addWidget(info_label)


    button_layout = QHBoxLayout()
    buy_button = QPushButton("Buy")
    sell_button = QPushButton("Sell")
    close_button = QPushButton("Close")
    button_layout.addStretch()
    button_layout.addWidget(buy_button)
    button_layout.addWidget(sell_button)
    button_layout.addWidget(close_button)
    layout.addLayout(button_layout)

    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    #connecting buy/sell/close functions to on screen button press
    buy_button.clicked.connect(on_buy_button_clicked(trade))
    sell_button.clicked.connect(on_sell_button_clicked(trade))
    close_button.clicked.connect(on_close_button_clicked(trade))

    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())