#!/usr/bin/python3
"""
class place
"""


from models.base_model import BaseModel, time_conversor
from datetime import datetime


class Place(BaseModel):
    """
    class place
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    def __init__(self, *args, **kwargs):
        """
        method init
        """
        BaseModel.__init__(self, *args, **kwargs)

    def __str__(self):
        """
        method str
        """
        self.__dict__.update({
            "created_at": time_conversor(self.created_at),
            "updated_at": time_conversor(self.updated_at),
            "city_id": self.city_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "number_rooms": self.number_rooms,
            "number_bathrooms": self.number_bathrooms,
            "max_guest": self.max_guest,
            "price_by_night": self.price_by_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "amenity_ids": self.amenity_ids,
            "__class__": self.__class__.__name__
        })
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def to_dict(self):
        """
        method to_dict
        """
        if type(self.created_at) in [str]:
            self.created_at = time_conversor(self.created_at)
        if type(self.updated_at) in [str]:
            self.updated_at = time_conversor(self.updated_at)
        self.__dict__.update({
            "city_id": self.city_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "number_rooms": self.number_rooms,
            "number_bathrooms": self.number_bathrooms,
            "max_guest": self.max_guest,
            "price_by_night": self.price_by_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "amenity_ids": self.amenity_ids,
            "created_at": self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "updated_at": self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "__class__": self.__class__.__name__
        })
        return self.__dict__
