import json
from PIL import Image

def get_person_data():
    """
    Returns the person data loaded from the json file.
    """
    # Opening JSON file
    file = open("data/person_db.json")
    with open("data/person_db.json", "r", encoding = "utf-8") as file:
        person_data = json.load(file)
    return person_data


def get_person_name():
    """
    Returns a list of person names from the loaded person data.
    """

    names_list = []
    # Gib mir die Liste mit allen Persons
    person_dict = get_person_data()
    # Gehe durch die Liste 
    for person_dict in person_dict:
        # Jeder Eintrag ist ein dict mit den Feldern (firstname und lastname)
        names_list.append(person_dict["firstname"] + "," + person_dict["lastname"])
        # Hänge das an die Namensliste an
    return names_list
    
def get_person_data_by_name(personname):

    all_persons = get_person_data()
    firstname = personname.split(",")[1]
    lastname = personname.split(",")[0]

    for person_dict in all_persons:
        if person_dict["firstname"] == firstname and person_dict["lastname"] == lastname:
            return person_dict
    

def get_person_image_by_name(personname):

    person_dict = get_person_data_by_name(person_name)
    print(person_dict["picture_path"])

    # Laden eines Bildes
    
    image = Image.open("data/pictures/js.jpg")
    return image

    # Anzeigen eines Bildes mit Caption
    st.image(image, caption = st.session_state.selected_person)
    


if __name__ == "__main__" :
    # Example
    person_data = get_person_data()


    person_names = get_person_name()

    person_name = "Huber, Julian"
    person_dict = get_person_data_by_name(person_name)
    print(person_dict["picture_path"])
