# IMPORT REQUIRED LIBRARIES
# ============================================================
import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
import copy

# GRAPH CONSTANTS
# ============================================================
# DIRS represents directions in the grid.
# Each direction maps to a movement (row_change, column_change)
# This is used to move from one tile to another (graph traversal).
DIRS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}
# OPPOSITE direction mapping.
# Since connections are undirected:
# If one tile connects North, the neighbor must connect South.
OPPOSITE = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E'
}
# ROTATE_MAP defines clockwise rotation of directions.
# Used when a tile is rotated by the player or computer.
ROTATE_MAP = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'
}

def rotate_set(connections):
    """
    Rotates all directions in a tile clockwise.
    Example: {'N','E'} → {'E','S'}
    """
    return {ROTATE_MAP[d] for d in connections}

# TILE CLASS (GRAPH VERTEX)
# ============================================================
class PuzzleTile:
    """
    Represents a single tile in the NetWalk grid.
    Each tile behaves like a vertex in a graph.
    """
    def __init__(self, connections=None, is_power=False):
        # connections → set of directions (edges)
        self.connections = connections if connections else set()
        # is_power → True only for center tile
        self.is_power = is_power

    def rotate_clockwise(self):
        #Rotates this tile clockwise by 90 degrees.
        self.connections = rotate_set(self.connections)

