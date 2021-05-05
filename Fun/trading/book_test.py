import time
import unittest

from Fun.trading.book import TradingBook
from Fun.utils.testing import parameterized


class TestBook(unittest.TestCase):
    @parameterized(
            [
                {"title": "", "index": ""},
                {"title": "", "index": "hello"},
                {"title": "hello", "index": "[]"},
                {"title": "hello", "index": "hello,;$"},
                {"title": "hello", "index": "098,;$"},
            ]
    )
    def test_init_invalid(self, title, index):
        with self.assertRaises(ValueError):
            TradingBook(
                    title=title, index=index,
            )

    @parameterized(
            [
                {
                    "title":                "hello",
                    "index":                "",
                    "last_modified":        0,
                    "expect_index":         "",
                    "expect_last_modified": 0,
                },
                {
                    "title":                "hello",
                    "index":                "hello",
                    "last_modified":        0,
                    "expect_index":         "hello",
                    "expect_last_modified": 0,
                },
                {
                    "title":                "hello",
                    "index":                "",
                    "last_modified":        123,
                    "expect_index":         "",
                    "expect_last_modified": 123,
                },
                {
                    "title":                "hello",
                    "index":                "hello",
                    "last_modified":        123,
                    "expect_index":         "hello",
                    "expect_last_modified": 123,
                },
            ]
    )
    def test_init_succeed(
            self, title, index, last_modified, expect_index, expect_last_modified
    ):
        book = TradingBook(title=title, index=index, last_modified=last_modified, )

        self.assertEqual(book.title(), title)

        if expect_index == "":
            self.assertNotEqual(book.index(), "")
        else:
            self.assertEqual(book.index(), expect_index)

        if expect_last_modified == 0:
            self.assertNotEqual(book.last_modified(), 0)
        else:
            self.assertEqual(book.last_modified(), expect_last_modified)

    @parameterized([{"last_modified": 0}, {"last_modified": time.time()}])
    def test_update_last_modified_succeed(self, last_modified):
        book = TradingBook(title="hello", last_modified=last_modified)
        last_modified = book.last_modified()
        if last_modified == 0:
            self.assertNotEqual(book.last_modified(), 0)
        else:
            self.assertEqual(book.last_modified(), last_modified)

        book.update_last_modified()

        self.assertNotEqual(last_modified, book.last_modified())
        self.assertLess(last_modified, book.last_modified())

    @parameterized(
            [
                {"title": "hello", "index": "", "last_modified": 0},
                {"title": "hello", "index": "hello", "last_modified": 0},
                {"title": "hello", "index": "", "last_modified": 123},
                {"title": "hello", "index": "hello", "last_modified": 123},
            ]
    )
    def test_entity_succeed(self, title, index, last_modified):
        book = TradingBook(title=title, index=index, last_modified=last_modified, )

        self.assertEqual(book.to_entity().get("title", ""), title)

        if index == "":
            self.assertNotEqual(book.to_entity().get("index", ""), index)
        else:
            self.assertEqual(book.to_entity().get("index", ""), index)

        if last_modified == 0:
            self.assertNotEqual(
                    book.to_entity().get("last_modified", "0"), str(last_modified)
            )
        else:
            self.assertEqual(
                    book.to_entity().get("last_modified", "0"), str(last_modified)
            )

    @parameterized(
            [
                {"entity": {"title": "hello"}},
                {"entity": {"title": "hello", "index": "", "last_modified": "0"}},
                {"entity": {"title": "hello", "index": "abc", "last_modified": "0"}},
                {"entity": {"title": "hello", "index": "", "last_modified": "123"}},
                {"entity": {"title": "hello", "index": "abc", "last_modified": "123"}},
            ]
    )
    def test_entity_exchange_succeed(self, entity):
        book = TradingBook(
                title=entity.get("title", ""),
                index=entity.get("index", ""),
                last_modified=float(entity.get("last_modified", "0")),
        )

        new_book = TradingBook.from_entity(book.to_entity())

        self.assertEqual(book.title(), new_book.title())
        self.assertEqual(book.index(), new_book.index())
        self.assertEqual(book.last_modified(), new_book.last_modified())

    @parameterized(
            [
                {"entity": {"title": "hello"}},
                {"entity": {"title": "hello", "index": "", "last_modified": "0"}},
                {"entity": {"title": "hello", "index": "abc", "last_modified": "0"}},
                {"entity": {"title": "hello", "index": "", "last_modified": "123"}},
                {"entity": {"title": "hello", "index": "abc", "last_modified": "123"}},
            ]
    )
    def test_trading_book_from_entity_succeed(self, entity):
        book = TradingBook.from_entity(entity)

        self.assertEqual(book.title(), entity.get("title", ""))
        self.assertNotEqual(book.last_modified, 0)
        self.assertNotEqual(book.index, "")

    @parameterized(
            [
                {"entity": {}},
                {"entity": {"index": ""}},
                {"entity": {"last_modified": "0"}},
                {"entity": {"index": "", "last_modified": "0"}},
                {"entity": {"index": "hello", "last_modified": "123"}},
            ]
    )
    def test_trading_book_from_entity_missing_necessary_key(self, entity):
        with self.assertRaises(KeyError):
            TradingBook.from_entity(entity)


if __name__ == "__main__":
    unittest.main()
