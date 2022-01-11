import tkinter as tk
from tkinter import ttk
import settings as st


root = tk.Tk()
root.geometry(f"{st.MAIN_WINDOW_WIDTH}x{st.MAIN_WINDOW_HEIGHT}+{st.INDENT_LEFT}+{st.INDENT_TOP}")
root.title('English word trainer')
root.resizable(st.RESIZE_W, st.RESIZE_H)

root.mainloop()