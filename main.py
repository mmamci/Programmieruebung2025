import streamlit as st

from classes.person import Person
from src.analyze_activity_data import ActivityData, ActivityPlot

if "person_list" not in st.session_state:
    st.session_state.person_list = Person.get_all_persons()

st.write("# Analyse der Herzfrequenz-Zonen")

st.session_state.selected_person = st.selectbox("Wählen Sie eine Versuchsperson", options = [person.get_full_name() for person in st.session_state.person_list])

st.session_state.selected_person = Person.get_person_object_by_full_name(st.session_state.selected_person)

st.write(st.session_state.selected_person)
 
st.image(st.session_state.selected_person.get_picture(), caption = st.session_state.selected_person.get_full_name())

activity_data = ActivityData()

heartrate_input = st.text_input("Geben Sie ihre maximale Herzfrequenz ein (z.B. 180)")

if heartrate_input:
    activity_data.define_zones(heartrate_input)

st.write("### Zeit und Leistung pro Herzfrequenz-Zone")
st.dataframe(activity_data.get_Zeitleistung_pro_Zone())

plot = ActivityPlot(activity_data.dataframe)

st.write("### Leistungs- und Herzfrequenzverlauf")
st.plotly_chart(plot.create_plot(), use_container_width=True)
