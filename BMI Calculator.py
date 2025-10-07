import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

DATA_FILE = "bmi_data.json"

class ModernBMICalculator:
    def __init__(self, root):
        self.root = root
        self.setup_styles()  # Setup styles first
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.root.title("Modern BMI Calculator")
        self.root.geometry("520x680")
        self.root.configure(bg=self.colors['bg_primary'])
        self.root.resizable(False, False)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_styles(self):
        self.colors = {
            'bg_primary': '#0D1117',      # Deep dark blue-gray
            'bg_secondary': '#21262D',    # Medium dark gray
            'bg_card': '#161B22',         # Card background - slightly lighter
            'bg_input': '#21262D',        # Input field background
            'border': '#30363D',          # Subtle borders
            'accent': '#58A6FF',          # GitHub-like blue
            'accent_hover': '#1F6FEB',    # Darker blue for hover
            'accent_secondary': '#7C3AED', # Purple accent
            'text_primary': '#F0F6FC',    # High contrast white
            'text_secondary': '#8B949E',  # Muted gray text
            'text_muted': '#6E7681',      # Even more muted
            'success': '#3FB950',         # GitHub green
            'warning': '#D29922',         # Warm amber
            'danger': '#F85149',          # GitHub red
            'underweight': '#79C0FF',     # Light blue
            'normal': '#3FB950',          # Green
            'overweight': '#D29922',      # Amber
            'obese': '#F85149'            # Red
        }
        
    def calculate_bmi(self, weight, height):
        return weight / (height ** 2)

    def classify_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight", self.colors['underweight']
        elif bmi < 25:
            return "Normal Weight", self.colors['normal']
        elif bmi < 30:
            return "Overweight", self.colors['overweight']
        else:
            return "Obese", self.colors['obese']

    def save_bmi(self, user, bmi, weight, height):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if user not in data:
            data[user] = []

        data[user].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": weight,
            "height": height,
            "bmi": bmi
        })

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def create_rounded_button(self, parent, text, command, bg_color, hover_color):
        button_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        
        button = tk.Button(
            button_frame,
            text=text,
            command=command,
            font=("Segoe UI", 12, "bold"),
            bg=bg_color,
            fg=self.colors['text_primary'],
            activebackground=hover_color,
            activeforeground=self.colors['text_primary'],
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            relief="flat"
        )
        button.pack()
        
        return button_frame, button

    def create_input_field(self, parent, label_text, row):
        # Label
        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        label.grid(row=row, column=0, sticky="w", pady=(20, 8), padx=(0, 15))
        
        # Entry field with improved styling
        entry_frame = tk.Frame(parent, bg=self.colors['border'], relief="flat", highlightthickness=1)
        entry_frame.grid(row=row, column=1, sticky="ew", pady=(20, 8))
        parent.grid_columnconfigure(1, weight=1)
        
        entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 13),
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent'],
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        entry.pack(fill="both", expand=True, padx=2, pady=2)
        
        return entry

    def create_bmi_gauge(self, parent, bmi_value=None, category=None):
        canvas = tk.Canvas(
            parent,
            width=300,
            height=180,
            bg=self.colors['bg_primary'],
            highlightthickness=0
        )
        canvas.pack(pady=20)
        
        # Draw gauge background
        center_x, center_y = 150, 140
        radius = 100
        
        # BMI ranges with colors
        ranges = [
            (0, 0.25, self.colors['underweight']),    # Underweight (0-18.5)
            (0.25, 0.5, self.colors['normal']),       # Normal (18.5-25)
            (0.5, 0.75, self.colors['overweight']),   # Overweight (25-30)
            (0.75, 1.0, self.colors['obese'])         # Obese (30+)
        ]
        
        # Draw gauge sections
        start_angle = 180
        for i, (start_ratio, end_ratio, color) in enumerate(ranges):
            extent = (end_ratio - start_ratio) * 180
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle - start_ratio * 180,
                extent=-extent,
                fill=color,
                outline="",
                width=0
            )
        
        # Draw inner circle to create donut effect
        inner_radius = 60
        canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            fill=self.colors['bg_primary'],
            outline=""
        )
        
        # Add BMI value and category text
        if bmi_value is not None:
            canvas.create_text(
                center_x, center_y - 15,
                text=f"{bmi_value:.1f}",
                font=("Segoe UI", 24, "bold"),
                fill=self.colors['text_primary']
            )
            
            if category:
                canvas.create_text(
                    center_x, center_y + 15,
                    text=category,
                    font=("Segoe UI", 12, "bold"),
                    fill=self.colors['text_secondary']
                )
                
                # Draw needle
                if bmi_value <= 18.5:
                    needle_angle = (bmi_value / 18.5) * 45
                elif bmi_value <= 25:
                    needle_angle = 45 + ((bmi_value - 18.5) / 6.5) * 45
                elif bmi_value <= 30:
                    needle_angle = 90 + ((bmi_value - 25) / 5) * 45
                else:
                    needle_angle = 135 + min(((bmi_value - 30) / 10) * 45, 45)
                
                needle_angle = 180 - needle_angle  # Adjust for canvas coordinates
                needle_rad = np.radians(needle_angle)
                needle_length = 70
                
                end_x = center_x + needle_length * np.cos(needle_rad)
                end_y = center_y - needle_length * np.sin(needle_rad)
                
                canvas.create_line(
                    center_x, center_y,
                    end_x, end_y,
                    fill=self.colors['accent'],
                    width=3
                )
                
                # Needle center circle
                canvas.create_oval(
                    center_x - 8, center_y - 8,
                    center_x + 8, center_y + 8,
                    fill=self.colors['accent'],
                    outline=""
                )
        
        # Add labels
        labels = ["18.5", "25", "30", "40+"]
        label_positions = [45, 90, 135, 165]
        for label, angle in zip(labels, label_positions):
            angle_rad = np.radians(180 - angle)
            label_x = center_x + (radius + 20) * np.cos(angle_rad)
            label_y = center_y - (radius + 20) * np.sin(angle_rad)
            canvas.create_text(
                label_x, label_y,
                text=label,
                font=("Segoe UI", 10),
                fill=self.colors['text_secondary']
            )
        
        return canvas

    def show_enhanced_graph(self, user):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            entries = data.get(user, [])
            if not entries:
                messagebox.showinfo("No Data", "No BMI history found for this user.")
                return

            # Create new window for graph
            graph_window = tk.Toplevel(self.root)
            graph_window.title(f"{user}'s BMI History")
            graph_window.geometry("900x600")
            graph_window.configure(bg=self.colors['bg_primary'])

            # Prepare data
            dates = [datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") for e in entries]
            bmis = [e["bmi"] for e in entries]
            weights = [e["weight"] for e in entries]

            # Create matplotlib figure with improved dark theme
            plt.style.use('dark_background')
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=self.colors['bg_primary'])
            
            # BMI chart with better colors
            ax1.plot(dates, bmis, 'o-', color=self.colors['accent'], linewidth=3, markersize=8, alpha=0.9)
            ax1.axhspan(0, 18.5, alpha=0.15, color=self.colors['underweight'], label='Underweight')
            ax1.axhspan(18.5, 25, alpha=0.15, color=self.colors['normal'], label='Normal')
            ax1.axhspan(25, 30, alpha=0.15, color=self.colors['overweight'], label='Overweight')
            ax1.axhspan(30, max(max(bmis) + 2, 35), alpha=0.15, color=self.colors['obese'], label='Obese')
            
            ax1.set_ylabel('BMI', fontsize=12, color='white', fontweight='bold')
            ax1.set_title(f"{user}'s BMI Progress", fontsize=14, color='white', fontweight='bold', pad=20)
            ax1.grid(True, alpha=0.2, color='gray')
            ax1.legend(loc='upper right', framealpha=0.9, facecolor=self.colors['bg_secondary'])
            ax1.set_facecolor(self.colors['bg_primary'])
            
            # Weight chart with better styling
            ax2.plot(dates, weights, 's-', color=self.colors['warning'], linewidth=3, markersize=8, alpha=0.9)
            ax2.set_ylabel('Weight (kg)', fontsize=12, color='white', fontweight='bold')
            ax2.set_xlabel('Date', fontsize=12, color='white', fontweight='bold')
            ax2.grid(True, alpha=0.2, color='gray')
            ax2.set_facecolor(self.colors['bg_primary'])
            
            # Format x-axis
            for ax in [ax1, ax2]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
                ax.tick_params(colors='white')

            plt.tight_layout()
            
            # Embed plot in tkinter window
            canvas = FigureCanvasTkAgg(fig, graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not display graph: {str(e)}")

    def submit(self):
        try:
            user = self.user_entry.get().strip()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if not user:
                raise ValueError("Please enter a username.")
            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers.")
            if height > 3:  # Assume height in meters
                raise ValueError("Height seems too large. Please enter height in meters.")

            bmi = self.calculate_bmi(weight, height)
            category, color = self.classify_bmi(bmi)

            # Update result display
            self.result_frame.destroy()
            self.create_result_display(bmi, category, color)
            
            # Save data
            self.save_bmi(user, bmi, weight, height)
            
            # Show success message
            self.status_label.config(
                text="✓ BMI calculated and saved successfully!",
                fg=self.colors['success']
            )
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            self.status_label.config(
                text="✗ Please check your input values.",
                fg=self.colors['danger']
            )

    def create_result_display(self, bmi, category, color):
        self.result_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        self.result_frame.pack(fill="x", pady=25)
        
        # Create BMI gauge
        self.create_bmi_gauge(self.result_frame, bmi, category)
        
        # BMI details card with better styling
        details_card = tk.Frame(self.result_frame, bg=self.colors['bg_card'], relief="flat", highlightthickness=1, highlightcolor=self.colors['border'])
        details_card.pack(fill="x", padx=25, pady=15)
        
        # Add subtle border effect
        border_frame = tk.Frame(details_card, bg=self.colors['border'], height=1)
        border_frame.pack(fill="x")
        
        content_frame = tk.Frame(details_card, bg=self.colors['bg_card'])
        content_frame.pack(fill="x", padx=25, pady=20)
        
        tk.Label(
            content_frame,
            text=f"Your BMI: {bmi:.1f}",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors['bg_card'],
            fg=color
        ).pack(pady=(0, 8))
        
        tk.Label(
            content_frame,
            text=f"Category: {category}",
            font=("Segoe UI", 15),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack()

    def create_widgets(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Header with gradient-like effect
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        header_frame.pack(fill="x", pady=(0, 35))
        
        # Title with better styling
        title_label = tk.Label(
            header_frame,
            text="BMI Calculator",
            font=("Segoe UI", 32, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Track your Body Mass Index over time",
            font=("Segoe UI", 13),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(8, 0))
        
        # Input card with border
        input_card_outer = tk.Frame(self.main_frame, bg=self.colors['border'], relief="flat")
        input_card_outer.pack(fill="x", pady=(0, 25))
        
        input_card = tk.Frame(input_card_outer, bg=self.colors['bg_card'], relief="flat")
        input_card.pack(fill="both", expand=True, padx=2, pady=2)
        
        input_inner = tk.Frame(input_card, bg=self.colors['bg_card'])
        input_inner.pack(fill="x", padx=35, pady=30)
        
        # Input fields
        self.user_entry = self.create_input_field(input_inner, "Username:", 0)
        self.weight_entry = self.create_input_field(input_inner, "Weight (kg):", 1)
        self.height_entry = self.create_input_field(input_inner, "Height (m):", 2)
        
        # Buttons with improved spacing
        button_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        button_frame.pack(fill="x", pady=25)
        
        # Calculate button
        calc_frame, calc_btn = self.create_rounded_button(
            button_frame, "Calculate BMI", self.submit,
            self.colors['accent'], self.colors['accent_hover']
        )
        calc_frame.pack(side="left", expand=True, padx=(0, 10))
        
        # History button
        history_frame, history_btn = self.create_rounded_button(
            button_frame, "View History", 
            lambda: self.show_enhanced_graph(self.user_entry.get()),
            self.colors['bg_secondary'], self.colors['accent_secondary']
        )
        history_frame.pack(side="right", expand=True, padx=(10, 0))
        
        # Status label with better positioning
        self.status_label = tk.Label(
            self.main_frame,
            text="Enter your details above to calculate BMI",
            font=("Segoe UI", 12),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_muted']
        )
        self.status_label.pack(pady=15)
        
        # Result display placeholder
        self.result_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        self.result_frame.pack(fill="x")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBMICalculator(root)
    root.mainloop()