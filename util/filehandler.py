import os
import json


class FileHandler(object):

    def __init__(self, relative_root_path=None):

        if relative_root_path is not None:
            self.base_path = os.path.abspath(
                os.path.dirname(__file__)) + "/" + relative_root_path + "/"
        else:
            self.base_path = os.path.abspath(
                os.path.dirname(__file__))

    def load_json(self, path):
        """Loads a json file and returns the content as a dictionary"""
        filepath = os.path.join(self.base_path, path)

        with open(filepath) as jsonfile:
            data = json.load(jsonfile)
        return data

    def save_json(self, data, path):
        """Stores string json data to a json file at given path"""
        filepath = os.path.join(self.base_path, path)

        with open(filepath, 'w+') as outfile:
            json.dump(data, outfile)

    def load_file(self, path):
        """Loads a file and returns the content as string"""
        filepath = os.path.join(self.base_path, path)

        with open(filepath, "r") as file:
            data = file.read()
        return data

    def save_file(self, data, path):
        """Stores string data to a file at given path"""
        filepath = os.path.join(self.base_path, path)

        with open(filepath, "w+") as file:
            data = file.write(str(data))
        return data

    def object2json(self, object, path):
        """Stores object values to a json file at given path"""
        filepath = os.path.join(self.base_path, path)

        with open(filepath, 'w+') as outfile:
            json.dump(object.__dict__, outfile)

    def file_exists(self, path):
        """Checks wether the given file exists or not"""
        filepath = os.path.join(self.base_path, path)
        return os.path.exists(filepath)

    def get_files_in_dir(self, path):
        """Returns a list containing all filenames in a given directory"""
        filepath = os.path.join(self.base_path, path)
        return os.listdir(filepath)
