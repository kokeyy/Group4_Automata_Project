import streamlit as st

st.title("Welcome to the Automaton App")

if st.button("First DFA"):
    st.switch_page("DFA1.py")
if st.button("Second DFA"):
    st.switch_page("DFA2.py")