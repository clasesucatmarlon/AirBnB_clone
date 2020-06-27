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
        keypass = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[keypass] = obj

    def save(self):
        new_json_object = {}
        for keypass in self.__objects:
            new_json_object[keypass] = self.__objects[keypass].to_dict()
        with open(self.__file_path, 'w') as f:
            f.write(dumps(new_json_object))

    def reload(self):
        try:
            with open(self.__file_path, 'r') as f:
                for keypass, dummy in loads(f.read()).items():
                    ins = eval(dummy["__class__"])(**dummy)
                    self.__objects[keypass] = ins
        except FileNotFoundError:
            pass
