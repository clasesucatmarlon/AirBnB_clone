from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import json


def task1():
    my_model = BaseModel()
    my_model.name = "Holberton"
    my_model.my_number = 89
    print(my_model)
    my_model.save()
    print(my_model)
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(
            key, type(my_model_json[key]), my_model_json[key]))


def task2():
    my_model = BaseModel()
    my_model.name = "Holberton"
    my_model.my_number = 89
    print(my_model.id)
    print(my_model)
    print(type(my_model.created_at))
    print("--")
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(
            key, type(my_model_json[key]), my_model_json[key]))
    print("--")
    my_new_model = BaseModel(**my_model_json)
    print(my_new_model.id)
    print(my_new_model)
    print(type(my_new_model.created_at))
    print("--")
    print(my_model is my_new_model)


def task3():
    all_objs = storage.all()
    print("-- Reloaded objects --")
    for obj_id in all_objs.keys():
        obj = all_objs[obj_id]
        print(obj)

    print("-- Create a new object --")
    my_model = BaseModel()
    my_model.name = "Holberton"
    my_model.my_number = 89
    my_model.save()
    print(my_model)


d = {}
with open('file.json', 'r') as f:
    d = json.loads(f.read())

keys = list(d.keys())
value = d.values()

for i in range(len(keys)):
    print(f'Model: {keys[i]}')
    print(f'Created at -> {d[keys[i]]["created_at"]}')
    print(f'Updated at -> {d[keys[i]]["update_at"]}')
    print('------------')
