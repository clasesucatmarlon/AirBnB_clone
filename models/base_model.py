import uuid
import datetime
import json
import models

def getdate():
  return datetime.datetime.today()

class BaseModel:

  def __init__(self, *args, **kwargs):
    if len(kwargs.keys()) > 0:
      self.id = kwargs["id"]
      self.created_at = datetime.datetime.fromisoformat(kwargs["created_at"])
      self.update_at = datetime.datetime.fromisoformat(kwargs["update_at"])
      self.name = kwargs["name"]
      self.my_number = kwargs["my_number"]
    else:
      self.id = str(uuid.uuid4())
      self.created_at = getdate()
      self.update_at = getdate()
      self.name = ""
      self.my_number = 0
    models.storage.new(self)

  def save(self):
    self.update_at = getdate()
    models.storage.save()

  def __str__(self):
    name = self.__class__.__name__
    id = self.id
    dicti = self.__dict__.copy()
    return "[{}] ({}) {}".format(name, id, dicti)
  
  def to_dict(self):
    # Arreglar error en el tiempo de update, debe ser igual created
    dictionary = {
      "name" : self.name,
      "id" : self.id,
      "created_at" : str(self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')),
      "update_at" : str(self.update_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')),
      "my_number" : self.my_number,
      "__class__" : self.__class__.__name__
    }
    return dictionary

  #def to_json(self):
    #self.__dict__.update({"__class__" : self.__class__.__name__})
    #return self.__dict__