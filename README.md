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
