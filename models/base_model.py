#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    def __init__(self, *args, **kwargs):
        if kwargs:
            self.created_at = datetime.fromisoformat(kwargs["created_at"])
            self.updated_at = datetime.fromisoformat(kwargs["updated_at"])
            for k, v in kwargs.items():
                if k == '__class__':
                    continue
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            models.storage.new(self)

    def __str__(self):
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def __repr__(self):
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        if type(self.created_at) in [str]:
            self.created_at = datetime.fromisoformat(self.created_at)
        if type(self.updated_at) in [str]:
            self.updated_at = datetime.fromisoformat(self.updated_at)
        self.created_at = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.updated_at = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        aux_val = (self.__dict__).copy()
        aux_val['__class__'] = self.__class__.__name__
        return aux_val
