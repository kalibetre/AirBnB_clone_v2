#!/usr/bin/python3
"""Module file_storage

This Module contains a definition for FileStorage Class
"""

import importlib
import json
import os
import re


class FileStorage:
    """FileStorage Class

    Attributes:
        __file_path (str): string - path to the JSON file
        __objects (dict): A dictionary of instantiated objects.

    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is None:
            return {k: v for k, v in self.__objects.items()}
        return {k: v for k, v in self.__objects.items() if type(v) == cls}

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        path = self.__file_path
        if (os.path.isfile(path) and os.path.getsize(path) > 0):
            with open(self.__file_path, 'r') as f:
                self.__objects = {
                    k: self.get_class(k.split(".")[0])(**v)
                    for k, v in json.load(f).items()
                }

    def delete(self, obj=None):
        """Deletes an object"""
        if obj is None:
            return None
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        return self.__objects.pop(key, None)

    def get_class(self, name):
        """ returns a class from models module using its name"""
        sub_module = re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()
        module = importlib.import_module(
            "models.{sub_module}".format(sub_module))
        return getattr(module, name)

    def close(self):
        """ calls the reload method """
        self.reload()
