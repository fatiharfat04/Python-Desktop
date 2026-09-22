from tkinter.ttk import Combobox
from tkinter import *
from tkinter.ttk import *

window = Tk()
window.title("YouTube")
window.geometry("400x300")

combo = Combobox(window)
combo['values'] = ("Java", "Python", "C++", "C#", "JavaScript", "HTML", "CSS")
combo.current(0)
combo.grid(row=0, column=0, padx=10, pady=10)

label = Label(window, text="Choose a programming language:")
label.grid(row=1, column=0, padx=10, pady=10)

def on_combobox_select():
    paragraph.config(text=f"I want to learn {combo.get()}")

learn_btn = Button(window, text="Learn", command=on_combobox_select)
learn_btn.grid(row=0, column=1, padx=10, pady=10)

paragraph = Label(window, font=("ariel", 10))
paragraph.config(text="the choosen one will appear here!")
paragraph.grid(row=2, column=0, padx=10, pady=10)

window.mainloop()