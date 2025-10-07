import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
import threading
from datetime import datetime

class ModernWeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.root.title("Weather")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8fafc")
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (200)
        y = (self.root.winfo_screenheight() // 2) - (300)
        self.root.geometry(f"400x600+{x}+{y}")
        
    def create_widgets(self):
        # Search section
        search_frame = tk.Frame(self.root, bg="#f8fafc")
        search_frame.pack(fill="x", pady=30, padx=30)
        
        # Search input with modern styling
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("SF Pro Display", 16),
            bg="white",
            fg="#1f2937",
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightcolor="#3b82f6",
            highlightbackground="#e5e7eb"
        )
        self.search_entry.pack(fill="x", ipady=12, pady=(0, 15))
        self.search_entry.bind("<Return>", lambda e: self.get_weather())
        
        # Add placeholder text
        self.search_entry.insert(0, "Enter city name...")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)
        self.search_entry.config(fg="#9ca3af")
        
        # Search button
        self.search_btn = tk.Button(
            search_frame,
            text="Get Weather",
            font=("SF Pro Display", 14, "bold"),
            bg="#3b82f6",
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.get_weather
        )
        self.search_btn.pack()
        
        # Weather display container
        self.weather_container = tk.Frame(self.root, bg="#f8fafc")
        self.weather_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Initial message
        self.show_initial_message()
        
    def clear_placeholder(self, event):
        if self.search_entry.get() == "Enter city name...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#1f2937")
            
    def add_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Enter city name...")
            self.search_entry.config(fg="#9ca3af")
            
    def show_initial_message(self):
        initial_label = tk.Label(
            self.weather_container,
            text="☁️",
            font=("SF Pro Display", 60),
            bg="#f8fafc",
            fg="#6b7280"
        )
        initial_label.pack(expand=True)
        
        msg_label = tk.Label(
            self.weather_container,
            text="Search for a city to see weather",
            font=("SF Pro Display", 16),
            bg="#f8fafc",
            fg="#6b7280"
        )
        msg_label.pack()
        
    def clear_weather_display(self):
        for widget in self.weather_container.winfo_children():
            widget.destroy()
            
    def show_loading(self):
        self.clear_weather_display()
        loading_label = tk.Label(
            self.weather_container,
            text="🔄",
            font=("SF Pro Display", 40),
            bg="#f8fafc",
            fg="#3b82f6"
        )
        loading_label.pack(expand=True)
        
        msg_label = tk.Label(
            self.weather_container,
            text="Loading...",
            font=("SF Pro Display", 14),
            bg="#f8fafc",
            fg="#6b7280"
        )
        msg_label.pack()
        
    def get_weather(self):
        city = self.search_var.get().strip()
        if not city or city == "Enter city name...":
            messagebox.showerror("Error", "Please enter a city name")
            return
            
        self.search_btn.config(state="disabled", text="Loading...")
        self.show_loading()
        
        # Fetch weather in background thread
        threading.Thread(target=self.fetch_weather_data, args=(city,), daemon=True).start()
        
    def fetch_weather_data(self, city):
        try:
            # Using a simple weather API (you can replace with OpenWeatherMap)
            api_key = "your_api_key_here"  # Replace with your API key
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.root.after(0, lambda: self.display_weather(data))
            else:
                error_msg = response.json().get("message", "City not found")
                self.root.after(0, lambda: self.show_error(error_msg))
                
        except requests.exceptions.RequestException:
            self.root.after(0, lambda: self.show_error("Network error"))
        except Exception as e:
            self.root.after(0, lambda: self.show_error("Something went wrong"))
        finally:
            self.root.after(0, self.reset_search_button)
            
    def display_weather(self, data):
        self.clear_weather_display()
        
        # Main weather card
        card = tk.Frame(self.weather_container, bg="white", relief="flat")
        card.pack(fill="both", expand=True, pady=10)
        
        # Add subtle shadow effect with border
        card.config(highlightbackground="#e5e7eb", highlightthickness=1)
        
        # City name
        city_label = tk.Label(
            card,
            text=f"{data['name']}, {data['sys']['country']}",
            font=("SF Pro Display", 24, "bold"),
            bg="white",
            fg="#1f2937"
        )
        city_label.pack(pady=(30, 10))
        
        # Temperature
        temp = int(data['main']['temp'])
        temp_label = tk.Label(
            card,
            text=f"{temp}°C",
            font=("SF Pro Display", 72, "bold"),
            bg="white",
            fg="#1f2937"
        )
        temp_label.pack()
        
        # Weather description
        desc = data['weather'][0]['description'].title()
        desc_label = tk.Label(
            card,
            text=desc,
            font=("SF Pro Display", 18),
            bg="white",
            fg="#6b7280"
        )
        desc_label.pack(pady=(0, 20))
        
        # Weather details in a clean grid
        details_frame = tk.Frame(card, bg="white")
        details_frame.pack(pady=20, padx=30, fill="x")
        
        # Feels like
        feels_like = int(data['main']['feels_like'])
        self.create_detail_row(details_frame, "Feels like", f"{feels_like}°C", 0)
        
        # Humidity
        humidity = data['main']['humidity']
        self.create_detail_row(details_frame, "Humidity", f"{humidity}%", 1)
        
        # Wind
        wind_speed = data['wind']['speed']
        self.create_detail_row(details_frame, "Wind", f"{wind_speed} m/s", 2)
        
        # Pressure
        pressure = data['main']['pressure']
        self.create_detail_row(details_frame, "Pressure", f"{pressure} hPa", 3)
        
    def create_detail_row(self, parent, label, value, row):
        # Label
        label_widget = tk.Label(
            parent,
            text=label,
            font=("SF Pro Display", 14),
            bg="white",
            fg="#6b7280",
            anchor="w"
        )
        label_widget.grid(row=row, column=0, sticky="w", pady=8)
        
        # Value
        value_widget = tk.Label(
            parent,
            text=value,
            font=("SF Pro Display", 14, "bold"),
            bg="white",
            fg="#1f2937",
            anchor="e"
        )
        value_widget.grid(row=row, column=1, sticky="e", pady=8)
        
        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
    def show_error(self, message):
        self.clear_weather_display()
        
        error_label = tk.Label(
            self.weather_container,
            text="❌",
            font=("SF Pro Display", 40),
            bg="#f8fafc",
            fg="#ef4444"
        )
        error_label.pack(expand=True)
        
        msg_label = tk.Label(
            self.weather_container,
            text=message,
            font=("SF Pro Display", 16),
            bg="#f8fafc",
            fg="#6b7280"
        )
        msg_label.pack()
        
    def reset_search_button(self):
        self.search_btn.config(state="normal", text="Get Weather")
        
    def run(self):
        self.root.mainloop()

