# -*- coding: utf-8 -*-
# encoding: utf-8

from Tkinter import *
from PIL import ImageTk, ImageColor
from gui.common import show_openfiledialog, show_colordialog
import os
import os.path
from tkMessageBox import showinfo, showerror
from fire.imgtool import openimg, median_filter, gray_scale, enhance,\
    gaussian_filter, detect_color, scale_img
from fire.ostu import ostu_capture
from tkFileDialog import askdirectory
import ttk
from threading import Thread


class Recognition(object):
    '''图片识别
    '''

    def __init__(self):
        self.lastup=None
        self.lastdown=None
        self.lastup_file=None
        self.lastdown_file=None
        
    def make_ui(self,uiparent):
        self.which=IntVar(uiparent,value=0)
        self.colortodetect=StringVar(uiparent,'#ffa879')
        self.threshold=IntVar(uiparent,value=40)
        self.result_dir=StringVar(uiparent)
        self.croppixels=StringVar(uiparent,'50')
        self.origin_dir=StringVar(uiparent)
        self.testret=StringVar(uiparent,'识别结果:')
        
        leftframe=Frame(uiparent)
        leftframe.config(width=300,height=500)
        leftframe.pack(side=LEFT,fill=Y,anchor=W,padx=10)
        
        rightframe=Frame(uiparent,bg='green')
        rightframe.pack(side=LEFT,expand=YES,fill=BOTH)
        
        self.up=Canvas(rightframe,bg='gray',relief=SUNKEN,highlightthickness=0)
        hbar=Scrollbar(rightframe,command=self.up.xview,orient='horizontal')
        vbar=Scrollbar(rightframe,command=self.up.yview)
        
        self.up.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set,scrollregion=(0,0,1000,600))

        vbar.pack(side=RIGHT,fill=Y,anchor=E)
        hbar.pack(side=BOTTOM,fill=X,anchor=S)
        self.up.pack(side=TOP,expand=YES,fill=BOTH)
        
        row=Frame(leftframe)
        row.config(height=30)
        row.pack(side=TOP, fill=X)
        
        row=Frame(leftframe)
        row.config(pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='素材目录:',command=self.open_dir).pack(side=LEFT)
        ent=Entry(row,textvariable=self.origin_dir)
        ent.pack(side=LEFT,expand=YES,fill=X,padx=5)

        row=LabelFrame(leftframe,text='批量预处理',padx=20,pady=20)
        row.pack(side=TOP,fill=X)
        
        row1=Frame(row)
        row1.pack(side=TOP,expand=YES,fill=X)
        Label(row1,text='结果目录:').pack(side=LEFT,padx=2)
        ent = Entry(row1,state='readonly',textvariable=self.result_dir)
        ent.pack(side=RIGHT,expand=YES,fill=X,padx=2)
 
        row1=Frame(row)
        row1.pack(side=TOP,expand=YES,fill=X,pady=10)
        Label(row1,text='切块尺寸:').pack(side=LEFT,padx=2)
        
        ent = Entry(row1,textvariable=self.croppixels)
        ent.pack(side=RIGHT,expand=YES,fill=X,padx=2)
        
        row1=Frame(row)
        row1.pack(side=TOP,expand=YES,fill=X,pady=10)
        Label(row1,text='颜色分割阈值:').pack(side=LEFT,padx=2)
        ent = Spinbox(row1,width=10,from_=0,to=255,increment=1,textvariable=self.threshold)
        ent.pack(side=LEFT,padx=2)

        Label(row1,text=' 颜色:').pack(side=LEFT,padx=2)
        ent = Entry(row1,textvariable=self.colortodetect)
        ent.pack(side=RIGHT,fill=X,padx=2)
        
        
        Button(row,text='执行预处理',fg="blue",command=self.begin_preprocess).pack(expand=YES,fill=X,side=TOP,pady=10)
        self.prebar = ttk.Progressbar(row,mode='indeterminate')
        self.prebar.pack(side=TOP,fill=X)
        
        
        
        row=LabelFrame(leftframe,text='训练',padx=20,pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='开始训练',fg="blue",command=self.begin_train).pack(expand=YES,fill=X,side=TOP,pady=10)
        self.trainbar = ttk.Progressbar(row,mode='indeterminate')
        self.trainbar.pack(side=TOP,fill=X)

        row=Frame(leftframe)
        row.config(pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='打开图片',command=self.open_image).pack(expand=YES,fill=X,side=LEFT)
        Button(row,text='识别',fg="blue",command=self.do_recog).pack(expand=YES,fill=X,side=LEFT)
        row=Frame(leftframe)
        row.config(pady=10)
        row.pack(side=TOP, fill=X)
        Label(row,textvariable=self.testret).pack(side=LEFT)

    def begin_preprocess(self):
        dim = self.croppixels.get()
        w=dim
        w=int(w)
        h=w
        if(not w or not h):
            self.alert('请输入正确的切块尺寸')
            return
        if(not self.origin_dir.get()):
            self.alert('请设置素材目录')
            return
        sc = self.colortodetect.get()
        c=None
        try:
            c = ImageColor.getrgb(sc)
        except:
            pass
        
        if not c: 
            self.alert('请设置正确的颜色')
            return
        
        self.prebar.start(10)
        from fire.prepare import batch_preprocess
        Thread(target=batch_preprocess,
               args=(self.origin_dir.get(), self.result_dir.get(),w,h,self.threshold.get(),c,
                     self.on_preprocess)
               ).start()
    def on_preprocess(self):
        self.prebar.stop()
