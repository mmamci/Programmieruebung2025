import json
from PIL import Image
from datetime import datetime

class Person:
    def __init__(self, id: int, firstname: str, lastname: str, date_of_birth: int, picture_path: str, ekg_tests: list = None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.picture_path = picture_path
        self.ekg_tests =  ekg_tests

    def __str__(self):
        return self.get_full_name()
        
    def get_full_name(self):
        return f"{self.lastname}, {self.firstname}"
    
    def get_picture(self):
        return Image.open(self.picture_path)
    
    def calculate_age(self):
        return datetime.now().year - self.date_of_birth

    def calc_max_heartrate(self):
        return 220 - self.calculate_age()

    @staticmethod
    def load_by_id(id):
        with open("data/person_db.json", "r", encoding='utf-8') as file:
            person_data = json.load(file)

        for person in person_data:
            if int(person["id"]) == id:
                return Person(
                 person["id"], 
                 person["firstname"], 
                 person["lastname"], 
                 person["date_of_birth"], 
                 person["picture_path"], 
                 person["ekg_tests"]
                 )

    @staticmethod
    def get_all_persons():
        """
        Returns the person data loaded from the JSON file.
        """
        with open("data/person_db.json", "r", encoding='utf-8') as file:
            person_data = json.load(file)

        person_object_list = []
        for person in person_data:
            person_object_list.append(Person(
             person["id"],
             person["firstname"],
             person["lastname"],
             person["date_of_birth"],
             person["picture_path"],
             person["ekg_tests"]
            )
        )
        return person_object_list 
    
    @staticmethod
    def get_person_object_by_full_name(person_name):
        firstname = person_name.split(", ")[1]
        lastname = person_name.split(", ")[0]
        for person in Person.get_all_persons():
            if person.firstname == firstname and person.lastname == lastname:
                return person
    




# def get_person_object_by_full_name(person_name):

#     firstname = person_name.split(", ")[1]
#     lastname = person_name.split(", ")[0]

#     for person in get_person_data():
#         if person.firstname == firstname and person.lastname == lastname:
#             return person

