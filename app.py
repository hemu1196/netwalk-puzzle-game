import streamlit as st
import random
from collections import deque
import copy

# ============================================================
# CONSTANTS
# ============================================================

DIRS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

OPPOSITE = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E'
}

ROTATE_MAP = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'
}

# ============================================================
# HELPERS
# ============================================================

def rotate_set(connections):
    return {ROTATE_MAP[d] for d in connections}

# ============================================================
# TILE CLASS
# ============================================================

class PuzzleTile:
    def __init__(self, connections=None, is_power=False):
        self.connections = connections if connections else set()
        self.is_power = is_power

    def rotate_clockwise(self):
        self.connections = rotate_set(self.connections)

# ============================================================
# GAME LOGIC
# ============================================================

class NetPuzzle:
    def __init__(self, size=5):
        self.size = size

        self.grid = [[PuzzleTile(is_power=(i == size//2 and j == size//2))
                      for j in range(size)] for i in range(size)]

        self.active = [[False]*size for _ in range(size)]

        self.generate_solution()

        self.solution_state = [[copy.deepcopy(self.grid[i][j].connections)
                                for j in range(size)] for i in range(size)]

        self.shuffle_tiles()

        self.compute_active()

    def generate_solution(self):
        n = self.size

        for row in self.grid:
            for tile in row:
                tile.connections.clear()

        visited = [[False]*n for _ in range(n)]

        cx = cy = n//2

        visited[cx][cy] = True

        stack = [(cx, cy)]

        while stack:
            i, j = stack[-1]

            neighbors = []

            for d, (di, dj) in DIRS.items():
                ni, nj = i+di, j+dj

                if 0 <= ni < n and 0 <= nj < n and not visited[ni][nj]:
                    neighbors.append((d, ni, nj))

            if not neighbors:
                stack.pop()

            else:
                d, ni, nj = random.choice(neighbors)

                self.grid[i][j].connections.add(d)
                self.grid[ni][nj].connections.add(OPPOSITE[d])

                visited[ni][nj] = True

                stack.append((ni, nj))

    def shuffle_tiles(self):
        for row in self.grid:
            for tile in row:
                if tile.is_power:
                    continue

                for _ in range(random.randint(0, 3)):
                    tile.rotate_clockwise()

    def compute_active(self):
        n = self.size

        self.active = [[False]*n for _ in range(n)]

        cx = cy = n//2

        self.active[cx][cy] = True

        q = deque([(cx, cy)])

        while q:
            i, j = q.popleft()

            for d in self.grid[i][j].connections:
                ni, nj = i+DIRS[d][0], j+DIRS[d][1]

                if 0 <= ni < n and 0 <= nj < n:
                    if OPPOSITE[d] in self.grid[ni][nj].connections and not self.active[ni][nj]:
                        self.active[ni][nj] = True
                        q.append((ni, nj))

    def rotate_tile(self, i, j):
        if not self.grid[i][j].is_power:
            self.grid[i][j].rotate_clockwise()
            self.compute_active()

    def is_solved(self):
        return all(all(row) for row in self.active)

# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(page_title="NETWALK", layout="centered")

st.title("🧩 NETWALK – Human vs Computer")

if "game" not in st.session_state:
    st.session_state.game = NetPuzzle(5)

game = st.session_state.game

st.write("Rotate tiles to connect the network!")

for i in range(game.size):

    cols = st.columns(game.size)

    for j in range(game.size):

        tile = game.grid[i][j]

        txt = ""

        if tile.is_power:
            txt = "⚡"

        else:
            txt = "".join(sorted(tile.connections))

        if cols[j].button(txt, key=f"{i}-{j}"):

            game.rotate_tile(i, j)

            st.rerun()

if game.is_solved():
    st.success("🎉 Puzzle Solved!")
