from models.base_model import BaseModel
from datetime import datetime


class User(BaseModel):
    email = ""
    password = ""
    first_name = ""
    last_name = ""
    def __init__(self, *args, **kwargs):
        BaseModel.__init__(self, *args, **kwargs)


    def __str__(self):
        self.__dict__.update({
            "email" : self.email,
            "password" : self.password,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "__class__" : self.__class__.__name__
        })
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def to_dict(self):
        if type(self.created_at) in [str]:
            self.created_at = datetime.fromisoformat(self.created_at)
        if type(self.updated_at) in [str]:
            self.updated_at = datetime.fromisoformat(self.updated_at)
        self.created_at = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.updated_at = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.__dict__.update({
            "email" : self.email,
            "password" : self.password,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "__class__" : self.__class__.__name__
        })
        return self.__dict__
