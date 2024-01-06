import tkinter as tk
from tkinter import ttk
import base64
import urllib.parse
import html
import codecs

def detect_encoding(message):
    # Check for Base64 encoding
    try:
        base64.b64decode(message)
        return 'Base64'
    except Exception:
        pass

    # Check for ROTn encoding
    for shift in range(1, 26):
        decoded_message = decode_caesar_cipher(message, shift)
        if decoded_message.isalpha():
            return f'ROT{shift}'

    # Check for HTML encoding
    if "&" in message and ";" in message:
        try:
            decoded_message = html.unescape(message)
            if decoded_message.isprintable():
                return 'HTML Encoding'
        except Exception:
            pass

    # Check for URL encoding
    try:
        decoded_message = urllib.parse.unquote(message)
        if decoded_message.isprintable():
            return 'URL Encoding'
    except Exception:
        pass

    # Check for Unicode encoding
    try:
        decoded_message = codecs.decode(message, 'unicode_escape')
        if decoded_message.isprintable():
            return 'Unicode Encoding'
    except Exception:
        pass

    # Check for Hex encoding
    try:
        decoded_message = bytes.fromhex(message).decode('utf-8')
        if decoded_message.isprintable():
            return 'Hex Encoding'
    except Exception:
        pass

    # Check for ASCII encoding
    try:
        decoded_message = ''.join(chr(int(chunk, 16)) for chunk in message.split())
        if decoded_message.isprintable():
            return 'ASCII Encoding'
    except Exception:
        pass

    # Add more encoding checks as needed

    # If no encoding is detected, return None
    return None

def decode_caesar_cipher(message, shift):
    decoded_message = ""
    
    for char in message:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            is_upper = char.isupper()
            
            # Shift the character position by the specified shift value
            char_code = ord(char.lower())
            char_code = (char_code - ord('a') - shift) % 26 + ord('a')
            
            # Convert the character back to uppercase if it was originally uppercase
            if is_upper:
                decoded_message += chr(char_code).upper()
            else:
                decoded_message += chr(char_code)
        else:
            # Keep non-alphabetic characters unchanged
            decoded_message += char
    
    return decoded_message

def auto_decode(message):
    encoding = detect_encoding(message)
    
    if encoding:
        decoded_message = None

        # Perform decoding based on detected encoding
        if encoding.startswith('ROT'):
            shift = int(encoding[3:])
            decoded_message = decode_caesar_cipher(message, shift)
        elif encoding == 'Base64':
            decoded_message = base64.b64decode(message).decode('utf-8')
        elif encoding == 'HTML Encoding':
            decoded_message = html.unescape(message)
        elif encoding == 'URL Encoding':
            decoded_message = urllib.parse.unquote(message)
        elif encoding == 'Unicode Encoding':
            decoded_message = codecs.decode(message, 'unicode_escape')
        elif encoding == 'Hex Encoding':
            decoded_message = bytes.fromhex(message).decode('utf-8')
        elif encoding == 'ASCII Encoding':
            decoded_message = ''.join(chr(int(chunk, 16)) for chunk in message.split())
        
        # Recursively continue decoding until a printable message is obtained
        if decoded_message and not decoded_message.isprintable():
            return auto_decode(decoded_message)
        
        return decoded_message
    
    # If no encoding is detected, return the original message
    return message

class MessageDecoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message Decoder")
        self.root.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        # Input Label and Entry
        input_label = ttk.Label(self.root, text="Enter Encoded Message:")
        input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.input_entry = ttk.Entry(self.root, width=40)
        self.input_entry.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="w")

        # Output Label and Entry
        output_label = ttk.Label(self.root, text="Decoded Message:")
        output_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.output_entry = ttk.Entry(self.root, width=40, state="readonly")
        self.output_entry.grid(row=3, column=0, padx=10, pady=5, columnspan=2, sticky="w")

        # Decode Button
        decode_button = ttk.Button(self.root, text="Decode", command=self.decode_message)
        decode_button.grid(row=4, column=0, pady=10, sticky="w")

    def decode_message(self):
        encoded_message = self.input_entry.get()
        decoded_message = auto_decode(encoded_message)
        self.output_entry.config(state="normal")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, decoded_message)
        self.output_entry.config(state="readonly")

if __name__ == "__main__":
    root = tk.Tk()
    app = MessageDecoderApp(root)
    root.mainloop()
