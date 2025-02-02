import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to simulate health and update graph
def simulate_health():
    try:
        # Get input values
        temp = temp_slider.get()
        co2 = co2_slider.get()
        moisture = moisture_slider.get()
        nitrogen = nitrogen_slider.get()
        phosphorus = phosphorus_slider.get()
        potassium = potassium_slider.get()
        fragmentation = fragmentation_var.get()
        remediation = remediation_var.get()

        # Calculate health score
        health = (0.7 if 10 <= temp <= 20 else 0.85)
        health *= (0.9 if 20 <= moisture <= 40 else 1.1)
        health *= (1.0 if nitrogen >= 10 and phosphorus >= 5 and potassium >= 5 else 0.7)
        health *= (0.85 if fragmentation == "High" else 1.0)

        # Apply remediation impact
        remediation_impact = {
            "Biochar": 1.1, "Inoculation": 1.2, "Compost": 1.05, "Humic Substances": 1.1
        }
        health *= remediation_impact.get(remediation, 1.0)

        # Clamp health between 0 and 1
        health = max(0.0, min(1.0, health))

        # Update health bar and labels
        health_bar["value"] = health * 100
        baseline_health_label.config(text=f"🌱 Baseline Health: {health:.2f}")

        # Determine outcome message
        if health <= 0.6:
            outcome = "⚠️ Poor soil health: Immediate intervention needed."
            health_bar["style"] = "red.Horizontal.TProgressbar"
        elif health <= 0.79:
            outcome = "🔄 Moderate soil health: Some issues present."
            health_bar["style"] = "yellow.Horizontal.TProgressbar"
        else:
            outcome = "✅ Good soil health: Mycorrhizal networks are thriving!"
            health_bar["style"] = "green.Horizontal.TProgressbar"

        outcome_message_label.config(text=outcome)

        # Update graph
        update_graph(temp, co2, moisture, nitrogen, phosphorus, potassium, health)

    except ValueError:
        messagebox.showerror("Oops! 🚨", "Please enter valid numbers.")

# Function to update graph
def update_graph(temp, co2, moisture, nitrogen, phosphorus, potassium, health):
    ax.clear()
    categories = ["Temp", "CO₂", "Moisture", "N", "P", "K", "Health"]
    values = [temp / 50, co2 / 800, moisture / 100, nitrogen / 50, phosphorus / 50, potassium / 50, health]

    ax.bar(categories, values, color=["#A3D9FF", "#96E6B3", "#FFD3B5", "#FF9AA2", "#D7BCE8", "#FBC3C3", "#FF8080"])
    ax.set_ylim(0, 1)
    ax.set_title("Soil Health Parameters 📊", fontsize=12, color="#30475E", fontweight="bold")
    ax.set_facecolor("#FAF3E0")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    canvas.draw()

# Create main window
root = tk.Tk()
root.title("🌱 Mycorrhizal Health Simulator")
root.geometry("750x750")
root.configure(bg="#F3E8EE")

# Style Configuration
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, relief="flat", background="#FFD3B5")
style.configure("TLabel", font=("Arial", 11), background="#F3E8EE")
style.configure("TProgressbar", troughcolor="white", background="#A3D9FF")
style.configure("green.Horizontal.TProgressbar", troughcolor="white", background="lightgreen")
style.configure("yellow.Horizontal.TProgressbar", troughcolor="white", background="gold")
style.configure("red.Horizontal.TProgressbar", troughcolor="white", background="salmon")

# Input Frame
input_frame = ttk.LabelFrame(root, text="🔢 Input Parameters", padding=10, style="TLabel")
input_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Temperature Slider
ttk.Label(input_frame, text="🌡 Temperature (°C):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
temp_slider = ttk.Scale(input_frame, from_=0, to=50, orient="horizontal")
temp_slider.set(25)
temp_slider.grid(row=0, column=1, padx=5, pady=5)

# CO2 Slider
ttk.Label(input_frame, text="🌍 CO₂ Levels (ppm):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
co2_slider = ttk.Scale(input_frame, from_=200, to=800, orient="horizontal")
co2_slider.set(400)
co2_slider.grid(row=1, column=1, padx=5, pady=5)

# Moisture Slider
ttk.Label(input_frame, text="💧 Moisture (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
moisture_slider = ttk.Scale(input_frame, from_=0, to=100, orient="horizontal")
moisture_slider.set(40)
moisture_slider.grid(row=2, column=1, padx=5, pady=5)

# Nitrogen Slider
ttk.Label(input_frame, text="🔬 Nitrogen (mg/kg):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
nitrogen_slider = ttk.Scale(input_frame, from_=0, to=50, orient="horizontal")
nitrogen_slider.set(10)
nitrogen_slider.grid(row=3, column=1, padx=5, pady=5)

# Phosphorus Slider
ttk.Label(input_frame, text="🧪 Phosphorus (mg/kg):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
phosphorus_slider = ttk.Scale(input_frame, from_=0, to=50, orient="horizontal")
phosphorus_slider.set(5)
phosphorus_slider.grid(row=4, column=1, padx=5, pady=5)

# Potassium Slider
ttk.Label(input_frame, text="🟤 Potassium (mg/kg):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
potassium_slider = ttk.Scale(input_frame, from_=0, to=50, orient="horizontal")
potassium_slider.set(5)
potassium_slider.grid(row=5, column=1, padx=5, pady=5)

# Fragmentation Dropdown
ttk.Label(input_frame, text="🌳 Fragmentation Level:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
fragmentation_var = tk.StringVar(value="Low")
fragmentation_menu = ttk.Combobox(input_frame, textvariable=fragmentation_var, values=["Low", "High"])
fragmentation_menu.grid(row=6, column=1, padx=5, pady=5)

# Remediation Dropdown
ttk.Label(input_frame, text="🛠 Remediation Strategy:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
remediation_var = tk.StringVar(value="Biochar")
remediation_menu = ttk.Combobox(input_frame, textvariable=remediation_var, values=["Biochar", "Inoculation", "Compost", "Humic Substances"])
remediation_menu.grid(row=7, column=1, padx=5, pady=5)

# Simulate Button
ttk.Button(root, text="🌍 Simulate Health", command=simulate_health, style="TButton").pack(pady=10)

# Health Progress Bar
health_bar = ttk.Progressbar(root, length=200, mode="determinate", style="TProgressbar")
health_bar.pack(pady=10)

# Result Label
baseline_health_label = ttk.Label(root, text="🌱 Baseline Health: ")
baseline_health_label.pack()
outcome_message_label = ttk.Label(root, text="")
outcome_message_label.pack()

# Graph Setup
fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
