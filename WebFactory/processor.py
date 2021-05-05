import hashlib
import os
import subprocess
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional

from fun.utils import colors, pretty


class Processor(metaclass=ABCMeta):
    _store: Dict[str, bytes] = {}
    _init: bool = True

    @classmethod
    def _cache_store(cls) -> Dict[str, bytes]:
        return cls._store

    @classmethod
    def _is_fresh(cls) -> bool:
        return cls._init

    @classmethod
    def _not_fresh(cls) -> None:
        cls._init = False

    def __init__(self, root: str, optimized: bool = False):
        assert os.path.exists(root)

        self._root = root
        self._optimized = optimized

    @abstractmethod
    def _src_exts(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def _dst_ext(self) -> str:
        raise NotImplementedError

    def _excluded_path(self) -> List[str]:
        return ["node_modules"]

    @abstractmethod
    def _optimized_command(self, src: str, dst: str) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def _command(self, src: str, dst: str) -> List[str]:
        raise NotImplementedError

    def process(self) -> None:
        self._prepare(self._root)
        self._watch()
        self._synchronize()

        self._not_fresh()

    def _prepare(self, src: str) -> None:
        assert os.path.exists(src)
        assert os.path.isdir(src)

        for f in os.listdir(src):
            if f in self._excluded_path():
                continue

            srcr = os.path.join(src, f)

            if os.path.isdir(srcr):
                self._prepare(srcr)

            elif os.path.isfile(srcr):
                if os.path.splitext(srcr)[1] not in self._src_exts():
                    continue

                self._cache_init(srcr)
            else:
                raise ValueError(f"unknown file type: {srcr}")

    def _watch(self) -> None:
        fs = self._cache_changed()
        shadow_changed = False
        if fs is not None:
            for f in fs:
                if os.path.splitext(f)[1] not in self._src_exts():
                    continue

                if self._is_shadow_file(f):
                    shadow_changed = True
                    break

        for src in self._cache_store().keys():
            assert os.path.exists(src)

            ext = os.path.splitext(src)[1]
            if ext not in self._src_exts():
                continue

            if self._is_shadow_file(src):
                continue

            dst = src.replace(ext, self._dst_ext())

            if not os.path.exists(dst):
                if self._is_fresh():
                    self._compile(src, dst)
            else:
                if fs is not None:
                    if src in fs:
                        self._compile(src, dst)
                    elif shadow_changed:
                        self._compile(src, dst)

    def _synchronize(self) -> None:
        for k in self._cache_store().keys():
            if self._is_shadow_file(k):

                if os.path.splitext(k)[1] not in self._src_exts():
                    continue

                self._cache_refresh(k)

    def _compile(self, src: str, dst: str) -> None:
        pretty.color_print(colors.PAPER_LIGHT_BLUE_300, f"process: {src} -> {dst}")

        cmd: subprocess.CompletedProcess
        if self._optimized:
            cmd = subprocess.run(
                    self._optimized_command(src, dst), capture_output=True, encoding="utf-8"
            )
        else:
            cmd = subprocess.run(
                    self._command(src, dst), capture_output=True, encoding="utf-8"
            )

        self._cache_refresh(src)

        if cmd.returncode != 0:
            pretty.color_print(
                    colors.PAPER_RED_400, f"\nmessage: {cmd.stdout}\nerror: {cmd.stderr}"
            )

    def _is_shadow_file(self, src: str) -> bool:
        assert os.path.isfile(src)

        path = src
        while True:
            base = os.path.basename(path)
            if base.startswith(".") or base.startswith("_"):
                return True
            parent = os.path.dirname(path)
            if parent == self._root or parent == "":
                break
            path = parent

        return False

    def _cache_init(self, src: str) -> None:
        assert os.path.exists(src)

        if src not in self._cache_store():
            pretty.color_print(colors.PAPER_TEAL_300, f"cache: {src}")
            self._cache_store()[src] = self._cache_hash(src)

    def _cache_refresh(self, src: str) -> None:
        assert os.path.exists(src)
        assert src in self._cache_store()

        h = self._cache_hash(src)
        if self._cache_store()[src] != h:
            pretty.color_print(colors.PAPER_TEAL_300, f"cache: {src}")
            self._cache_store()[src] = h

    def _cache_changed(self) -> Optional[List[str]]:
        d = []
        for k, v in self._cache_store().items():
            if self._cache_hash(k) != v:
                d.append(k)

        return d if d else None

    def _cache_hash(self, src: str) -> bytes:
        assert os.path.exists(src)

        m = hashlib.sha256()
        with open(src, "rb") as f:
            m.update(f.read())

        return m.digest()


class ProcessorCSS(Processor):
    def _src_exts(self) -> List[str]:
        return [".sass", ".scss"]

    def _dst_ext(self) -> str:
        return ".css"

    def _optimized_command(self, src: str, dst: str) -> List[str]:
        return self._command(src, dst)

    def _command(self, src: str, dst: str) -> List[str]:
        return ["sass", "--no-source-map", src, dst]


class ProcessorDart(Processor):
    def _src_exts(self) -> List[str]:
        return [".dart"]

    def _dst_ext(self) -> str:
        return ".js"

    def _optimized_command(self, src: str, dst: str) -> List[str]:
        return ["dart2js", "-O2", src, "-o", dst]

    def _command(self, src: str, dst: str) -> List[str]:
        return ["dart2js", src, "-o", dst, "--enable-asserts"]


class ProcessorTS(Processor):
    def _src_exts(self) -> List[str]:
        return [".ts"]

    def _dst_ext(self) -> str:
        return ".js"

    def _optimized_command(self, src: str, dst: str) -> List[str]:
        return self._command(src, dst)

    def _command(self, src: str, dst: str) -> List[str]:
        return [
            "tsc",
            "--outFIle",
            dst,
            "--module",
            "amd",
            "--moduleResolution",
            "node",
            "--target",
            "es3",
            "--lib",
            "dom,es2015",
            "--noImplicitAny",
            "--removeComments",
            src,
        ]
