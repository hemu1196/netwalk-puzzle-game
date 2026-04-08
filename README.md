# 🧩 NETWALK – Human vs Computer (DAA)

A Python-based interactive puzzle game built using Tkinter, demonstrating core concepts of Design and Analysis of Algorithms (DAA) such as Graphs, DFS, BFS, and Greedy Algorithms.

---

## 📌 Project Overview

NETWALK is a grid-based puzzle game where:
- Each tile represents a node (vertex)
- Connections represent edges
- The goal is to connect all tiles to a central power source

---

## 🎯 Objectives

- Connect all tiles to the power source
- Use minimum moves to solve
- Compete against a computer (Greedy strategy)

---

## 🧠 Concepts Used

### Graph Theory
- Grid → Graph
- Tiles → Vertices
- Connections → Edges

### Depth First Search (DFS)
- Used to generate a valid spanning tree
- Ensures full connectivity without cycles

### Breadth First Search (BFS)
- Used to simulate power flow
- Starts from center and spreads to connected tiles

### Greedy Algorithm
- Used by computer player
- Prioritizes tiles with higher connections

### Data Structures
- Set → store directions
- List → grid
- Queue (deque) → BFS
- Stack → DFS

---

## 🕹️ Rules & Regulations

1. Grid size is N × N
2. Center tile is the power source (cannot rotate)
3. Tiles have directions: N, E, S, W
4. Tiles rotate clockwise (90°)
5. Power flows only if connections match
6. BFS is used for power propagation
7. Human plays first
8. Computer uses Greedy strategy
9. Game ends when all tiles are powered

---

## 🏗️ System Architecture

User Interface (Tkinter)
→ Game Controller
→ Game Logic
→ Graph Algorithms (DFS, BFS, Greedy)

---

## ⚙️ Features

- Interactive GUI
- Dynamic grid size (3–15)
- Random puzzle generation
- Real-time power flow
- Human vs Computer gameplay
- Win detection

---

## 📂 Project Structure
netwalk/
│
├── DAA_R1.py
├── README.md


---

## ▶️ How to Run

```bash
git clone https://github.com/your-username/netwalk.git
cd netwalk
python main.py


---

## 🧾 Conclusion

The NETWALK project successfully demonstrates the practical application of core Design and Analysis of Algorithms (DAA) concepts in a real-world interactive system. By modeling the puzzle as a graph, the project effectively utilizes Depth First Search (DFS) to generate a valid spanning tree, Breadth First Search (BFS) to simulate power propagation, and a Greedy approach for automated decision-making by the computer player.

This project not only strengthens understanding of graph traversal algorithms but also highlights how theoretical concepts can be integrated with user interface design using Tkinter. The combination of algorithmic logic and visualization makes the system both educational and engaging.

Overall, NETWALK serves as a strong example of applying algorithmic thinking to solve problems, build interactive applications, and simulate intelligent behavior, making it a valuable learning experience in both DSA and software development.

