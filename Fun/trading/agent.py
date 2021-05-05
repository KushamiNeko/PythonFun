import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from functools import cmp_to_key

import numpy as np
from Fun.trading.book import TradingBook
from Fun.trading.order import TransactionOrder
from Fun.trading.statistic import Statistic
from Fun.trading.trade import FuturesTrade
from Fun.trading.transaction import FuturesTransaction
from Fun.utils.helper import random_string
from Fun.utils.jsondb import JsonDB


class OrderProcessor:
    def __init__(self) -> None:
        self._orders: List[TransactionOrder] = []

    def read_orders(self) -> List[TransactionOrder]:
        return self._orders

    def new_order(self, entiry: Dict[str, str]) -> None:
        o = TransactionOrder.from_entity(entiry)
        self._orders.append(o)

    def delete_order(self, index: int) -> None:
        del self._orders[index]

    def delete_all_orders(self) -> None:
        self._orders = []

    def check_orders(
        self, price: float, symbol: Optional[str] = None
    ) -> Optional[List[TransactionOrder]]:
        indexes = []
        orders = []

        for i, order in enumerate(self._orders):
            if symbol is not None:
                if order.symbol() != symbol:
                    continue

            if order.operation() == "+":
                if order.price() <= price:
                    orders.append(order)
                    indexes.append(i)
            elif order.operation() == "-":
                if order.price() >= price:
                    orders.append(order)
                    indexes.append(i)
            else:
                raise ValueError("invalid operation")

        self._orders = [o for i, o in enumerate(self._orders) if i not in indexes]

        if len(orders) == 0:
            return None
        else:
            return orders


