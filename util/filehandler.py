import os
import json
from threading import Lock


class FileHandler(object):

    # staticpath reference
    base_path = os.path.abspath(os.path.dirname(__file__))

    @staticmethod
    def load_json(path):
        """Loads a json file and returns the content as a dictionary"""
        filepath = os.path.join(FileHandler.base_path, '..', path)

        lock = Lock()
        lock.acquire()
        try:
            with open(filepath) as jsonfile:
                data = json.load(jsonfile)
            return data
        finally:
            lock.release()

    @staticmethod
    def save_json(data, path):
        """Stores string json data to a json file at given path"""
        filepath = os.path.join(FileHandler.base_path, '..', path)

        lock = Lock()
        lock.acquire()
        try:
            with open(filepath, 'w+') as outfile:
                json.dump(data, outfile)
        finally:
            lock.release()

    @staticmethod
    def load_file(path):
        """Loads a json file and returns the content as a dictionary"""
        filepath = os.path.join(FileHandler.base_path, '..', path)

        with open(filepath, "r") as file:
            data = file.read()
        return data

    @staticmethod
    def object2json(object, path):
        """Stores object values to a json file at given path"""
        filepath = os.path.join(FileHandler.base_path, '..', path)

        lock = Lock()
        lock.acquire()
        try:
            with open(filepath, 'w+') as outfile:
                json.dump(object.__dict__, outfile)
        finally:
            lock.release()

    @staticmethod
    def file_exists(path):
        """Checks wether the given file exists or not"""
        filepath = os.path.join(FileHandler.base_path, '..', path)
        return os.path.exists(filepath)

    @staticmethod
    def get_files_in_dir(path):
        """Returns a list containing all filenames in a given directory"""
        filepath = os.path.join(FileHandler.base_path, '..', path)
        return os.listdir(filepath)
