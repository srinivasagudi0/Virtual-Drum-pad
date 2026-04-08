import streamlit as st

st.title("Band")

st.header("Click buttons and see the magic!")

if st.button("Crash Cymbal"):
    st.write("Crash!")

if st.button("Hi Hat"):
    st.write("Tss!")

if st.button("Snare Drum"):
    st.write("Boom!")

if st.button("Bass Drum"):
    st.write("Dum!")

if st.button("Rack Tom 1"):
    st.write("Tock!")

if st.button("Rack Tom 2"):
    st.write("Tock!")

if st.button("Ride Cymbal"):
    st.write("Ting!")

if st.button("Floor Tom"):
    st.write("Tock!")

