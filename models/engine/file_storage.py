#!/usr/bin/python3


"""
class filestorage
"""


from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

import json
import os


class FileStorage:
    """ Class file storage
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ all objects
        """
        return self.__objects

    def new(self, obj):
        """ method new object given
        """
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """ Method save
        """
        with open(self.__file_path, "w", encoding="UTF-8") as f:
            obj_dict = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(obj_dict, f, indent=4, sort_keys=True, default=str)

    def reload(self):
        """ Method reload that add in self.objects the dict of the file
        """
        all_class = {
            "BaseModel": BaseModel,
            "User": User,
            "Amenity": Amenity,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State
        }
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, "r", encoding="UTF-8") as f:
                obj_dict = json.load(f)
                for k, v in obj_dict.items():
                    name = k.split('.')[0]
                    if name in all_class:
                        obj = all_class[name](**v)
                        self.__class__.__objects[k] = obj
