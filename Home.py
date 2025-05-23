import streamlit as st
import pathlib

# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the external CSS
css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

st.html("<h1 style = 'text-align: center;'> Group Project in Automata</h1>")
st.html("<h2 style = 'text-align: center;'> By Group 6</h2>")

col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])

with col2:
    if st.button("1st DFA", key = 'pulse'):
        st.switch_page("Pages/DFA1.py")
with col4:        
    if st.button("2nd DFA", key = 'pulse2'):
        st.switch_page("Pages/DFA2.py")
