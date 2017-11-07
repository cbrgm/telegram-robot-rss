import unittest
import os
from util.filehandler import FileHandler


class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.fh = FileHandler("..")

    def test_save_and_load_json(self):
        sample_json = {}
        sample_json["testbool"] = True
        sample_json["teststring"] = "hello world"

        self.fh.save_json(sample_json, "resources/sample.json")
        data = self.fh.load_json("resources/sample.json")
        self.assertEqual(data["testbool"], True)
        self.assertEqual(data["teststring"], "hello world")

    def test_save_and_load_file(self):
        data = "text message"
        self.fh.save_file(data=data, path="resources/sample.txt")
        result = self.fh.load_file("resources/sample.txt")
        self.assertEqual(result, "text message")

    def test_file_exists(self):
        data = "text message"
        self.fh.save_file(data=data, path="resources/sample.txt")
        self.assertTrue(self.fh.file_exists("resources/sample.txt"))

    def tearDown(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        filepath_json = os.path.join(base_path, '..', "resources/sample.json")
        filepath_text = os.path.join(base_path, '..', "resources/sample.txt")
        if os.path.exists(filepath_json):
            os.remove(filepath_json)
        if os.path.exists(filepath_text):
            os.remove(filepath_text)
