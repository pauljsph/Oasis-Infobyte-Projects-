# Oasis Infobyte Python Projects

This repository contains a collection of Python GUI applications developed as part of the Oasis Infobyte internship program. Each application features a modern, user-friendly interface built with Tkinter.

## 📋 Projects Overview

### 1. BMI Calculator
A modern Body Mass Index (BMI) calculator with data tracking and visualization capabilities.

**Features:**
- Calculate BMI based on weight and height input
- Visual BMI gauge with color-coded categories
- Historical data tracking with JSON storage
- Interactive graphs showing BMI trends over time
- Modern dark-themed UI with GitHub-inspired design
- User-specific data management
- BMI classification (Underweight, Normal, Overweight, Obese)

**Technologies:**
- Tkinter for GUI
- Matplotlib for data visualization
- JSON for data persistence
- NumPy for numerical operations

### 2. Weather Application
A clean and simple weather application that displays current weather information.

**Features:**
- City-based weather search
- Demo mode for testing without API key
- Modern, minimalist UI design
- Display of temperature, weather conditions, and additional details
- Placeholder text and user-friendly input handling

**Technologies:**
- Tkinter for GUI
- Requests for API calls (optional)
- PIL/Pillow for image handling
- Threading for asynchronous operations

**Note:** The application includes both a full-featured version (requires OpenWeatherMap API key) and a demo version for testing without an API key.

### 3. Random Password Generator
*Note: This file appears to be misnamed and contains BMI Calculator code. It may need to be updated or replaced with actual password generator functionality.*

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Install Required Dependencies

```bash
pip install tkinter matplotlib numpy pillow requests
```

**Detailed dependency list:**
- `tkinter` - GUI framework (usually comes with Python)
- `matplotlib` - For data visualization and graphs
- `numpy` - For numerical operations
- `pillow` (PIL) - For image handling
- `requests` - For HTTP requests (Weather app)

## 💻 Usage

### Running the BMI Calculator

```bash
python "BMI Calculator.py"
```

1. Enter your name in the "Name" field
2. Enter your weight in kilograms
3. Enter your height in meters
4. Click "Calculate BMI" to see your results
5. View historical data by clicking "Show My Graph"

### Running the Weather Application

```bash
python "Weather app.py"
```

**For Demo Mode (No API Key Required):**
1. Enter any city name
2. Press Enter or click Search
3. View demo weather data

**For Full Functionality:**
1. Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Open `Weather app.py` and replace `"your_api_key_here"` with your actual API key
3. Change the instantiation from `SimpleWeatherApp()` to `ModernWeatherApp()` at the bottom of the file
4. Run the application and search for real weather data

## 📁 Data Storage

### BMI Calculator
- Data is stored in `bmi_data.json` in the same directory as the script
- Each user's BMI history is tracked separately
- Data includes: date, weight, height, and calculated BMI

## 🎨 Design Features

All applications feature:
- Modern, clean user interfaces
- Responsive layouts
- Color-coded feedback
- Intuitive user experience
- Error handling and validation

### BMI Calculator Design
- Dark theme with GitHub-inspired color palette
- Smooth animations and hover effects
- Visual BMI gauge with category indicators
- Card-based layout for better organization

### Weather App Design
- Light, minimalist theme
- Clean typography with SF Pro Display font
- Rounded corners and subtle shadows
- Responsive search functionality

## 🔧 Customization

### Changing Colors (BMI Calculator)
Colors are defined in the `setup_styles()` method. You can customize:
- Background colors
- Accent colors
- Text colors
- Category-specific colors

### Adding API Key (Weather App)
Edit the `fetch_weather_data()` method in the `ModernWeatherApp` class:
```python
api_key = "your_api_key_here"  # Replace with your actual API key
```

## 📝 Project Structure

```
Oasis-Infobyte-Projects-/
├── BMI Calculator.py           # BMI calculation with data tracking
├── Weather app.py              # Weather information application
├── Random Password Generator.py # (Currently contains BMI Calculator code)
├── bmi_data.json              # BMI data storage (auto-generated)
└── README.md                   # This file
```

## ⚠️ Known Issues

1. "Random Password Generator.py" appears to contain BMI Calculator code instead of password generation functionality
2. Weather app requires an API key for full functionality (demo mode available)

## 🤝 Contributing

This is an internship project repository. If you find bugs or have suggestions:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of the Oasis Infobyte internship program.

## 🙏 Acknowledgments

- Oasis Infobyte for the internship opportunity
- OpenWeatherMap for weather data API
- The Python community for excellent libraries and tools

## 📞 Contact

For questions or feedback about these projects, please reach out through the repository's issue tracker.

---

**Happy Coding! 🚀**