# GAME LOGIC CLASS (DFS, BFS, GREEDY)
# ============================================================
class NetPuzzle:
    def __init__(self, size=5):
        """
        Handles all core NetWalk game logic.
        Includes:
        - Puzzle generation (DFS)
        - Power propagation (BFS)
        - Computer move (Greedy + Sorting)
        """
        self.size = size
        # Create grid of tiles
        # Center tile is power source
        self.grid = [[PuzzleTile(is_power=(i == size//2 and j == size//2))
                      for j in range(size)] for i in range(size)]
        # Active matrix indicates which tiles are powered
        self.active = [[False]*size for _ in range(size)]
        # Generate a valid solved puzzle using DFS
        self._generate_solution()
        # Store the solution state for computer reference
        self.solution_state = [[copy.deepcopy(self.grid[i][j].connections)
                                for j in range(size)] for i in range(size)]
        # Randomly rotate tiles to make puzzle unsolved
        self._shuffle_tiles()
        # Compute power flow after shuffle
        self._compute_active()

    def _generate_solution(self):
        """
        Generates a fully connected valid puzzle.
        Uses Depth First Search to form a spanning tree.
        """
        n = self.size
        # Clear any existing connections
        for row in self.grid:
            for tile in row:
                tile.connections.clear()

        visited = [[False]*n for _ in range(n)]
        cx = cy = n//2    # Start DFS from power source
        visited[cx][cy] = True
        stack = [(cx, cy)]
        while stack:
            i, j = stack[-1]
            neighbors = []
            # Check unvisited neighbors
            for d, (di, dj) in DIRS.items():
                ni, nj = i+di, j+dj
                if 0 <= ni < n and 0 <= nj < n and not visited[ni][nj]:
                    neighbors.append((d, ni, nj))
             
            if not neighbors:
                stack.pop()
            else:
                # Choose random neighbor
                d, ni, nj = random.choice(neighbors)
                # Connect both tiles
                self.grid[i][j].connections.add(d)
                self.grid[ni][nj].connections.add(OPPOSITE[d])
                visited[ni][nj] = True
                stack.append((ni, nj))

     # ---------------- SHUFFLE TILES ----------------
    def _shuffle_tiles(self):
        """
        Randomly rotates tiles to scramble the puzzle.
        """
        for row in self.grid:
            for tile in row:
                if tile.is_power:
                    continue
                for _ in range(random.randint(0, 3)):
                    tile.rotate_clockwise()

    # ---------------- BFS POWER PROPAGATION ----------------
    def _compute_active(self):
        """
        Uses Breadth First Search (BFS)
        to determine which tiles receive power.
        """
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

       # ---------------- TILE ROTATION ----------------
    def rotate_tile(self, i, j):
        """
        Rotates selected tile and recomputes power flow.
        """
        self.grid[i][j].rotate_clockwise()
        self._compute_active()

     # ---------------- CHECK WIN CONDITION ----------------
    def is_solved(self):
        """
        Game is solved if all tiles are powered.
        """
        return all(all(row) for row in self.active)

    # ---------------- COMPUTER MOVE (GREEDY) ----------------
    def computer_move(self):
        """
        Computer uses Greedy strategy.
        Prioritizes tiles with higher degree (connections).
        """
        tiles = []
        for i in range(self.size):
            for j in range(self.size):
                tiles.append((len(self.solution_state[i][j]), i, j))
        # Sort tiles by degree (descending)
        tiles.sort(reverse=True)

        for _, i, j in tiles:
            if not self.grid[i][j].is_power and \
               self.grid[i][j].connections != self.solution_state[i][j]:
                self.grid[i][j].rotate_clockwise()
                self._compute_active()
                return

# UI - MAIN CONTROL
# ============================================================
class NetGameUI:
    """
    Handles all GUI operations.
    Includes Menu, Game Board, Rules, Turns.
    """
    def __init__(self, root):
        self.root = root
        self.cell = 70 # Size of each grid cell
        
        # Window setup
        root.title("NETWALK – Human vs Computer (DAA)")
        root.configure(bg="#0f172a") # Dark background
        
        self.current_frame = None
        self.show_menu()
    # ---------------- SCREEN CLEAR ----------------
    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg="#0f172a")
        self.current_frame.pack(fill="both", expand=True)

    # ---------------- MAIN MENU ----------------
    def show_menu(self):
        """
        Displays main menu screen.
        """
        self.clear_screen()
        
        # Title
        tk.Label(self.current_frame, text="N E T W A L K", 
                 font=("Segoe UI", 48, "bold"), fg="#38bdf8", bg="#0f172a").pack(pady=(50, 10))
        
        tk.Label(self.current_frame, text="23CSE211 - Design and Analysis of Algorithms", 
                 font=("Segoe UI", 14), fg="#94a3b8", bg="#0f172a").pack(pady=5)

        tk.Label(self.current_frame, text="Group No: 05", 
                 font=("Segoe UI", 12, "bold"), fg="#fbbf24", bg="#0f172a").pack(pady=5)

        # Input Frame
        params_frame = tk.Frame(self.current_frame, bg="#1e293b", pady=20, padx=40)
        params_frame.pack(pady=40)

        tk.Label(params_frame, text="Enter Grid Size (N x N):", 
                 font=("Segoe UI", 14), fg="white", bg="#1e293b").pack(side="left", padx=10)

        self.size_entry = tk.Entry(params_frame, width=5, font=("Segoe UI", 14, "bold"), justify="center")
        self.size_entry.insert(0, "7")
        self.size_entry.pack(side="left", padx=10)

        # Buttons
        btn_frame = tk.Frame(self.current_frame, bg="#0f172a")
        btn_frame.pack(pady=20)

        self.create_btn(btn_frame, "PLAY GAME", "#00ffcc", self.on_play_click).pack(pady=10, fill="x")
        self.create_btn(btn_frame, "RULES", "#fbbf24", self.show_rules).pack(pady=10, fill="x")
        self.create_btn(btn_frame, "EXIT", "#ef4444", self.root.quit).pack(pady=10, fill="x")

    def create_btn(self, parent, text, color, command):
        """
        Creates styled buttons.
        """
        return tk.Button(parent, text=text, font=("Segoe UI", 12, "bold"),
                         bg=color, fg="#0f172a", activebackground="white", 
                         width=20, pady=5, command=command)

    # ---------------- GAME SCREEN ----------------
    def on_play_click(self):
        """Reads input size and starts the game."""
        try:
            s = int(self.size_entry.get())
            if s < 3: s = 3
            if s > 15: s = 15 
        except ValueError:
            s = 7
        self.launch_game(s)

    def launch_game(self, size):
        """
        Reads grid size and starts game.
        Starts/Resets the game with the given size.
        Initializes new game.
        """
        self.size = size
        
        # Setup Transition
        self.clear_screen()
        
        # 1. Header
        header = tk.Frame(self.current_frame, bg="#87CEEB", pady=10)
        header.pack(fill="x")
        
        tk.Button(header, text="← MAIN MENU", bg="#4f46e5", fg="white", font=("Segoe UI", 10, "bold"),
                  activebackground="#4338ca", activeforeground="white", padx=10,
                  command=self.show_menu).pack(side="left", padx=10)

        tk.Label(header, text="NETWALK", font=("Segoe UI", 20, "bold"),
                 fg="#0f172a", bg="#87CEEB").pack(side="left", padx=20)
        
        tk.Button(header, text="NEW GAME", bg="#10b981", fg="white", font=("Segoe UI", 10, "bold"),
                 activebackground="#059669", activeforeground="white", padx=10,
                 command=lambda: self.launch_game(self.size)).pack(side="right", padx=10)

        # 2. Canvas Area
        self.canvas_frame = tk.Frame(self.current_frame, bg="#0f172a")
        self.canvas_frame.pack(pady=10)
        
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.size*self.cell,
            height=self.size*self.cell,
            bg="#87CEEB",
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.human_turn)

        # 3. Status
        self.status = tk.Label(self.current_frame, font=("Segoe UI", 14, "bold"),
                               fg="#e5e7eb", bg="#0f172a", text="Turn: HUMAN")
        self.status.pack(pady=10)

        # Initialize Game
        self.game = NetPuzzle(self.size)
        self.turn = "Human"
        self.winner = None
        self.draw()

    def draw(self):
        """
        Draws entire grid and connections.
        """
        self.canvas.delete("all")
        S = self.cell
        h = S // 2
        active_color = "#38bdf8"
        inactive_color = "#475569"

        for i in range(self.size):
            for j in range(self.size):
                x0, y0 = j*S, i*S
                x1, y1 = x0+S, y0+S

                self.canvas.create_rectangle(
                    x0+2, y0+2, x1-2, y1-2,
                    fill="#020617", outline="#1e293b"
                )

                tile = self.game.grid[i][j]
                cx, cy = x0+h, y0+h

                for d in tile.connections:
                    if d == 'N': x2, y2 = cx, y0
                    elif d == 'S': x2, y2 = cx, y1
                    elif d == 'W': x2, y2 = x0, cy
                    else: x2, y2 = x1, cy

                    color = active_color if self.game.active[i][j] else inactive_color
                    self.canvas.create_line(cx, cy, x2, y2, fill=color, width=4)

                if tile.is_power:
                    self.canvas.create_oval(cx-7, cy-7, cx+7, cy+7,
                                            fill="#ef4444", outline="")
                elif len(tile.connections) == 1:
                    color = active_color if self.game.active[i][j] else "#2563eb"
                    self.canvas.create_rectangle(cx-7, cy-7, cx+7, cy+7,
                                                 fill=color, outline="")
                else:
                    color = active_color if self.game.active[i][j] else inactive_color
                    self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6,
                                            fill=color, outline="")

        if self.game.is_solved():
            self.status.config(text=f"WINNER : {self.winner}", fg="#00ffcc")
        else:
            self.status.config(text=f"Turn : {self.turn}", fg="#e5e7eb")

    def human_turn(self, event):
        """
        Handles human move.
        """
        if self.game.is_solved() or self.turn != "Human":
            return

        i, j = event.y//self.cell, event.x//self.cell
        if not (0 <= i < self.size and 0 <= j < self.size):
            return
        if self.game.grid[i][j].is_power:
            return

        self.game.rotate_tile(i, j)

        if self.game.is_solved():
            self.winner = "HUMAN"
            self.draw()
            return

        self.turn = "Computer"
        self.draw()
        self.root.after(500, self.computer_turn)

    def computer_turn(self):
        """
        Executes computer move.
        """
        if self.game.is_solved():
            return

        self.game.computer_move()

        if self.game.is_solved():
            self.winner = "COMPUTER"
            self.draw()
            return

        self.turn = "Human"
        self.draw()

    def show_rules(self):
        """
        Displays game rules.
        """
        rules = """
        ----- NETWALK – Rules & Regulations -----
        1. Game board: N x N grid of tiles.
        2. Center tile: Power source (cannot be rotated).
        3. Tile connections: N, E, S, W.
        4. Rotation: Clockwise 90 deg.
        5. Power flow: Matching connections between tiles.
        6. Power spread: BFS from source.
        7. Active tile: Connected to source.
        8. Turns: Human first, then computer (greedy).
        9. Win condition: All tiles lit up.
        """
        messagebox.showinfo("Rules", rules)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x800")
    app = NetGameUI(root)
    root.mainloop()
