import tkinter as tk
import os

file_path = 'kala.text'
last_modified = None

def display_content():
    global last_modified
    try:
        file_stats = os.stat(file_path)
        current_modified = file_stats.st_mtime

        if last_modified is None or current_modified > last_modified:
            last_modified = current_modified
            with open(file_path, 'r',encoding='utf-8') as file:
                content = file.read()
                index = 0
                text.delete('1.0', tk.END)
                root.after(4, display_character, content, index)
    except FileNotFoundError:
        text.delete('1.0', tk.END)
        text.insert(tk.END, "File not found.")

    root.after(1000, display_content)

def display_character(content, index):
    if index < len(content):
        text.insert(tk.END, content[index])
        text.tag_add("green_text", "1.0", "end")
        text.tag_config("green_text", foreground="white", background="black")
        index += 1
        root.after(50, display_character, content, index)

root = tk.Tk()
root.configure(bg='black')

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create a text widget to display the content
text = tk.Text(root, font=('Arial', 25), fg='white', bg='black')
text.pack()

# Set the size and position of the window to full screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

display_content()

root.mainloop()

