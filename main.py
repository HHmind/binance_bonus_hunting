import os
import json
from binance import Client

API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
floor_price = float(os.environ.get("floor_price"))
ceil_price = float(os.environ.get("ceil_price"))

# Initialize Binance client
client = Client(API_KEY, SECRET_KEY)

# Get balance from data/balance.json
with open("data/balance.json", "r") as f:
    balance = json.load(f)

def update_balance(new_balance):
    with open("data/balance.json", "w") as f:
        json.dump(new_balance, f)

def truncate(number, decimals=0):
    return int(number * (10 ** decimals)) / (10 ** decimals)

def check_open_order():
    if balance["open_order"]:
        order_status = client.get_order(
            symbol="BUSDUSDT",
            orderId=balance["open_order"]
        )
        if order_status["status"] == "FILLED":
            executed_quantity = float(order_status["executedQty"])
            fees = executed_quantity * 0.00075
            balance["fees"] = truncate(balance["fees"] + fees, 8)

            if order_status["side"] == "BUY":
                balance["BUSD"] = truncate(executed_quantity, 4)
                balance["USDT"] = 0
            elif order_status["side"] == "SELL":
                balance["BUSD"] = 0
                balance["USDT"] = truncate(executed_quantity * float(order_status["price"]), 4)
            balance["open_order"] = None
            update_balance(balance)

    if not balance["open_order"]:
        if balance["BUSD"] == 0:
            order_id = place_order("buy", balance["USDT"], ceil_price)
        elif balance["USDT"] == 0:
            order_id = place_order("sell", balance["BUSD"], floor_price)
        balance["open_order"] = order_id
        update_balance(balance)

def place_order(side, quantity, price):
    if side == "buy":
        quantity = "{:.4f}".format(quantity / price)
    elif side == "sell":
        quantity = "{:.4f}".format(quantity)

    order = client.create_order(
        symbol="BUSDUSDT",
        side=side.upper(),
        type=Client.ORDER_TYPE_LIMIT,
        timeInForce=Client.TIME_IN_FORCE_GTC,
        quantity=quantity,
        price="{:.4f}".format(price)
    )

    return order["orderId"]

check_open_order()
