import tkinter as tk
from tkinter import *
from tkinter import font
from text_theme import *
from file_actions import *
import functools

class LineNumbers(tk.Text):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)

        self.text_widget = text_widget
        self.text_widget.bind('<KeyPress>', self.on_key_press)

        self.insert(1.0, '1')
        self.configure(state='disabled')

    def on_key_press(self, event=None):
        final_index = str(self.text_widget.index(tk.END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(no + 1) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines))

        self.configure(state='normal', width=width)
        self.delete(1.0, tk.END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')


root = Tk()
root.title("Text Editor")
root.geometry("800x500")
# root.minsize(height=400)
root.minsize(height=250, width=350)
# root.maxsize(height=250, width=350)


scrollbar = Scrollbar(root)
scrollbar.pack(fill=Y, side=RIGHT)
text = Text(root, yscrollcommand=scrollbar.set)
l = LineNumbers(root,text,width=1)
l.pack(side=tk.LEFT)
text.pack(fill=BOTH,side=tk.LEFT,expand=1)
scrollbar.config(command=text.yview)



# Menu
menu = Menu()
# Menu For File Options
file_options = Menu()
file_options.add_command(label='New File',command=lambda:new_file(text))
file_options.add_command(label='Open File',command=lambda:open_file(text))
file_options.add_command(label='Open From Google Drive',command=lambda:open_from_drive(text))
file_options.add_command(label='Save to Google Drive',command=lambda:save_to_drive(text))
file_options.add_command(label='Save',command=lambda:save_file(text))
file_options.add_command(label='Save as',command=lambda:save_as(text))
file_options.add_command(label='Exit',command=root.quit)
menu.add_cascade(label='File',menu=file_options) 

# Menu For Themes Options
theme_options = Menu()
theme_options.add_command(label='Dark Theme',command=lambda:theme(0,root,text,"black","white"))
theme_options.add_command(label='Dark-Blue Theme',command=lambda:theme(1,root,text,"blue","white"))
theme_options.add_command(label='Light Theme',command=lambda:theme(2,root,text,"white","black"))
theme_options.add_command(label='Light-Pink Theme',command=lambda:theme(3,root,text,"#FADCD9","black"))
theme_options.add_command(label='Quiet-Light Theme',command=lambda:theme(4,root,text,"#d4cebd","black"))
menu.add_cascade(label='Themes',menu=theme_options) 

# Menu For Font Family Options
font_family_options = Menu()

for i in font.families():
    font_family_options.add_command(label=i,command=lambda x=i:font_family(x,text))
    
menu.add_cascade(label='Font Family',menu=font_family_options) 

# Menu For Font Size Options
font_size_options = Menu()
for i in range(1,80):
    font_size_options.add_command(label=i,command=functools.partial(font_size,i,text))
menu.add_cascade(label='Font Size',menu=font_size_options) 

# Menu For Font Weight Options
font_weight_options = Menu()
weight = ["normal","bold","italic","underline"]
for i in weight:
    font_weight_options.add_command(label=i,command=functools.partial(font_weight,i,text))
menu.add_cascade(label='Font Weight',menu=font_weight_options) 

root.config(menu=menu)

root.mainloop()
