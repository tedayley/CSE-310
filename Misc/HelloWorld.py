import tkinter as tk


window = tk.Tk()
window.title("See I work")
window.geometry("300x150")

greeting = tk.Label(window, text="Hello, World!", font=("URW Chancery L", 26))
greeting.pack(expand=True)

window.mainloop()