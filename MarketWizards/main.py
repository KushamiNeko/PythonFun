import sys
import traceback

from flask import Flask
from flask_cors import cross_origin

from fun.utils import colors, pretty
from happy.market_wizards.handlers.chart import ChartHandler
from happy.market_wizards.handlers.trade import TradeHandler

app = Flask(__name__)


@app.route("/")
def welcome():
    return "welcome to the market wizards charts reader api"


@app.route("/service/chart", methods=["GET"])
@cross_origin(allow_headers=["Content-Type"])
def chart():
    try:
        return ChartHandler().response()
    except (ValueError, IndexError, NotImplementedError, AssertionError) as err:
        info = sys.exc_info()
        traceback.print_tb(info[2])
        pretty.color_print(
            colors.PAPER_RED_500, f"{type(info[1]).__name__}: {str(info[1])}"
        )
        return {"error": f"{type(err)}: {err}"}


@app.route("/service/trade/order", methods=["GET", "POST", "DELETE"])
@cross_origin(allow_headers=["Content-Type"])
def trade_order():
    try:
        return TradeHandler().response_order()
    except (ValueError, IndexError, NotImplementedError, AssertionError) as err:
        info = sys.exc_info()
        traceback.print_tb(info[2])
        pretty.color_print(
            colors.PAPER_RED_500, f"{type(info[1]).__name__}: {str(info[1])}"
        )
        return {"error": f"{type(err)}: {err}"}


@app.route("/service/trade/statistic", methods=["GET"])
@cross_origin(allow_headers=["Content-Type"])
def trade_statistic():
    try:
        return TradeHandler().response_statistic()
    except (ValueError, IndexError, NotImplementedError, AssertionError) as err:
        info = sys.exc_info()
        traceback.print_tb(info[2])
        pretty.color_print(
            colors.PAPER_RED_500, f"{type(info[1]).__name__}: {str(info[1])}"
        )
        return {"error": f"{type(err)}: {err}"}


if __name__ == "__main__":
    # app.run(debug=True, threaded=True, host="192.168.0.11")
    app.run(debug=True, threaded=True)
