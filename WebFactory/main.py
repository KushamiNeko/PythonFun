import argparse
import os
from time import sleep
from typing import Any, Dict, List, cast

from fun.utils import colors, pretty
from happy.web_factory.processor import Processor, ProcessorCSS, ProcessorDart, ProcessorTS


def args_parse() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", metavar="", type=str, help="the input directory")

    parser.add_argument(
            "--operation",
            metavar="",
            nargs="*",
            default=["scss", "dart"],
            choices=["scss", "dart", "ts"],
            help="processor",
    )

    parser.add_argument(
            "--optimized",
            metavar="",
            nargs="?",
            const=True,
            default=False,
            type=bool,
            help="optimize the output file",
    )

    parser.add_argument(
            "--interval",
            metavar="",
            nargs="?",
            const=3,
            default=3,
            type=int,
            help="sleep interval (seconds)",
    )

    args = vars(parser.parse_args())

    assert args.get("input") is not None

    assert args.get("operation") is not None

    assert args.get("optimized") is not None
    assert args.get("interval") is not None

    pretty.color_print(colors.PAPER_INDIGO_300, f"input: {args.get('input')}")

    pretty.color_print(
            colors.PAPER_INDIGO_300,
            f"operation: {', '.join(cast(List[str], args.get('operation')))}",
    )
    pretty.color_print(colors.PAPER_INDIGO_300, f"optimized: {args.get('optimized')}")

    pretty.color_print(
            colors.PAPER_INDIGO_300, f"interval: {args.get('interval')} seconds"
    )

    return args


def main() -> None:
    args = args_parse()

    src = args.get("input")
    assert src is not None
    assert os.path.isdir(src)

    ops = args.get("operation")
    assert ops is not None
    assert len(ops) >= 1

    optimized = args.get("optimized", False)
    assert optimized is not None

    interval = args.get("interval", 3)
    assert interval is not None

    while True:
        for op in ops:
            p = processorFactory(op, src, optimized)
            p.process()

        sleep(interval)


def processorFactory(op: str, root: str, optimized: bool = False) -> Processor:
    assert op in ("scss", "dart", "ts")

    if op == "scss":
        return ProcessorCSS(root=root, optimized=optimized)
    elif op == "dart":
        return ProcessorDart(root=root, optimized=optimized)
    elif op == "ts":
        return ProcessorTS(root=root, optimized=optimized)
    else:
        raise ValueError(f"invalid op: {op}")


if __name__ == "__main__":
    main()
