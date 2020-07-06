#!/usr/bin/python3
"""
class city
"""


from models.base_model import BaseModel, time_conversor
from datetime import datetime


class City(BaseModel):
    """ Class city
    """
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """ Initialize method init
        """
        BaseModel.__init__(self, *args, **kwargs)

    def __str__(self):
        """ Define method str
        """
        self.__dict__.update({
            "created_at": time_conversor(self.created_at),
            "updated_at": time_conversor(self.updated_at),
            "state_id": self.state_id,
            "name": self.name,
            "__class__": self.__class__.__name__
        })
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def to_dict(self):
        """ Update to dictionary
        """
        if type(self.created_at) in [str]:
            self.created_at = time_conversor(self.created_at)
        if type(self.updated_at) in [str]:
            self.updated_at = time_conversor(self.updated_at)
        self.__dict__.update({
            "state_id": self.state_id,
            "name": self.name,
            "created_at": self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "updated_at": self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "__class__": self.__class__.__name__
        })
        return self.__dict__
