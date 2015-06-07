# -*- coding: utf-8 -*-
from tkFileDialog import askopenfilename
from tkColorChooser  import askcolor

def show_openfiledialog(directory,title="Open File",filetypes=[('jpg','*.jpg'),('gif','*.gif'),('png','*.png'),('jpeg','*.jpeg')]):
    return askopenfilename(initialdir=directory,filetypes=filetypes,title=title)
def show_colordialog(color='red'):
    return askcolor(color)