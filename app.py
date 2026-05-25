import streamlit as st
import subprocess

st.title("🧩 NETWALK – Human vs Computer")

st.write("DAA Puzzle Game using DFS, BFS and Greedy Algorithms")

if st.button("Start Game"):
    subprocess.run(["python", "DAA_R1.py"])
