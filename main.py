import streamlit as st
from PIL import Image

from src.read_data import get_person_name

if "selected_person" not in st.session_state:
    st.session_state.selected_person = "NONE"

print(st.session_state.selected_person)

st.write(" # Hello, Streamlit!")

st.write("## Zweite Überschrift")

st.write("This is a simple Streamlit app to demonstrate the setup.")

st.session_state.selected_person = st.selectbox("Wähle eine Versuchsperson", options = get_person_name())

# Laden eines Bildes
image = Image.open("data/pictures/js.jpg")
# Anzeigen eines Bildes mit Caption
st.image(image, caption = st.session_state.selected_person)

st.write(st.session_state.selected_person)
print(st.session_state.selected_person)



