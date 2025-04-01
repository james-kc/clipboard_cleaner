import re
import time
import pyperclip
import threading
import tkinter as tk

class ClipboardCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Cleaner")
        self.root.geometry("300x150")
        
        self.running = False
        self.last_text = pyperclip.paste()  # Start with existing clipboard content

        # UI Elements
        self.label = tk.Label(root, text="Clipboard Cleaner", font=("Arial", 12))
        self.label.pack(pady=10)

        self.toggle_button = tk.Button(root, text="Start", command=self.toggle_monitoring, width=10)
        self.toggle_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app, width=10)
        self.exit_button.pack(pady=5)

    def clean_text(self, text):
        """Removes unnecessary newlines while preserving paragraph breaks."""
        # Remove carriage returns and form feeds
        text = text.replace("\r", " ").replace("\f", " ")

        # Fix hyphenated words broken by line breaks (e.g., "solar-\nflare" -> "solar-flare")
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

        # Preserve paragraphs by temporarily marking them
        text = text.replace("\n\n", "¶¶")  # Mark paragraph breaks

        # Replace single newlines with spaces (while keeping paragraph markers)
        text = re.sub(r"(?<!¶)\n(?!¶)", " ", text)

        # Restore paragraph breaks
        text = text.replace("¶¶", "\n\n")

        return text.strip()

    def monitor_clipboard(self):
        """Continuously monitors clipboard for new text and auto-cleans it."""
        while self.running:
            clipboard_text = pyperclip.paste()
            if clipboard_text and clipboard_text != self.last_text:  # Only process new clipboard content
                cleaned_text = self.clean_text(clipboard_text)
                if cleaned_text != clipboard_text:  # Only modify if needed
                    pyperclip.copy(cleaned_text)
                    print("Clipboard cleaned:\n", cleaned_text, "\n")
                self.last_text = cleaned_text  # Update last_text to prevent duplicate processing
            time.sleep(0.2)  # Check clipboard every second

    def toggle_monitoring(self):
        """Starts or stops clipboard monitoring."""
        if self.running:
            self.running = False
            self.toggle_button.config(text="Start")
        else:
            self.running = True
            self.toggle_button.config(text="Stop")
            threading.Thread(target=self.monitor_clipboard, daemon=True).start()

    def exit_app(self):
        """Stops monitoring and closes the app."""
        self.running = False
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardCleaner(root)
    root.mainloop()
