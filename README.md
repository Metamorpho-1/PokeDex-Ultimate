🔴 PokeDex Ultimate
A sleek, modern, and fully animated Pokedex built entirely in Python. I built this to bring some serious UI polish and interactive design to HackJKLU 5.0. It completely ditches the boring console output for a dark-mode GUI that feels like a real, premium desktop app.

✨ Features
Dynamic Type Theming: The UI automatically shifts its accent colors to match the Pokemon's primary element (e.g., green for Grass, red for Fire, yellow for Electric).

Animated Base Stats: Watch the HP, Attack, Defense, and Speed progress bars smoothly animate and fill up in real-time when a Pokemon is searched.

Deep Lore Integration: Doesn't just fetch raw stats—it hits the pokemon-species API endpoint to pull the actual official flavor text and descriptions from the games.

HD Visuals: Serves up high-resolution official vector-style artwork instead of pixelated retro sprites, perfectly scaled for modern displays.

Modern GUI: Powered by CustomTkinter for a seamless, rounded, dark-mode aesthetic.

🛠️ Tech Stack
Language: Python 3.x

GUI Framework: customtkinter

Image Processing: Pillow (PIL)

Data Fetching: requests & PokeAPI

🚀 How to Run It
Clone this repository:

Bash
git clone https://github.com/yourusername/pokedex-ultimate.git
cd pokedex-ultimate
Install the required dependencies:

Bash
pip install customtkinter requests pillow
Boot up the Pokedex:

Bash
python main.py
(Note: Make sure your Python file is named main.py or replace this command with your actual file name!)
#!/bin/bash

echo "🔴 Welcome to PokeDex Ultimate Setup!"

# 1. Create a virtual environment so dependencies don't mess with system Python
echo "📦 Creating a Python virtual environment..."
python3 -m venv venv

# 2. Activate the virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# 3. Upgrade pip and install the required libraries
echo "⬇️ Installing required packages (customtkinter, requests, Pillow)..."
pip install --upgrade pip
pip install customtkinter requests pillow

# 4. Run the application
echo "🚀 Launching the Pokedex..."
python main.py

# 5. Deactivate the virtual environment when the app is closed
deactivate
echo "🛑 Pokedex closed. Virtual environment deactivated."
