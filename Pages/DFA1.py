import streamlit as st
import graphviz
import time
import pathlib
from PIL import Image

# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the external CSS
css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

# --- DFA Class ---
class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            current_state = self.transition_function.get(current_state, {}).get(symbol)
            if current_state is None:
                return False
        return current_state in self.accept_states

def simulate_dfa(dfa, input_string):
    path = []
    current_state = dfa.start_state
    path.append((current_state, None))

    for symbol in input_string:
        next_state = dfa.transition_function.get(current_state, {}).get(symbol)
        if next_state is None:
            return path, False, f"No transition from {current_state} on '{symbol}'"
        path.append((next_state, symbol))
        current_state = next_state

    return path, current_state in dfa.accept_states, None

def draw_dfa(dfa, path=[], active_state=None, active_color="lightgreen", edge_color="green"):
    dot = graphviz.Digraph(engine='dot')
    dot.attr(rankdir='LR')  # Make layout horizontal
    path_edges = set()
    visited_nodes = set()

    for i in range(1, len(path)):
        from_state, symbol = path[i-1]
        to_state, _ = path[i]
        path_edges.add((from_state, to_state, symbol))
        visited_nodes.add(from_state)
        visited_nodes.add(to_state)

    for state in dfa.states:
        if state == active_state:
            dot.node(state, shape="doublecircle" if state in dfa.accept_states else "circle", style="filled", color=active_color)
        elif state in visited_nodes:
            dot.node(state, shape="doublecircle" if state in dfa.accept_states else "circle", style="filled", color="palegreen")
        else:
            dot.node(state, shape="doublecircle" if state in dfa.accept_states else "circle")

    dot.node("start", shape="none", label="")
    dot.edge("start", dfa.start_state)

    for from_state, trans in dfa.transition_function.items():
        for symbol, to_state in trans.items():
            if (from_state, to_state, symbol) in path_edges:
                dot.edge(from_state, to_state, label=symbol, color=edge_color, penwidth="2")
            else:
                dot.edge(from_state, to_state, label=symbol)

    return dot

def draw_input_pointer(input_string, position):
    spaced_input = '  '.join(input_string)
    pointer = '   ' * position + '^'
    return spaced_input + "\n" + pointer

# --- DFA Definition ---
dfa_letter = {
    'q0':{'0':'q1','1':'q2'},
    'q1':{'1':'q3','0':'q5'},
    'q2':{'1':'q5','0':'q4'},
    'q3':{'0':'q5', '1':'q5'},
    'q4':{'0':'q5', '1':'q5'},
    'q5':{'0':'q6','1': 'q6'},
    'q6':{'0':'q7','1':'q7'},
    'q7':{'0':'q8','1':'q9'},
    'q8':{'0':'q10','1':'q9'},
    'q9':{'0':'q11','1':'q12' },
    'q10':{'0':'q14','1':'q14'},
    'q11':{'0':'q14','1':'q14'},
    'q12':{'0':'q13','1':'q14'},
    'q13':{'0':'q11','1':'q14'},
    'q14':{'0':'q15','1':'q16'},
    'q15':{'0':'q17','1':'q16'},
    'q16':{'1':'q18','0':'q19'},
    'q17':{'0':'q20','1':'q20'},
    'q18':{'0':'q20','1':'q20'},
    'q19':{'0':'q20','1':'q20'},
    'q20':{'0':'q20','1':'q20'}
}
states = set(dfa_letter.keys())
alphabet = {'1', '2'}
start_state = 'q0'
accept_states = {'q20'}

dfa = DFA(states, alphabet, dfa_letter, start_state, accept_states)

# --- Streamlit Interface ---
st.html("<h1 style = 'text-align: center;'>1st DFA Visualizer </h1>")
st.html("<p> For Regular Expression: (1+0)* (11 + 00 +101 + 010) (1+0)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)* </p>")
active_color = st.color_picker("Pick a color for the active state highlight:", "#90ee90")
edge_color = st.color_picker("Pick a color for the transition trail:", "#32CD32")
input_string = st.text_input("Enter input string of '1' and '0':", key = 'styledinput')

if input_string:
    path, accepted, error = simulate_dfa(dfa, input_string)

    if error:
        st.error(error)
    else:
        st.subheader("Step-by-step Simulation:")
        placeholder = st.empty()
        pointer_placeholder = st.empty()
        result = "✅ Accepted" if accepted else "❌ Rejected"
  

        for i, (state, symbol) in enumerate(path):
            with placeholder.container():
                st.graphviz_chart(draw_dfa(dfa, path[:i+1], active_state=state, active_color=active_color, edge_color=edge_color))
            with pointer_placeholder.container():
                st.code(draw_input_pointer(input_string, i-1 if i > 0 else 0), language="markdown")
                st.write(f"**Current State:** {state}, **Symbol:** {symbol if symbol else 'Start'}")
            time.sleep(1)

        if accepted:
            st.success(f"✅ The string '{input_string}' is ACCEPTED.")
        else:
            st.error(f"❌ The string '{input_string}' is REJECTED.")

st.subheader("Full DFA Diagram")
st.graphviz_chart(draw_dfa(dfa, edge_color=edge_color))

image = Image.open("Images/DFA1.png")
# Session state to remember toggle
if "show_img" not in st.session_state:
    st.session_state.show_img = False


st.html("<h1 style = 'text-align: center;'>Other Langauges for this Regex </h1>")

with st.expander("CFG for this Regex"):
    st.markdown("""
S → X1 X2 X3 X4 X5 X6 X7 X8 X9 X10

X1 → 1 X1 | 0 X1 | λ  
X2 → 1 1 | 0 0 | 1 0 1 | 0 1 0  
X3 → 1 X3 | 0 X3 | λ  
X4 → 1 1 | 0 0 | 0 | 1  
X5 → 1 | 0 | 1 1  
X6 → 1 1 X6 | 0 0 X6 | λ  
X7 → 1 0 1 | 0 0 0 | 1 1 1  
X8 → 1 X8 | 0 X8 | λ  
X9 → 1 0 1 | 0 0 0 | 1 1 1 | 0 0 1 | 1 0 0  
X10 → 1 1 X10 | 0 0 X10 | 1 X10 | 0 X10 | λ
    """)
# Button to toggle visibility
if st.button("Show/Hide PDA"):
    st.session_state.show_img = not st.session_state.show_img

# Show the image if toggled on
if st.session_state.show_img:
    st.image(image, caption="PDA for this Regex", use_column_width=True)

if st.button("Go back", key = 'pulse2'):
    st.switch_page("Home.py")
