import os
import re
from typing import Any, Dict, List, cast, Tuple

from flask import request
from fun.trading.agent import TradingAgent

_ROOT = os.path.join(
    # cast(str, os.getenv("HOME")), "Documents", "database", "testing", "json"
    cast(str, os.getenv("HOME")),
    "Documents",
    "database",
    "market_wizards",
)


class TradeHandler:
    def _long_short_trading_adjustment(
        self,
        agent: TradingAgent,
        entity: Dict[str, str],
        allow_negative_leverage: bool = False,
    ) -> Dict[str, str]:

        title = entity["book"]
        account = entity["account"]
        book = f"{title}_{account}"

        entity["book"] = book

        return entity

    def _long_short_entity_adjustment(
        self, entities: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:

        return entities

    def _new_market_order(self) -> Dict[str, str]:
        entity = request.get_json()
        agent = TradingAgent(root=_ROOT, new_user=True)

        # entity = self._long_short_trading_adjustment(agent=agent, entity=entity)

        ts = agent.new_record(entity["book"], entity, new_book=True)

        return ts.to_entity()

    def _new_stop_order(self) -> Dict[str, List[Dict[str, str]]]:
        entity = request.get_json()
        agent = TradingAgent(root=_ROOT, new_user=True)

        # entity = self._long_short_trading_adjustment(agent=agent, entity=entity)

        agent.new_order(entity)

        return self._read_stop_orders()

    def _delete_stop_order(self) -> Dict[str, List[Dict[str, str]]]:
        index = request.args.get("index")
        if index is None or index == "":
            raise ValueError("invalid order index")

        if re.match(r"^\d+$", index) is None:
            raise ValueError("invalid order index")

        assert index is not None and len(index) > 0

        agent = TradingAgent(root=_ROOT, new_user=True)
        agent.delete_order(int(index))

        return self._read_stop_orders()

    def _read_stop_orders(self) -> Dict[str, List[Dict[str, str]]]:
        agent = TradingAgent(root=_ROOT, new_user=True)
        entities = [o.to_entity() for o in agent.read_orders()]

        # entities = self._long_short_entity_adjustment(entities)

        return {"data": entities}

    def _statistic(self) -> Dict[str, str]:
        pass

    def response_order(self) -> Any:

        if request.method == "POST":

            order = request.args.get("order")
            assert order in ("market", "stop")

            if order == "market":
                return self._new_market_order()
            elif order == "stop":
                return self._new_stop_order()
            else:
                raise ValueError(f"invalid order type {order}")

        elif request.method == "GET":
            return self._read_stop_orders()

        elif request.method == "DELETE":
            return self._delete_stop_order()

        else:
            return "invalid method"

    def response_statistic(self) -> Any:
        function = request.args.get("function")

        assert function in ("books", "statistic")

        if function == "books":
            agent = TradingAgent(root=_ROOT, new_user=True)
            books = agent.books()
            if books is None or len(books) == 0:
                return {"data": []}
            else:
                return {"data": [b.to_entity()["title"] for b in books]}

        elif function == "statistic":
            titles = request.args.get("titles", None)
            assert titles is not None

            start_date = request.args.get("startDate", None)
            end_date = request.args.get("endDate", None)

            start_date = None if start_date == "" else start_date
            end_date = None if end_date == "" else end_date

            titles = titles.split(",")
            agent = TradingAgent(root=_ROOT, new_user=True)
            return agent.read_statistic(
                titles, start_date=start_date, end_date=end_date
            )

        else:
            return "invalid function"
