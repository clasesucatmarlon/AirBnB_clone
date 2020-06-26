from os import getcwd
from json import dumps, loads
from models.base_model import BaseModel
import json

class FileStorage:
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        return self.__objects
    
    def new(self, obj):
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        json_object = {}
        for key in self.__objects:
            json_object[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            f.write(dumps(json_object))

    def reload(self):
        try:
            with open(self.__file_path, 'r') as f:
                for key, value in loads(f.read()).items():
                    ins = eval(value["__class__"])(**value)
                    self.__objects[key] = ins
        except FileNotFoundError:
            pass




