# -*- coding: utf-8 -*-
from Tkinter import *
from tkMessageBox import askyesno

from gui import experiment, recognition
import ttk
        
def confirm_close(root):
    def handler():
        if askyesno('询问','确定要退出吗'):
            root.quit()
        else:
            return None
    return handler

def mainloop():
    root = Tk()
    root.title("基于图片的火灾检测")
    root.geometry("1000x630+100+30")
    root.state('zoomed')
    root.protocol('WM_DELETE_WINDOW', confirm_close(root))
    nt=ttk.Notebook(root)
    nt.pack(side=TOP,expand=YES,fill=BOTH)
    f1=Frame(nt)
    f2=Frame(nt)
    nt.add(f1,text='训练和识别')
    nt.add(f2,text='预处理试验')
    recognition.Recognition().make_ui(f1)
    experiment.Experiment().make_ui(f2)
    
    root.mainloop()