import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image
from io import BytesIO

ctk.set_appearance_mode("dark")

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"

# Pokemon Type Colors for dynamic UI theming
TYPE_COLORS = {
    "normal": "#A8A77A", "fire": "#EE8130", "water": "#6390F0",
    "electric": "#F7D02C", "grass": "#7AC74C", "ice": "#96D9D6",
    "fighting": "#C22E28", "poison": "#A33EA1", "ground": "#E2BF65",
    "flying": "#A98FF3", "psychic": "#F95587", "bug": "#A6B91A",
    "rock": "#B6A136", "ghost": "#735797", "dragon": "#6F35FC",
    "dark": "#705746", "steel": "#B7B7CE", "fairy": "#D685AD"
}

class PokeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PokeDex Ultimate")
        self.geometry("450x800")
        self.resizable(False, False)

        # Main Scrollable Card
        self.main_card = ctk.CTkScrollableFrame(self, fg_color="#242424", corner_radius=20)
        self.main_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Search Area
        self.search_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.search_frame.pack(pady=(10, 10))

        self.entry_name = ctk.CTkEntry(self.search_frame, placeholder_text="Enter Pokemon...", 
                                       width=200, height=40, font=("Helvetica", 16))
        self.entry_name.pack(side="left", padx=10)

        self.btn_search = ctk.CTkButton(self.search_frame, text="Search", command=self.get_pokemon, 
                                        width=90, height=40, fg_color="#E3350D", hover_color="#B32A0A", 
                                        font=("Helvetica", 14, "bold"))
        self.btn_search.pack(side="left")

        # HD Image Container
        self.image_label = ctk.CTkLabel(self.main_card, text="", width=250, height=250)
        self.image_label.pack(pady=10)

        # Basic Info
        self.lbl_name = ctk.CTkLabel(self.main_card, text="---", font=("Helvetica", 28, "bold"))
        self.lbl_name.pack()
        
        self.lbl_type = ctk.CTkLabel(self.main_card, text="---", font=("Helvetica", 18))
        self.lbl_type.pack(pady=5)

        self.lbl_stats = ctk.CTkLabel(self.main_card, text="---", 
                                      font=("Helvetica", 14, "italic"), text_color="#A0A0A0")
        self.lbl_stats.pack(pady=(0, 15))

        # Pokedex Entry Text
        self.lbl_desc = ctk.CTkLabel(self.main_card, text="Waiting for data...", wraplength=350, 
                                     font=("Helvetica", 14), text_color="#CCCCCC", justify="center")
        self.lbl_desc.pack(pady=10, padx=20)

        # Base Stats Section
        self.stats_frame = ctk.CTkFrame(self.main_card, fg_color="#333333", corner_radius=15)
        self.stats_frame.pack(pady=20, fill="x", padx=10, ipady=10)
        
        ctk.CTkLabel(self.stats_frame, text="Base Stats", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Create progress bars for stats
        self.stat_bars = {}
        stat_names = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
        
        for stat in stat_names:
            row = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            
            lbl = ctk.CTkLabel(row, text=stat.upper().replace("-", " "), width=100, anchor="w", font=("Helvetica", 12))
            lbl.pack(side="left")
            
            bar = ctk.CTkProgressBar(row, width=200, height=12, progress_color="#E3350D")
            bar.set(0) # Start at 0
            bar.pack(side="left", padx=10)
            
            val_lbl = ctk.CTkLabel(row, text="0", width=30, anchor="e", font=("Helvetica", 12))
            val_lbl.pack(side="right")
            
            self.stat_bars[stat] = {"bar": bar, "label": val_lbl}

    def get_pokemon(self):
        name = self.entry_name.get().lower().strip()
        if not name:
            return

        try:
            # Fetch Main Data
            response = requests.get(f"{BASE_URL}{name}")
            if response.status_code == 200:
                data = response.json()
                
                # Fetch Species Data for Pokedex Entry
                species_response = requests.get(f"{SPECIES_URL}{data['id']}")
                species_data = species_response.json() if species_response.status_code == 200 else None

                self.update_ui(data, species_data)
            else:
                messagebox.showerror("Error", "Pokemon not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def update_ui(self, data, species_data):
        self.lbl_name.configure(text=f"{data['name'].capitalize()} (#{data['id']})")
        
        # Get Primary Type for UI Theme Color
        primary_type = data['types'][0]['type']['name']
        theme_color = TYPE_COLORS.get(primary_type, "#E3350D")
        
        # Update UI Colors
        self.btn_search.configure(fg_color=theme_color, hover_color=theme_color)
        
        types = " / ".join([t['type']['name'].capitalize() for t in data['types']])
        self.lbl_type.configure(text=f"Type: {types}", text_color=theme_color)
        
        self.lbl_stats.configure(text=f"Height: {data['height']/10}m  |  Weight: {data['weight']/10}kg")

        # Parse Description (Find the first English entry and clean up hidden linebreaks)
        if species_data:
            entries = species_data.get('flavor_text_entries', [])
            eng_entry = next((entry['flavor_text'] for entry in entries if entry['language']['name'] == 'en'), "No description available.")
            eng_entry = eng_entry.replace('\n', ' ').replace('\f', ' ')
            self.lbl_desc.configure(text=f'"{eng_entry}"')
        else:
            self.lbl_desc.configure(text="Description not available.")

        # Fetch Crystal Clear Artwork
        hd_url = data['sprites']['other']['official-artwork']['front_default']
        if hd_url:
            img_response = requests.get(hd_url)
            img_data = Image.open(BytesIO(img_response.content))
            photo = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(250, 250))
            self.image_label.configure(image=photo)

        # Trigger Stat Bar Animations
        self.trigger_stat_animations(data['stats'], theme_color)

    def trigger_stat_animations(self, stats_data, color):
        for stat in stats_data:
            stat_name = stat['stat']['name']
            target_value = stat['base_stat']
            
            if stat_name in self.stat_bars:
                bar_ui = self.stat_bars[stat_name]
                bar_ui["bar"].configure(progress_color=color)
                # Reset to 0 before animating
                bar_ui["bar"].set(0)
                bar_ui["label"].configure(text="0")
                
                # Start animation loop for this specific bar
                self.animate_bar(bar_ui, target_value, 0)

    def animate_bar(self, bar_ui, target_value, current_value):
        # 255 is the max possible base stat in Pokemon (Blissey's HP)
        MAX_STAT = 255 
        
        if current_value < target_value:
            # Increase value (speed of animation)
            current_value += 3 
            if current_value > target_value:
                current_value = target_value
                
            # Update UI
            bar_ui["bar"].set(current_value / MAX_STAT)
            bar_ui["label"].configure(text=str(current_value))
            
            # Schedule next frame of animation (15 milliseconds)
            self.after(15, self.animate_bar, bar_ui, target_value, current_value)

if __name__ == "__main__":
    app = PokeApp()
    app.mainloop()
