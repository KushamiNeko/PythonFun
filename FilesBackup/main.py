from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
import traceback
from typing import Any, Dict, Iterator, Tuple, cast

from fun.utils import colors, pretty

SAFEGUARD = "/run/media/neko/IODATA/backups"


def args_parse() -> Dict[str, Any]:
    global SAFEGUARD

    parser = argparse.ArgumentParser()

    parser.add_argument("--from", metavar="", type=str, help="source directory")

    parser.add_argument("--to", metavar="", type=str, help="destination directory")

    parser.add_argument("--syncfile", metavar="", type=str, help="configuration file")

    parser.add_argument(
            "--refresh",
            metavar="",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="full refresh copy",
    )

    parser.add_argument(
            "--ensure",
            metavar="",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="ensure the backup files",
    )

    parser.add_argument(
            "--safeguard",
            metavar="",
            type=str,
            default=SAFEGUARD,
            help="the destination path must under safeguard path",
    )

    args = vars(parser.parse_args())

    if args.get("safeguard"):
        SAFEGUARD = cast(str, args.get("safeguard")).strip()

    if not args.get("syncfile"):
        if args.get("from") and args.get("to"):

            pretty.color_print(colors.PAPER_INDIGO_300, f"from: {args.get('from')}")

            pretty.color_print(colors.PAPER_INDIGO_300, f"to: {args.get('to')}")
        else:
            pretty.color_print(
                    colors.PAPER_RED_500,
                    "please specify flags of either SYNCFILE, or FROM and TO",
            )

            exit(1)

    else:
        pretty.color_print(colors.PAPER_INDIGO_300, f"syncfile: {args.get('syncfile')}")

    pretty.color_print(colors.PAPER_INDIGO_300, f"refresh: {args.get('refresh')}")
    pretty.color_print(colors.PAPER_INDIGO_300, f"ensure: {args.get('ensure')}")

    pretty.color_print(colors.PAPER_INDIGO_300, f"safeguard: {args.get('safeguard')}")

    return args


def main() -> None:
    global SAFEGUARD

    args = args_parse()

    assert SAFEGUARD != ""
    assert os.path.exists(SAFEGUARD)

    pretty.color_print(colors.PAPER_AMBER_300, "start files backup")
    start = time.time()

    if not args.get("syncfile"):
        operation(
                cast(str, args.get("from")).strip(),
                cast(str, args.get("to")).strip(),
                refresh_all=args.get("refresh", False),
                ensure=args.get("ensure", False),
        )

    else:

        with open(args.get("syncfile", "nonexist-file.txt"), "r") as f:
            content = f.read()
            regex = re.compile("(.+) -> (.+)", re.MULTILINE)

            for match in regex.finditer(content):
                src = match.group(1).strip()
                dst = match.group(2).strip()

                operation(
                        src,
                        dst,
                        refresh_all=args.get("refresh", False),
                        ensure=args.get("ensure", False),
                )

    end = time.time()
    length = end - start

    pretty.color_print(colors.PAPER_AMBER_300, "files backup completed!!!")
    pretty.color_print(colors.PAPER_AMBER_300, f"processing time: {length} seconds")


def operation(
        src: str, dst: str, refresh_all: bool = False, ensure: bool = False
) -> None:
    if src == "" or dst == "":
        pretty.color_print(colors.PAPER_RED_500, "empty src or dst")
        exit(1)

    if src == dst:
        pretty.color_print(colors.PAPER_RED_500, "src and dst are the same")
        exit(1)

    if not os.path.exists(src):
        pretty.color_print(colors.PAPER_RED_500, f"src does not exist: {src}")
        exit(1)

    if not os.path.exists(dst):
        pretty.color_print(colors.PAPER_RED_500, f"dst does not exist: {dst}")
        exit(1)

    tar = ""

    if os.path.isfile(src):
        tar = dst
    elif os.path.isdir(src):
        if os.path.basename(src) == os.path.basename(dst):
            tar = dst
        else:
            tar = os.path.join(dst, os.path.basename(src))
    else:
        raise ValueError("unknown file type")

    if not os.path.exists(tar):
        cp(src, tar)
        return

    try:
        if refresh_all:
            refresh(src, tar)
        else:
            sync(src, tar)

        if ensure:
            results = diff(src, tar)
            if results == "":
                pretty.color_print(colors.PAPER_PURPLE_300, f"ensure: {src} -> {tar}")
            else:
                raise Exception(f"program failed to sync {src} and {tar}")

    except Exception:
        info = sys.exc_info()
        traceback.print_tb(info[2])
        pretty.color_print(
                colors.PAPER_RED_500, f"{type(info[1]).__name__}: {str(info[1])}"
        )
        exit(1)


def files_differ(outb: str) -> Iterator[Tuple[str, str]]:
    matches = re.finditer(r"Files (.+) and (.+) differ", outb, re.MULTILINE)
    for match in matches:
        yield (match.group(1).strip(), match.group(2).strip())


def only_in(outb: str) -> Iterator[Tuple[str, str]]:
    matches = re.finditer(r"Only in (.+): (.+)", outb, re.MULTILINE)

    for match in matches:
        yield (match.group(1).strip(), match.group(2).strip())


def sync(src: str, tar: str) -> None:
    assert src != "" and tar != ""

    outb = diff(src, tar)
    for f1, f2 in files_differ(outb):

        s = ""
        d = ""

        if f1.startswith(src) and f2.startswith(tar):
            s = f1
            d = f2
        elif f1.startswith(tar) and f2.startswith(src):
            s = f2
            d = f1
        else:
            raise subprocess.SubprocessError(f"unknown path: {f1}, {f2}")

        rm(d)
        cp(s, d)

    for fd, fs in only_in(outb):

        path = os.path.join(fd, fs)

        if path.startswith(src):
            s = path
            d = path.replace(src, tar)
            cp(s, d)
        elif path.startswith(tar):
            rm(path)
        else:
            raise subprocess.SubprocessError(f"unknown path: {path}")


def refresh(src: str, tar: str) -> None:
    assert src != "" and tar != ""

    if os.path.exists(tar):
        rm(tar)
    cp(src, tar)


def diff(src: str, tar: str) -> str:
    assert src != "" and tar != ""

    cmd = subprocess.run(
            ["diff", "-rq", src, tar], capture_output=True, encoding="utf-8"
    )

    if cmd.returncode == 0:
        return ""
    elif cmd.returncode == 1:
        return cmd.stdout.strip()
    else:
        raise subprocess.SubprocessError(cmd.stderr)


def cp(src: str, tar: str) -> None:
    global SAFEGUARD

    assert src != "" and tar != ""
    assert SAFEGUARD in tar

    pretty.color_print(colors.PAPER_LIGHT_BLUE_300, f"cp: {src} -> {tar}")

    cmd = subprocess.run(["cp", "-rp", src, tar], capture_output=True, encoding="utf-8")

    if cmd.returncode != 0:
        raise subprocess.SubprocessError(cmd.stderr)


def rm(tar: str) -> None:
    global SAFEGUARD

    assert tar != ""
    assert SAFEGUARD in tar

    pretty.color_print(colors.PAPER_RED_500, f"rm: {tar}")

    cmd = subprocess.run(["rm", "-rf", tar], capture_output=True, encoding="utf-8")

    if cmd.returncode != 0:
        raise subprocess.SubprocessError(cmd.stderr)


if __name__ == "__main__":
    main()
