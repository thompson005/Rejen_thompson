import tkinter as tk
from tkinter import messagebox
import re

def check_password_strength(password):
    # Define your password strength rules here
    length_check = len(password) >= 8
    uppercase_check = any(c.isupper() for c in password)
    lowercase_check = any(c.islower() for c in password)
    digit_check = any(c.isdigit() for c in password)
    special_char_check = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None

    return length_check and uppercase_check and lowercase_check and digit_check and special_char_check

def check_password():
    password = password_entry.get()
    if check_password_strength(password):
        messagebox.showinfo("Password Checker", "Password is strong and secure!")
    else:
        messagebox.showwarning("Password Checker", "Password does not meet the strength criteria.")

# Create the main application window
app = tk.Tk()
app.title("Password Checker")

# Create and place widgets in the window
tk.Label(app, text="Enter Password:").pack(pady=10)
password_entry = tk.Entry(app, show="*")
password_entry.pack(pady=10)

check_button = tk.Button(app, text="Check Password", command=check_password)
check_button.pack(pady=20)

# Start the application loop
app.mainloop()