#         self.alert('批量预处理完成,请人工复选教材图片')
         
    def begin_train(self):
        if not self.result_dir.get():
            return self.alert('请先进行预处理准备教材图片')
        c=len(os.listdir(self.result_dir.get()))
        if c<3:
            return self.alert('请先进行预处理准备教材图片')
        dim = self.croppixels.get()
        w=dim
        w=int(w)
        h=w
        if(not w or not h):
            self.alert('请输入正确的切块尺寸')
            return
        
        sc = self.colortodetect.get()
        c=None
        try:
            c = ImageColor.getrgb(sc)
        except:
            pass
        
        if not c: 
            self.alert('请设置正确的颜色')
            return
        self.trainbar.start(10)
        from fire.prepare import train_fire_recognition
        Thread(target=train_fire_recognition,
               args=( self.result_dir.get(),w,h,
                     self.on_train)
               ).start()
               
    def on_train(self):
        self.trainbar.stop()
        
    def do_recog(self):
        if not self.lastup_file:
            return self.alert('请打开一个要识别的图片')
        
        dim = self.croppixels.get()
        w=dim
        w=int(w)
        h=w
        if(not w or not h):
            self.alert('请输入正确的切块尺寸')
            return
        
        sc = self.colortodetect.get()
        c=None
        try:
            c = ImageColor.getrgb(sc)
        except:
            pass
        
        if not c: 
            self.alert('请设置正确的颜色')
            return
        from fire.prepare import test
        result = test(self.lastup_file,w,h,self.threshold.get(),c)
        self.testret.set('识别结果:%s' % result)
    
    def _open_img(self):
        if(not self.lastup_file):
            self.alert('请先打开一个图片')
            return
        if(self.which.get()==0):
            return openimg(self.lastup_file)
        elif not self.lastdown_file:
            self.alert('请先对上图进行处理')
            return
        else:
            return openimg(self.lastdown_file)

    
    def tmpfile(self,path):
        dt = os.path.join(os.curdir,'tmp')
        if not os.path.exists(dt):
            os.makedirs(dt)
        return os.path.join(dt,'tmp-'+os.path.basename(path))
        

    def alert(self,msg):
        showinfo('提示', msg)
         
    def open_image(self):
        f = show_openfiledialog(os.curdir,'选择一张图片') 
        if(not f):return
        try:
            imgobj = ImageTk.PhotoImage(file=f)
            if(self.lastup):
                self.up.delete(self.lastup)
            self.lastup = self.up.create_image(2,2,anchor=NW,image=imgobj)
            self.lastup_file=f
            self.lastup_img=imgobj
        except:
            showerror('错误',"打开文件出错")
    
    def open_dir(self):
        f=askdirectory()
        if(not f):return
        self.origin_dir.set(f)
        result_d=os.path.join(f,'result')
        if not os.path.exists(result_d):
            os.mkdir(result_d)
        self.result_dir.set(result_d)
        
        
    def choose_color(self):
        rgb,_=show_colordialog()
        if(not rgb):
            pass
        else:
            showinfo('提示', 'color:(%s,%s,%s)' % rgb)
            
    def update_photo(self,f):
        try:
            imgobj = ImageTk.PhotoImage(file=f)
            if(self.lastdown):
                self.down.delete(self.lastdown)
            self.lastdown = self.down.create_image(2,2,anchor=NW,image=imgobj)
            self.lastdown_file=f
            self.lastdown_img=imgobj
        except:
            showerror('错误',"打开文件出错")
        
    
