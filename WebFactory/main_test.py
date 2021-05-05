import os
import subprocess
import unittest

from fun.utils import colors, pretty
from happy.web_factory.main import processorFactory


class TestMain(unittest.TestCase):
    times = 3

    @classmethod
    def setUpClass(cls):
        commands = [
            ["rm testing/**/*.css"],
            ["rm testing/**/**/*.css"],
            ["rm testing/**/*.js"],
            ["rm testing/**/**/*.js"],
            ["rm testing/**/*.js.*"],
            ["rm testing/**/**/*.js.*"],
        ]

        for command in commands:
            cmd = subprocess.run(
                    command, capture_output=True, encoding="utf-8", shell=True
            )
            if cmd.returncode != 0:
                print(cmd.stderr)

    def _testing(self, src_exts, tar_ext, root):
        for f in os.listdir(root):

            path = os.path.join(root, f)
            if os.path.isdir(path):

                if os.path.basename(path).startswith(".") or os.path.basename(
                        path
                ).startswith("_"):
                    for fs in os.listdir(path):
                        pretty.color_print(
                                colors.PAPER_AMBER_300, f"testing: {os.path.join(path, fs)}"
                        )
                        self.assertTrue(tar_ext not in fs)

                else:
                    self._testing(src_exts, tar_ext, path)

            else:
                ext = os.path.splitext(f)[1]
                if ext in src_exts:
                    path = os.path.join(root, f.replace(ext, tar_ext))
                    pretty.color_print(colors.PAPER_AMBER_300, f"testing: {path}")

                    if os.path.basename(path).startswith(".") or os.path.basename(
                            path
                    ).startswith("_"):

                        self.assertFalse(os.path.exists(path))
                    else:

                        self.assertTrue(os.path.exists(path))

    def setUp(self):
        print()

    def test_css(self):
        tbs = [{"src": "testing/testing_css"}]

        for _ in range(self.times):
            for tb in tbs:
                p = processorFactory("scss", tb["src"])
                p.process()

                self._testing((".sass", ".scss"), ".css", tb["src"])

    def test_dart(self):
        tbs = [{"src": "testing/testing_dart"}]

        for _ in range(self.times):
            for tb in tbs:
                p = processorFactory("dart", tb["src"])
                p.process()

                self._testing((".dart",), ".js", tb["src"])

    def test_ts(self):
        tbs = [{"src": "testing/testing_ts"}]

        for _ in range(self.times):
            for tb in tbs:
                p = processorFactory("ts", tb["src"])
                p.process()

                self._testing((".ts",), ".js", tb["src"])