class TradingAgent:
    _DB_ADMIN = "admin"

    _DB_TRADING_BOOKS = "books"
    _DB_TRADING_RECORDS = "records"
    _DB_TRADING_ORDERS = "orders"

    _COL_USER = "user"

    _ORDER_PROCESSOR: OrderProcessor = OrderProcessor()

    @classmethod
    def _read_orders(cls) -> List[TransactionOrder]:
        return cls._ORDER_PROCESSOR.read_orders()

    @classmethod
    def _new_order(cls, entity: Dict[str, str]) -> None:
        cls._ORDER_PROCESSOR.new_order(entity)

    @classmethod
    def _delete_order(cls, index: int) -> None:
        cls._ORDER_PROCESSOR.delete_order(index)

    @classmethod
    def _delete_all_orders(cls) -> None:
        cls._ORDER_PROCESSOR.delete_all_orders()

    @classmethod
    def _check_orders(
        cls, price: float, symbol: Optional[str] = None
    ) -> Optional[List[TransactionOrder]]:
        return cls._ORDER_PROCESSOR.check_orders(price, symbol=symbol)

    def __init__(
        self, root: str = "", user_name: str = "default", new_user: bool = False
    ) -> None:
        home = os.getenv("HOME")
        assert home is not None

        if root == "":
            root = os.path.join(home, "Documents/database/market_wizards")

        assert os.path.exists(root)

        self._db = JsonDB(root)

        self._uid = self._login(user_name, new_user)

    def _login(self, user_name: str, new_user: bool) -> str:
        users = self._db.find(
            database=self._DB_ADMIN,
            collection=self._COL_USER,
            query={"name": user_name},
        )

        if users is not None and len(users) == 1:
            uid = users[0].get("uid", None)
            assert uid is not None
            return uid
        else:
            if new_user:
                uid = random_string()

                self._db.insert(
                    self._DB_ADMIN,
                    self._COL_USER,
                    {"name": user_name, "uid": uid},
                )

                return uid
            else:
                raise ValueError("invalid user name")

    def _find_book(self, title: str) -> Optional[TradingBook]:
        books = self.books()
        if books is not None:
            for b in books:
                if b.title() == title:
                    return b

        return None

    @staticmethod
    def _transaction_compare(x: FuturesTransaction, y: FuturesTransaction) -> int:
        if x.datetime() == y.datetime():
            if x.time_stamp() > y.time_stamp():
                return 1
            elif x.time_stamp() < y.time_stamp():
                return -1
            else:
                raise ValueError("find identical time stamp")
        else:
            if x.datetime() > y.datetime():
                return 1
            else:
                return -1

    def books(self) -> Optional[List[TradingBook]]:
        books = self._db.find(
            database=self._DB_TRADING_BOOKS, collection=self._uid, query=None
        )

        if books is not None and len(books) > 0:
            bs = [TradingBook.from_entity(b) for b in books]
            bs.sort(key=lambda b: b.last_modified())
            return bs
        else:
            return None

    def new_order(self, entity: Dict[str, str]) -> None:
        self._new_order(entity)

    def delete_order(self, index: int) -> None:
        self._delete_order(index)

    def delete_all_orders(self) -> None:
        self._delete_all_orders()

    def read_orders(self) -> List[TransactionOrder]:
        return self._read_orders()

    def check_orders(
        self,
        title: str,
        dtime: datetime,
        price: float,
        new_book: bool = False,
        symbol: Optional[str] = None,
    ) -> None:
        orders = self._check_orders(price, symbol=symbol)
        if orders is None or len(orders) == 0:
            return
        else:
            for order in orders:
                if symbol is not None:
                    if order.symbol() != symbol:
                        continue

                entity = order.to_entity()
                entity["datetime"] = dtime.strftime("%Y%m%d")

                self.new_record(f"{title}_{order.account()}", entity, new_book=new_book)

    def new_record(
        self, title: str, entity: Dict[str, str], new_book: bool = False
    ) -> FuturesTransaction:
        assert title != ""

        book = self._find_book(title)
        if book is None:
            if new_book:
                book = TradingBook(title=title)
                self._db.insert(
                    self._DB_TRADING_BOOKS,
                    self._uid,
                    book.to_entity(),
                )
            else:
                raise ValueError(f"book {title} does not exist")

        t = FuturesTransaction.from_entity(entity)
        self._db.insert(self._DB_TRADING_RECORDS, book.index(), t.to_entity())

        return t

    def read_records(self, title: str) -> Optional[List[FuturesTransaction]]:
        assert title != ""

        book = self._find_book(title)
        if book is not None:
            entities = self._db.find(self._DB_TRADING_RECORDS, book.index(), query=None)
            if entities is not None and len(entities) != 0:
                return sorted(
                    [FuturesTransaction.from_entity(e) for e in entities],
                    key=cmp_to_key(self._transaction_compare),
                )

        return None

    def read_all_records(self) -> Optional[List[FuturesTransaction]]:

        books = self.books()
        if books is None or len(books) == 0:
            return None

        ts: List[FuturesTransaction] = []
        for b in books:
            entities = self._db.find(
                f"{self._DB_TRADING_RECORDS}", b.index(), query=None
            )
            if entities is None or len(entities) == 0:
                continue
            else:
                ts.extend([FuturesTransaction.from_entity(e) for e in entities])

        return sorted(
            ts,
            key=cmp_to_key(self._transaction_compare),
        )

    def read_trades(self, title: str) -> Optional[List[FuturesTrade]]:
        ts = self.read_records(title)
        if ts is None:
            return None
        else:
            return self._process_trades(ts)

    def read_statistic(
        self,
        titles: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, str]:
        trades = []

        for title in titles:
            ts = self.read_trades(title)
            if ts is not None and len(ts) > 0:
                trades.extend(ts)

        if start_date is not None and end_date is not None:

            s = datetime.strptime(start_date, "%Y%m%d")
            e = datetime.strptime(end_date, "%Y%m%d")

            trades = [t for t in trades if t.open_time() >= s and t.close_time() <= e]

        if len(trades) > 0:
            return Statistic(trades).to_entity()
        else:
            return {}

    def open_positions(
        self, title: str, dtime: Optional[datetime] = None
    ) -> Optional[List[FuturesTransaction]]:
        transactions = self.read_records(title)
        if transactions is None:
            return None

        if dtime is not None:
            transactions = [t for t in transactions if t.datetime() <= dtime]

        last_time_stamp = 0.0

        trades = self._process_trades(transactions)
        if trades is not None:
            last_date = trades[-1].close_time()
            last_time_stamp = trades[-1].close_time_stamp()

            if dtime is None:
                op = []
                for t in transactions:
                    if t.datetime() > last_date:
                        op.append(t)
                    elif t.datetime() == last_date:
                        if t.time_stamp() > last_time_stamp:
                            op.append(t)
                    else:
                        continue
            else:
                op = []
                for t in transactions:
                    if t.datetime() > last_date:
                        if t.datetime() < dtime:
                            op.append(t)
                    elif t.datetime() == last_date:
                        if t.time_stamp() > last_time_stamp:
                            if t.datetime() < dtime:
                                op.append(t)
                    else:
                        continue

            if len(op) > 0:
                return op
            else:
                return None

        else:
            if dtime is None:
                return transactions
            else:
                op = [t for t in transactions if t.datetime() <= dtime]
                if len(op) > 0:
                    return op
                else:
                    return None

    def open_positions_virtual_pl(
        self, title: str, dtime: datetime, virtual_close: float
    ) -> Optional[Tuple[float, float]]:
        op = self.open_positions(title, dtime=dtime)
        if op is None:
            return None

        virtual_operation = "+"
        if op[0].operation() == "+":
            virtual_operation = "-"

        virtual_t = FuturesTransaction(
            dtime=dtime,
            symbol=op[0].symbol(),
            operation=virtual_operation,
            leverage=abs(sum([float(f"{t.operation()}{t.leverage()}") for t in op])),
            price=virtual_close,
        )

        op.append(virtual_t)

        virtual_trade = FuturesTrade(orders=op)

        return virtual_trade.nominal_pl() * 100.0, virtual_trade.leveraged_pl() * 100.0

    def open_positions_operation(
        self, title: str, dtime: Optional[datetime] = None
    ) -> Optional[str]:
        op = self.open_positions(title, dtime=dtime)

        if op is None:
            return None

        return op[0].operation()

    def open_positions_leverage(
        self, title: str, dtime: Optional[datetime] = None
    ) -> Optional[float]:
        op = self.open_positions(title, dtime=dtime)

        if op is None:
            return None

        else:
            return abs(sum([float(f"{t.operation()}{t.leverage()}") for t in op]))

    def open_positions_nominal_average_opening(
        self, title: str, dtime: Optional[datetime] = None
    ) -> Optional[float]:
        ts = self.open_positions(title, dtime=dtime)
        if ts is None:
            return None

        else:
            return sum(
                [t.price() for t in ts if t.operation() == ts[0].operation()]
            ) / len([t for t in ts if t.operation() == ts[0].operation()])

    def open_positions_leverage_average_opening(
        self, title: str, dtime: Optional[datetime] = None
    ) -> Optional[float]:
        ts = self.open_positions(title, dtime=dtime)
        if ts is None:
            return None

        else:
            return sum(
                [
                    t.price() * t.leverage()
                    for t in ts
                    if t.operation() == ts[0].operation()
                ]
            ) / sum([t.leverage() for t in ts if t.operation() == ts[0].operation()])

    def _process_trades(
        self, transactions: List[FuturesTransaction]
    ) -> Optional[List[FuturesTrade]]:

        transactions.sort(
            key=cmp_to_key(self._transaction_compare),
        )

        ops = np.add.accumulate(
            [float(f"{t.operation()}{t.leverage()}") for t in transactions]
        )

        where = np.argwhere(ops == 0).flatten()

        trades: List[FuturesTrade] = []

        for i, w in enumerate(where):
            s = 0 if i == 0 else where[i - 1] + 1
            e = w + 1

            trades.append(FuturesTrade(transactions[s:e]))

        if len(trades) > 0:
            return trades
        else:
            return None
