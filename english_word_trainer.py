from tkinter import *
from tkinter import ttk
import settings as st




# Create main window
root = Tk()
root.geometry(f"+{st.INDENT_LEFT}+{st.INDENT_TOP}")
root.title('English word trainer')
root.resizable(st.RESIZE_W, st.RESIZE_H)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# Create main content frame
main_frame = ttk.Frame(root, padding=st.MCF_PADDING)
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))






# Create the different widgets
table_words_labl = ttk.Label(main_frame, text='Table of learned words ')
table_words = Listbox(main_frame, height=29)
eng_entry_labl = ttk.Label(main_frame, text='English word')
eng_word = StringVar()
eng_entry = ttk.Entry(main_frame, textvariable=eng_word)
translate_entry_labl = ttk.Label(main_frame, text='Translate on Russian')
translate_word = StringVar()
translate_entry = ttk.Entry(main_frame, textvariable=translate_word)
btn1 = ttk.Button(main_frame, text='Save', default='active')
btn2 = ttk.Button(main_frame, text='Delete', default='active')




# Grid all the widgets
table_words_labl.grid(column=0, row=0, sticky=(N, W))
table_words.grid(column=0, row=1, pady=(5, 10), rowspan=60, sticky=(N, W, E, S))
eng_entry_labl.grid(column=1, row=0, padx=(20, 0), columnspan=2, sticky=(N, W))
eng_entry.grid(column=1, row=1, padx=(20, 0), pady=(5, 10), columnspan=2, sticky=(N, W, E))
translate_entry_labl.grid(column=1, row=2, padx=(20, 0), pady=0, columnspan=2, sticky=(N, W))
translate_entry.grid(column=1, row=3, padx=(20, 0), pady=(5, 10), columnspan=2, sticky=(N, W, E))
btn1.grid(column=1, row=4, padx=(20, 0), pady=(10, 0), sticky=(N, W))
btn2.grid(column=2, row=4, padx=(20, 0), pady=(10, 0), sticky=(N, W))

root.mainloop()