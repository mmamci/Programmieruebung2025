import streamlit as st

from src.read_data import get_person_names, get_person_image_by_name  
from src.analyze_activity_data import ActivityData, ActivityPlot

if "selected_person" not in st.session_state:
    st.session_state.selected_person = "NONE"


st.write("# Analyse der Herzfrequenz-Zonen")


st.session_state.selected_person = st.selectbox("Wählen Sie eine Versuchsperson", options = get_person_names())

st.write(st.session_state.selected_person)

st.image(get_person_image_by_name(st.session_state.selected_person), caption = st.session_state.selected_person)

activity_data = ActivityData()

heartrate_input = st.text_input("Geben Sie ihre maximale Herzfrequenz ein (z.B. 180)")

if heartrate_input:
    activity_data.define_zones(heartrate_input)

st.write("### Zeit und Leistung pro Herzfrequenz-Zone")
st.dataframe(activity_data.get_Zeitleistung_pro_Zone())

plot = ActivityPlot(activity_data.dataframe)

st.write("### Leistungs- und Herzfrequenzverlauf")
st.plotly_chart(plot.create_plot(), use_container_width=True)