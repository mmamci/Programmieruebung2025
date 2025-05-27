import json
from PIL import Image

def get_person_data():
    """
    Returns the person data loaded from the JSON file.
    """

    with open("data/person_db.json", "r", encoding='utf-8') as file:
        person_data = json.load(file)

    return person_data

def get_person_names():
    """
    Returns a list of person names from the loaded person data.
    """

    names = []
    person_data = get_person_data()

    for person in person_data:
        names.append(person["lastname"] + ", " + person["firstname"])
    
    return names

def get_person_data_by_name(personname):
    all_persons = get_person_data()

    name = personname.split(", ")

    for person_dict in all_persons:
        if person_dict["firstname"]==name[1] and person_dict["lastname"] == name[0]:
            return person_dict
    
    return "Person not found"


def get_person_image_by_name(personname):
    person_dict = get_person_data_by_name(personname)
    
    return Image.open(person_dict["picture_path"])

if __name__ == "__main__":
    person_data = get_person_data()

    person_names = get_person_names()

    person_name = "Huber, Julian"

    person_dict = get_person_data_by_name(person_name)

    print(person_dict)


    