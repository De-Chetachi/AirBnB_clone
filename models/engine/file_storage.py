#!/usr/bin/python3
'''contains a file storage class'''


from json import dump
from json import load
from os.path import isfile
from json.decoder import JSONDecodeError
from models.base_model import BaseModel
from models.user import User

class FileStorage:
    '''file storage class'''
    __file_path = "storage.json"
    __objects = {}  # will store all objects by classname.id

    def __init__(self):
        '''instance constructor'''

    def all(self):
        '''returns the dictionary __objects'''
        return self.__objects
    
    def new(self, obj):
        '''sets in __objects the obj with key <obj classname.id'''
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        '''serializes __objects to the JSON file'''
        with open(self.__file_path, 'w', encoding="utf-8") as file_:
            # Convert objects to dictionaries before serializing
            json_str = {key: obj.to_dict() for key, obj in self.__objects.items()}
            dump(json_str, file_)

    def reload(self):
        '''deserializes the JSON file to __objects
        if the file does not exist, do nothing'''

        try:
            with open(self.__file_path, "r", encoding="utf-8") as file_:
                deserialize = load(file_)
                for key, value in deserialize.items():
                    class_name = value["__class__"]
                    del value["__class__"]
                    obj_id = key.split('.')[1]
                    # Create an instance of the class and store it
                    self.new(eval(class_name)(**value))

        except (FileNotFoundError, JSONDecodeError):
            return