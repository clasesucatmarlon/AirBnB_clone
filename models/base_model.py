#!/usr/bin/python3
"""
class Base model
"""


from uuid import uuid4
from datetime import datetime
import models


def time_conversor(obj):
    """ Define time conversor
        that return new time object
    """
    if type(obj) in [datetime]:
        obj = obj.strftime('%Y-%m-%dT%H:%M:%S.%f')
    return datetime.strptime(obj, "%Y-%m-%dT%H:%M:%S.%f")


class BaseModel:
    """ Class Base Model
    """
    def __init__(self, *args, **kwargs):
        """ Initialize method init
            Base instance
        """
        if kwargs:
            self.created_at = time_conversor(kwargs["created_at"])
            self.updated_at = time_conversor(kwargs["updated_at"])
            for k, v in kwargs.items():
                if k == '__class__':
                    continue
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.today().isoformat()
            self.updated_at = datetime.today().isoformat()
            models.storage.new(self)

    def __str__(self):
        """ Define method str that return
            string representation
        """
        self.__dict__.update({
            "created_at": time_conversor(self.created_at),
            "updated_at": time_conversor(self.updated_at),
        })
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def __repr__(self):
        """ Define method repr that return
            string representation
        """
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """ method save that calls storage
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """ Method to dictionary
            that return dict representation
        """
        if type(self.created_at) in [str]:
            self.created_at = time_conversor(self.created_at)
        if type(self.updated_at) in [str]:
            self.updated_at = time_conversor(self.updated_at)
        self.created_at = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        self.updated_at = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        aux_val = (self.__dict__).copy()
        aux_val['__class__'] = self.__class__.__name__
        return aux_val
