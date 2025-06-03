import tkinter as tk
import time
import matplotlib.pyplot as plt
import numpy as np
from timeit import default_timer as timer

class WalkSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Walking on Words Simulation")

        # Input fields for words u and w
        self.label_u = tk.Label(root, text="Enter word to walk on (u):")
        self.label_u.pack()
        self.entry_u = tk.Entry(root, width=30)
        self.entry_u.pack()

        self.label_w = tk.Label(root, text="Enter word to generate (w):")
        self.label_w.pack()
        self.entry_w = tk.Entry(root, width=30)
        self.entry_w.pack()

        # Start button
        self.start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        # Feedback Label for showing actions
        self.feedback_label = tk.Label(root, text="", font=("Arial", 16), fg="blue")
        self.feedback_label.pack()

        # Canvas to visualize the word walking
        self.canvas = tk.Canvas(root, width=500, height=100)
        self.canvas.pack()

        # Text ID for canvas, to update the visuals
        self.text_ids = []

        # Add a color key/legend for user reference
        self.color_key_frame = tk.Frame(root)
        self.color_key_frame.pack()

        self.add_color_key()

        # For graphing efficiency
        self.time_data = []        # Store times for each run
        self.input_sizes = []       # Store combined input sizes for each run

    def add_color_key(self):
        # Add color key labels to the frame
        tk.Label(self.color_key_frame, text="Color Key:").pack(side=tk.LEFT)
        tk.Label(self.color_key_frame, text="Stay", fg="green").pack(side=tk.LEFT, padx=10)
        tk.Label(self.color_key_frame, text="Move Left", fg="yellow").pack(side=tk.LEFT, padx=10)
        tk.Label(self.color_key_frame, text="Move Right", fg="blue").pack(side=tk.LEFT, padx=10)

    def start_simulation(self):
        # Clear previous simulations
        self.canvas.delete("all")
        self.feedback_label.config(text="")
        self.text_ids = []

        # Get the words from input fields
        u = self.entry_u.get()
        w = self.entry_w.get()
        
        # Calculate the combined size of the input (size of u + size of w)
        size_of_input = len(u) + len(w)

        # Draw the word on the canvas (for u)
        self.draw_word(u)

        # Measure start time
        start_time = timer()

        # Simulate the walking process
        if self.can_generate_dp(u, w):
            self.feedback_label.config(text=f"Successfully generated '{w}' from '{u}'!", fg="green")
        else:
            self.feedback_label.config(text=f"Failed to generate '{w}' from '{u}'", fg="red")

        # Measure end time and calculate elapsed time
        elapsed_time = timer() - start_time

        # Store size of input and elapsed time for graphing
        self.input_sizes.append(size_of_input)
        self.time_data.append(elapsed_time)

        # Show efficiency graph after the simulation is done
        self.show_efficiency_graph()

    def draw_word(self, word):
        # Draw each letter in the word on the canvas
        x_offset = 50
        for index, letter in enumerate(word):
            text_id = self.canvas.create_text(x_offset + index * 20, 50, text=letter, font=("Arial", 20))
            self.text_ids.append(text_id)

    def highlight_letter(self, index, color="yellow"):
        # Highlight the letter at a given index
        self.canvas.itemconfig(self.text_ids[index], fill=color)
        self.root.update()
        time.sleep(0.2)

    def reset_highlight(self, index):
        # Reset the highlight to black
        self.canvas.itemconfig(self.text_ids[index], fill="black")
        self.root.update()

    def display_action(self, action, color):
        # Update the feedback label to show the current action with the matching color
        self.feedback_label.config(text=action, fg=color)
        self.root.update()

    
    def can_generate_dp(self, u, w):
        m = len(u)
        n = len(w)

        # Early termination if generator word is longer
        if m > n:
            return False

        # DP table to store whether prefix w[1:j] can be generated from u[1:i]
        dp = [[False for _ in range(n + 1)] for _ in range(m + 1)]

        # Initialize: First character must match to start the generation
        for i in range(1, m + 1):
            dp[i][1] = (u[i - 1] == w[0])
            if dp[i][1]:
                self.display_action(f"Start from position {i} ('{u[i - 1]}') to generate '{w[0]}'", "green")
                self.highlight_letter(i - 1, "green")

        # Iterate over each prefix of w (j = 2 to n)
        for j in range(2, n + 1):
            for i in range(1, m + 1):
                if u[i - 1] == w[j - 1]:
                    # Stay on current position
                    if dp[i][j - 1]:
                        dp[i][j] = True
                        self.display_action(f"Stay at position {i} ('{u[i - 1]}') to match '{w[j - 1]}'", "green")
                        self.highlight_letter(i - 1, "green")
                        time.sleep(0.3)
                        self.reset_highlight(i - 1)

                    # Move left
                    if i > 1 and dp[i - 1][j - 1]:
                        dp[i][j] = True
                        self.display_action(f"Move left to position {i - 1} ('{u[i - 2]}') to match '{w[j - 1]}'", "yellow")
                        self.highlight_letter(i - 2, "yellow")
                        time.sleep(0.3)
                        self.reset_highlight(i - 2)

                    # Move right
                    if i < m and dp[i + 1][j - 1]:
                        dp[i][j] = True
                        self.display_action(f"Move right to position {i + 1} ('{u[i]}') to match '{w[j - 1]}'", "blue")
                        self.highlight_letter(i, "blue")
                        time.sleep(0.3)
                        self.reset_highlight(i)

        # Check if any dp state at position [i][n] is True
        for i in range(1, m + 1):
            if dp[i][n]:
                return True

        return False

# Run the Tkinter program
if __name__ == "__main__":
    root = tk.Tk()
    app = WalkSimulation(root)
    root.mainloop()
