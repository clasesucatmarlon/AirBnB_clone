#!/usr/bin/python3
"""
class user
"""
from models.base_model import BaseModel, time_conversor
from datetime import datetime


class User(BaseModel):
    """ Class user
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """ method init
        """
        BaseModel.__init__(self, *args, **kwargs)

    def __str__(self):
        """ method init
        """
        self.__dict__.update({
            "created_at": time_conversor(self.created_at),
            "updated_at": time_conversor(self.updated_at),
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "__class__": self.__class__.__name__
        })
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def to_dict(self):
        """ method to dict
        """
        if type(self.created_at) in [str]:
            self.created_at = time_conversor(self.created_at)
        if type(self.updated_at) in [str]:
            self.updated_at = time_conversor(self.updated_at)
        self.__dict__.update({
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "updated_at": self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "__class__": self.__class__.__name__
        })
        return self.__dict__
