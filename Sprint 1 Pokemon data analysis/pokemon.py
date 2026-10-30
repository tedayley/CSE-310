import tkinter as tk
from tkinter import messagebox
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def load_and_analyze(csv_path):
    data = pd.read_csv(csv_path)

    required = {"name", "weight_kg", "height_m", "pokedex_number"}
    missing_columns = required - set(data.columns)
    if missing_columns:
        raise ValueError(
            "The CSV is missing these required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # Convert relevant columns to numeric values, safely handling blanks.
    for column in ("weight_kg", "height_m", "pokedex_number"):
        data[column] = pd.to_numeric(data[column], errors="coerce")

    weighted = data.dropna(subset=["weight_kg"])
    if weighted.empty:
        raise ValueError("No usable Pokemon weight data was found.")

    heaviest = weighted.loc[weighted["weight_kg"].idxmax()]

    number_570 = data[data["pokedex_number"] == 570]
    average_height = data["height_m"].mean()  # pandas skips missing heights

    return data, heaviest, number_570, average_height


class PokemonExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon CSV Explorer")
        self.root.geometry("650x420")
        self.root.minsize(560, 380)

        self.csv_path = Path(__file__).resolve().with_name("pokemon.csv")
        self.data = None

        title = tk.Label(
            root,
            text="Pokémon CSV Explorer",
            font=("TkDefaultFont", 19, "bold"),
            pady=12,
        )
        title.pack()

        self.path_label = tk.Label(
            root, text=f"CSV: {self.csv_path}", wraplength=610
        )
        self.path_label.pack(pady=(0, 8))

        self.results = tk.Frame(root, padx=18, pady=10)
        self.results.pack(fill=tk.BOTH, expand=True)

        self.answer_labels = []
        for _ in range(3):
            label = tk.Label(
                self.results,
                text="Loading Pokémon data…",
                anchor="w",
                justify="left",
                wraplength=590,
                font=("TkDefaultFont", 11),
                pady=8,
            )
            label.pack(fill=tk.X)
            self.answer_labels.append(label)

        # Automatically load the adjacent pokemon.csv when available.
        if self.csv_path.exists():
            self.analyze()

    def analyze(self):
        try:
            data, heaviest, number_570, average_height = load_and_analyze(
                self.csv_path
            )
        except Exception as error:
            messagebox.showerror("Could not analyze CSV", str(error))
            return

        self.data = data

        self.answer_labels[0].config(
            text=(
                f"1. Heaviest Pokémon: {heaviest['name']} — "
                f"{heaviest['weight_kg']:,.1f} kg"
            )
        )

        if number_570.empty: #Should never happen because Zorua is the best, but redundency is redundency.
            dex_answer = "No Pokémon with Pokédex number 570 was found."
        else:
            names = ", ".join(number_570["name"].fillna("Unknown").astype(str))
            dex_answer = f"2. Pokédex #570: {names}"
        self.answer_labels[1].config(text=dex_answer)

        if pd.isna(average_height):
            height_answer = "3. Average height: no usable height data found."
        else:
            known_count = int(data["height_m"].notna().sum())
            height_answer = (
                f"3. Average height: {average_height:.3f} m "
                f"({known_count} Pokémon with recorded heights)"
            )
        self.answer_labels[2].config(text=height_answer)

        self.show_graph()

    def show_graph(self):
        if self.data is None:
            return

        heaviest_ten = (
            self.data.dropna(subset=["weight_kg"])
            .nlargest(10, "weight_kg")
            .sort_values("weight_kg")
        )

        # Make a separate Matplotlib window so the Tkinter app stays open.
        fig, ax = plt.subplots(figsize=(9, 6))
        bars = ax.barh(heaviest_ten["name"], heaviest_ten["weight_kg"])
        ax.set_title("The 10 Heaviest Pokémon")
        ax.set_xlabel("Weight (kg)")
        ax.set_ylabel("Pokémon")
        ax.grid(axis="x", linestyle="--", alpha=0.35)
        ax.bar_label(bars, fmt="%.1f kg", padding=3)
        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    window = tk.Tk()
    app = PokemonExplorer(window)
    window.mainloop()
