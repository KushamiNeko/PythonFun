import functools
from typing import Any, Dict, List

from Fun.utils import colors, pretty


def parameterized(sets: List[Dict[str, Any]]):
    def testing(func):
        @functools.wraps(func)
        def wrapper_testing(*args, **kargs):
            count = 0
            print()
            for book in sets:
                pretty.color_print(
                    colors.PAPER_LIGHT_GREEN_300,
                    f"running parameterized test of index {count}",
                )

                func(*args, **book)
                count += 1

            pretty.color_print(
                colors.PAPER_LIGHT_BLUE_300,
                f"\nfinished running {count} parameterized tests",
            )

        return wrapper_testing

    return testing
