import os
import unittest

import main


class TestFileSync(unittest.TestCase):
    root: str = "/run/media/neko/IODATA/testing_fields/file_sync/TESTING"

    src: str = os.path.join(root, "src")
    dst: str = os.path.join(root, "dst")
    tar: str = os.path.join(dst, "src")

    shell: str = os.path.join(root, "shell")

    def setUp(self):
        main.SAFEGUARD = self.root

    def test_cp_empty(self):
        with self.assertRaises(AssertionError):
            main.cp("", self.shell)

        with self.assertRaises(AssertionError):
            main.cp(self.shell, "")

    def test_rm_empty(self):
        with self.assertRaises(AssertionError):
            main.rm("")

    def test_cp_safeguard(self):
        with self.assertRaises(AssertionError):
            main.cp(self.shell, "/home/neko/programming_tools/python_ml")

    def test_rm_safeguard(self):
        with self.assertRaises(AssertionError):
            main.rm("/home/neko/programming_tools/python_ml")

    def test_cp_rm(self):
        src = os.path.join(self.shell, "src")
        dst = os.path.join(self.shell, "dst")

        src_file = os.path.join(self.shell, "src.txt")
        dst_file = os.path.join(self.shell, "dst.txt")

        self.assertTrue(os.path.exists(src))
        self.assertTrue(os.path.exists(src_file))

        self.assertFalse(os.path.exists(dst))
        self.assertFalse(os.path.exists(dst_file))

        print("")

        main.cp(src, dst)
        main.cp(src_file, dst_file)

        self.assertTrue(os.path.exists(dst))
        self.assertTrue(os.path.exists(dst_file))

        self.assertEqual(main.diff(src, dst), "")
        self.assertEqual(main.diff(src_file, dst_file), "")

        main.rm(dst)
        main.rm(dst_file)

        self.assertFalse(os.path.exists(dst))
        self.assertFalse(os.path.exists(dst_file))

        print("")

    def test_differ_empty(self):
        with self.assertRaises(AssertionError):
            main.diff(self.src, "")

        with self.assertRaises(AssertionError):
            main.diff("", self.tar)

    def differ_folder_helper(self, outb: str) -> None:
        for f1, f2 in main.files_differ(outb):
            self.assertTrue("differ" in f1)
            self.assertTrue("differ" in f2)
            self.assertTrue(self.src in f1 or self.dst in f1)
            self.assertTrue(self.src in f2 or self.dst in f2)

    def test_files_differ_folder(self):
        outb = main.diff(self.src, self.tar)
        self.differ_folder_helper(outb)

        outb = main.diff(self.tar, self.src)
        self.differ_folder_helper(outb)

    def differ_files_helper(self, outb: str) -> None:
        for f1, f2 in main.files_differ(outb):
            if "src" in f1:
                self.assertTrue("differ" in f2)
            elif "src" in f2:
                self.assertTrue("differ" in f1)
            else:
                raise Exception(f"unknown file\n{f1}, {f2}")

    def test_files_differ_files(self):
        outb = main.diff(
                os.path.join(self.root, "src.txt"), os.path.join(self.root, "dst.txt")
        )

        self.assertEqual(outb, "")

        outb = main.diff(
                os.path.join(self.root, "src.txt"), os.path.join(self.root, "differ.txt")
        )

        self.differ_files_helper(outb)

        outb = main.diff(
                os.path.join(self.root, "differ.txt"), os.path.join(self.root, "src.txt")
        )

        self.differ_files_helper(outb)

    def only_in_helper(self, outb: str) -> None:
        for fd, fs in main.only_in(outb):
            if "only_src" in fs:
                self.assertTrue(self.src in fd)
            elif "only_dst" in fs:
                self.assertTrue(self.dst in fd)
            else:
                raise Exception(f"only_in contain unknown files\n{fd}, {fs}")

    def test_only_in(self):
        outb = main.diff(self.src, self.tar)
        self.only_in_helper(outb)

        outb = main.diff(self.tar, self.src)
        self.only_in_helper(outb)
