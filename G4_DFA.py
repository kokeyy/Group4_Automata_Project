import streamlit as st
import graphviz
import time

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
    'q0':{'a':'q1','b':'q2'},
    'q1':{'a':'q3','b':'q2'},
    'q2':{'b':'q3','a':'q1'},
    'q3':{'a':'q4','b':'q5'},
    'q4':{'a':'q3','b':'q6'},
    'q5':{'a':'q6','b':'q3'},
    'q6':{'a':'q7','b':'q8'},
    'q7':{'a':'q8','b':'q9'},
    'q8':{'a':'q10','b':'q11'},
    'q9':{'a':'q12','b':'T' },
    'q10':{'a':'T','b':'q12'},
    'q11':{'a':'q12','b':'q12'},
    'q12':{'a':'q13','b':'q14'},
    'q13':{'a':'q16','b':'q15'},
    'q14':{'a':'q12','b':'q16'},
    'q15':{'a':'q16','b':'q12'},
    'q16':{'a':'q17','b':'q18'},
    'q17':{'a':'q19','b': 'T'},
    'q18':{'a':'q20', 'b': 'q21'},
    'q19':{'a':'q22','b':'T'},
    'q20':{'a':'T','b':'q22'},
    'q21':{'a':'q22','b':'T'},
    'q22':{'a':'q22', 'b': 'q18'},
    'T':{'a':'T','b':'T'}
}
states = set(dfa_letter.keys())
alphabet = {'a', 'b'}
start_state = 'q0'
accept_states = {'q22'}

dfa = DFA(states, alphabet, dfa_letter, start_state, accept_states)

# --- Streamlit Interface ---
st.title("🔄 DFA Visualizer with Trail & Custom Colors")

active_color = st.color_picker("Pick a color for the active state highlight:", "#90ee90")
edge_color = st.color_picker("Pick a color for the transition trail:", "#32CD32")
input_string = st.text_input("Enter input string of 'a' and 'b':")

if input_string:
    path, accepted, error = simulate_dfa(dfa, input_string)

    if error:
        st.error(error)
    else:
        st.subheader("Step-by-step Simulation:")
        placeholder = st.empty()
        pointer_placeholder = st.empty()

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

st.subheader("📌 Full DFA Diagram")
st.graphviz_chart(draw_dfa(dfa, edge_color=edge_color))