# Simple version without API key requirement for demo
class SimpleWeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.root.title("Weather")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8fafc")
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (200)
        y = (self.root.winfo_screenheight() // 2) - (300)
        self.root.geometry(f"400x600+{x}+{y}")
        
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="Weather App",
            font=("SF Pro Display", 28, "bold"),
            bg="#f8fafc",
            fg="#1f2937"
        )
        title.pack(pady=(40, 30))
        
        # Search section
        search_frame = tk.Frame(self.root, bg="#f8fafc")
        search_frame.pack(fill="x", pady=20, padx=40)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("SF Pro Display", 16),
            bg="white",
            fg="#1f2937",
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightcolor="#3b82f6",
            highlightbackground="#e5e7eb"
        )
        self.search_entry.pack(fill="x", ipady=15, pady=(0, 20))
        self.search_entry.bind("<Return>", lambda e: self.show_demo_weather())
        
        # Placeholder
        self.search_entry.insert(0, "Enter city name...")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)
        self.search_entry.config(fg="#9ca3af")
        
        # Search button
        search_btn = tk.Button(
            search_frame,
            text="Get Weather",
            font=("SF Pro Display", 14, "bold"),
            bg="#3b82f6",
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.show_demo_weather
        )
        search_btn.pack()
        
        # Weather display
        self.weather_frame = tk.Frame(self.root, bg="white", relief="flat")
        self.weather_frame.pack(fill="both", expand=True, padx=40, pady=30)
        self.weather_frame.config(highlightbackground="#e5e7eb", highlightthickness=1)
        
        # Demo message
        demo_msg = tk.Label(
            self.weather_frame,
            text="☁️\n\nEnter any city name to see\na demo weather display",
            font=("SF Pro Display", 16),
            bg="white",
            fg="#6b7280",
            justify="center"
        )
        demo_msg.pack(expand=True)
        
    def clear_placeholder(self, event):
        if self.search_entry.get() == "Enter city name...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#1f2937")
            
    def add_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Enter city name...")
            self.search_entry.config(fg="#9ca3af")
            
    def show_demo_weather(self):
        city = self.search_var.get().strip()
        if not city or city == "Enter city name...":
            messagebox.showerror("Error", "Please enter a city name")
            return
            
        # Clear existing content
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
            
        # City name
        city_label = tk.Label(
            self.weather_frame,
            text=city.title(),
            font=("SF Pro Display", 24, "bold"),
            bg="white",
            fg="#1f2937"
        )
        city_label.pack(pady=(30, 10))
        
        # Temperature (demo)
        temp_label = tk.Label(
            self.weather_frame,
            text="22°C",
            font=("SF Pro Display", 64, "bold"),
            bg="white",
            fg="#1f2937"
        )
        temp_label.pack()
        
        # Description
        desc_label = tk.Label(
            self.weather_frame,
            text="Partly Cloudy",
            font=("SF Pro Display", 18),
            bg="white",
            fg="#6b7280"
        )
        desc_label.pack(pady=(0, 20))
        
        # Details
        details = [
            ("Feels like", "25°C"),
            ("Humidity", "65%"),
            ("Wind", "3.2 m/s"),
            ("Pressure", "1013 hPa")
        ]
        
        details_frame = tk.Frame(self.weather_frame, bg="white")
        details_frame.pack(pady=20, padx=30, fill="x")
        
        for i, (label, value) in enumerate(details):
            label_widget = tk.Label(
                details_frame,
                text=label,
                font=("SF Pro Display", 14),
                bg="white",
                fg="#6b7280",
                anchor="w"
            )
            label_widget.grid(row=i, column=0, sticky="w", pady=8)
            
            value_widget = tk.Label(
                details_frame,
                text=value,
                font=("SF Pro Display", 14, "bold"),
                bg="white",
                fg="#1f2937",
                anchor="e"
            )
            value_widget.grid(row=i, column=1, sticky="e", pady=8)
            
        details_frame.grid_columnconfigure(0, weight=1)
        details_frame.grid_columnconfigure(1, weight=1)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Use SimpleWeatherApp for demo without API key
    # Use ModernWeatherApp if you have an API key
    app = SimpleWeatherApp()
    app.run()