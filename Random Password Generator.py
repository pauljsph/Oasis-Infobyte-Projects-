"""
Advanced Password Generator with GUI
A comprehensive password generator with Tkinter GUI featuring:
- Customizable password complexity
- Security rules enforcement
- Clipboard integration
- Character exclusion options
- Password strength indicator
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import re


class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=16)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)
        self.exclude_similar_var = tk.BooleanVar(value=False)
        self.exclude_custom_var = tk.StringVar()
        self.min_uppercase_var = tk.IntVar(value=1)
        self.min_lowercase_var = tk.IntVar(value=1)
        self.min_digits_var = tk.IntVar(value=1)
        self.min_symbols_var = tk.IntVar(value=1)
        self.enforce_rules_var = tk.BooleanVar(value=True)
        
        # Character sets
        self.ambiguous_chars = "il1Lo0O"
        self.similar_chars = "il1Lo0O|`"
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Password Generator", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Password Length Section
        length_frame = ttk.LabelFrame(main_frame, text="Password Length", padding="10")
        length_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(length_frame, text="Length:").grid(row=0, column=0, sticky=tk.W)
        length_spinbox = ttk.Spinbox(length_frame, from_=4, to=128, 
                                     textvariable=self.length_var, width=10)
        length_spinbox.grid(row=0, column=1, padx=(10, 20))
        
        length_scale = ttk.Scale(length_frame, from_=4, to=128, 
                                variable=self.length_var, orient=tk.HORIZONTAL, length=300)
        length_scale.grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        # Character Types Section
        char_frame = ttk.LabelFrame(main_frame, text="Character Types", padding="10")
        char_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(char_frame, text="Uppercase Letters (A-Z)", 
                       variable=self.uppercase_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(char_frame, text="Lowercase Letters (a-z)", 
                       variable=self.lowercase_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(char_frame, text="Digits (0-9)", 
                       variable=self.digits_var).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(char_frame, text="Symbols (!@#$%^&*)", 
                       variable=self.symbols_var).grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # Security Rules Section
        rules_frame = ttk.LabelFrame(main_frame, text="Security Rules", padding="10")
        rules_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(rules_frame, text="Enforce minimum character requirements", 
                       variable=self.enforce_rules_var).grid(row=0, column=0, columnspan=2, 
                                                             sticky=tk.W, pady=(0, 10))
        
        # Minimum requirements
        ttk.Label(rules_frame, text="Min Uppercase:").grid(row=1, column=0, sticky=tk.W)
        ttk.Spinbox(rules_frame, from_=0, to=20, textvariable=self.min_uppercase_var, 
                   width=10).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(rules_frame, text="Min Lowercase:").grid(row=2, column=0, sticky=tk.W)
        ttk.Spinbox(rules_frame, from_=0, to=20, textvariable=self.min_lowercase_var, 
                   width=10).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(rules_frame, text="Min Digits:").grid(row=3, column=0, sticky=tk.W)
        ttk.Spinbox(rules_frame, from_=0, to=20, textvariable=self.min_digits_var, 
                   width=10).grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(rules_frame, text="Min Symbols:").grid(row=4, column=0, sticky=tk.W)
        ttk.Spinbox(rules_frame, from_=0, to=20, textvariable=self.min_symbols_var, 
                   width=10).grid(row=4, column=1, sticky=tk.W, padx=(10, 0))
        
        # Exclusion Options Section
        exclusion_frame = ttk.LabelFrame(main_frame, text="Exclusion Options", padding="10")
        exclusion_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(exclusion_frame, text="Exclude ambiguous characters (il1Lo0O)", 
                       variable=self.exclude_ambiguous_var).grid(row=0, column=0, 
                                                                 sticky=tk.W, pady=2)
        ttk.Checkbutton(exclusion_frame, text="Exclude similar characters (il1Lo0O|`)", 
                       variable=self.exclude_similar_var).grid(row=1, column=0, 
                                                               sticky=tk.W, pady=2)
        
        ttk.Label(exclusion_frame, text="Exclude custom characters:").grid(row=2, column=0, 
                                                                           sticky=tk.W, pady=(10, 2))
        ttk.Entry(exclusion_frame, textvariable=self.exclude_custom_var, 
                 width=40).grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Generated Password Section
        password_frame = ttk.LabelFrame(main_frame, text="Generated Password", padding="10")
        password_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                   font=('Courier', 12), state='readonly', width=50)
        password_entry.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Strength indicator
        self.strength_label = ttk.Label(password_frame, text="Strength: N/A", 
                                       font=('Arial', 10, 'bold'))
        self.strength_label.grid(row=1, column=0, columnspan=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        generate_btn = ttk.Button(button_frame, text="Generate Password", 
                                 command=self.generate_password, width=20)
        generate_btn.grid(row=0, column=0, padx=5)
        
        copy_btn = ttk.Button(button_frame, text="Copy to Clipboard", 
                             command=self.copy_to_clipboard, width=20)
        copy_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear", 
                              command=self.clear_password, width=20)
        clear_btn.grid(row=0, column=2, padx=5)
        
    def validate_settings(self):
        """Validate user settings before generating password"""
        # Check if at least one character type is selected
        if not any([self.uppercase_var.get(), self.lowercase_var.get(), 
                   self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showerror("Error", "Please select at least one character type!")
            return False
        
        # Check if minimum requirements exceed password length
        if self.enforce_rules_var.get():
            min_total = (self.min_uppercase_var.get() + self.min_lowercase_var.get() + 
                        self.min_digits_var.get() + self.min_symbols_var.get())
            
            if min_total > self.length_var.get():
                messagebox.showerror("Error", 
                    f"Minimum character requirements ({min_total}) exceed password length ({self.length_var.get()})!")
                return False
        
        # Check if password length is valid
        if self.length_var.get() < 4:
            messagebox.showerror("Error", "Password length must be at least 4 characters!")
            return False
        
        return True
    
    def get_character_pool(self):
        """Build the character pool based on user selections"""
        char_pool = ""
        
        if self.uppercase_var.get():
            char_pool += string.ascii_uppercase
        if self.lowercase_var.get():
            char_pool += string.ascii_lowercase
        if self.digits_var.get():
            char_pool += string.digits
        if self.symbols_var.get():
            char_pool += string.punctuation
        
        # Remove excluded characters
        if self.exclude_ambiguous_var.get():
            char_pool = ''.join(c for c in char_pool if c not in self.ambiguous_chars)
        
        if self.exclude_similar_var.get():
            char_pool = ''.join(c for c in char_pool if c not in self.similar_chars)
        
        # Remove custom excluded characters
        custom_exclude = self.exclude_custom_var.get()
        if custom_exclude:
            char_pool = ''.join(c for c in char_pool if c not in custom_exclude)
        
        return char_pool
    
    def generate_password(self):
        """Generate a password based on user settings"""
        if not self.validate_settings():
            return
        
        char_pool = self.get_character_pool()
        
        if not char_pool:
            messagebox.showerror("Error", "No characters available for password generation!")
            return
        
        password = []
        
        # Enforce minimum requirements if enabled
        if self.enforce_rules_var.get():
            # Add minimum uppercase
            if self.uppercase_var.get() and self.min_uppercase_var.get() > 0:
                available_upper = [c for c in string.ascii_uppercase if c in char_pool]
                if available_upper:
                    password.extend(random.choices(available_upper, 
                                                  k=min(self.min_uppercase_var.get(), 
                                                       len(available_upper))))
            
            # Add minimum lowercase
            if self.lowercase_var.get() and self.min_lowercase_var.get() > 0:
                available_lower = [c for c in string.ascii_lowercase if c in char_pool]
                if available_lower:
                    password.extend(random.choices(available_lower, 
                                                  k=min(self.min_lowercase_var.get(), 
                                                       len(available_lower))))
            
            # Add minimum digits
            if self.digits_var.get() and self.min_digits_var.get() > 0:
                available_digits = [c for c in string.digits if c in char_pool]
                if available_digits:
                    password.extend(random.choices(available_digits, 
                                                  k=min(self.min_digits_var.get(), 
                                                       len(available_digits))))
            
            # Add minimum symbols
            if self.symbols_var.get() and self.min_symbols_var.get() > 0:
                available_symbols = [c for c in string.punctuation if c in char_pool]
                if available_symbols:
                    password.extend(random.choices(available_symbols, 
                                                  k=min(self.min_symbols_var.get(), 
                                                       len(available_symbols))))
        
        # Fill remaining length with random characters from pool
        remaining_length = self.length_var.get() - len(password)
        if remaining_length > 0:
            password.extend(random.choices(char_pool, k=remaining_length))
        
        # Shuffle the password to randomize positions
        random.shuffle(password)
        
        # Convert to string
        final_password = ''.join(password[:self.length_var.get()])
        
        # Set the password
        self.password_var.set(final_password)
        
        # Update strength indicator
        self.update_strength_indicator(final_password)
    
    def update_strength_indicator(self, password):
        """Calculate and display password strength"""
        strength_score = 0
        
        # Length scoring
        if len(password) >= 12:
            strength_score += 2
        elif len(password) >= 8:
            strength_score += 1
        
        # Character variety scoring
        if re.search(r'[A-Z]', password):
            strength_score += 1
        if re.search(r'[a-z]', password):
            strength_score += 1
        if re.search(r'\d', password):
            strength_score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            strength_score += 2
        
        # Determine strength level
        if strength_score >= 7:
            strength = "Very Strong"
            color = "green"
        elif strength_score >= 5:
            strength = "Strong"
            color = "blue"
        elif strength_score >= 3:
            strength = "Medium"
            color = "orange"
        else:
            strength = "Weak"
            color = "red"
        
        self.strength_label.config(text=f"Strength: {strength} ({strength_score}/8)", 
                                  foreground=color)
    
    def copy_to_clipboard(self):
        """Copy the generated password to clipboard"""
        password = self.password_var.get()
        
        if not password:
            messagebox.showwarning("Warning", "No password to copy!")
            return
        
        try:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
    
    def clear_password(self):
        """Clear the generated password"""
        self.password_var.set("")
        self.strength_label.config(text="Strength: N/A", foreground="black")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
