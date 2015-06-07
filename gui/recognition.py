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
        self.scale=DoubleVar(uiparent,value=0)
        self.enhance_factor=DoubleVar(uiparent,value=0)
        self.result_dir=StringVar(uiparent)
        self.croppixels=StringVar(uiparent)
        self.origin_dir=StringVar(uiparent)
        
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
        ent.pack(side=LEFT,fill=X,padx=5)

        row=LabelFrame(leftframe,text='批量预处理',padx=20,pady=20)
        row.pack(side=TOP,fill=X)
        
        row1=Frame(row)
        row1.pack(side=TOP,expand=YES,fill=X)
        Label(row1,text='处理结果目录:').pack(side=LEFT,padx=2)
        ent = Entry(row1,textvariable=self.result_dir)
        ent.pack(side=RIGHT,expand=YES,fill=X,padx=2)
 
        row1=Frame(row)
        row1.pack(side=TOP,expand=YES,fill=X,pady=10)
        Label(row1,text='切块尺寸:').pack(side=LEFT,padx=2)
        self.croppixels.set('50x50')
        ent = Entry(row1,textvariable=self.croppixels)
        ent.pack(side=RIGHT,expand=YES,fill=X,padx=2)
        
        Button(row,text='执行预处理',command=self.begin_preprocess).pack(expand=YES,fill=X,side=TOP,pady=10)
        self.prebar = ttk.Progressbar(row,mode='indeterminate')
        self.prebar.pack(side=TOP,fill=X)
        
        
        
        row=LabelFrame(leftframe,text='训练',padx=20,pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='开始训练',command=self.begin_train).pack(expand=YES,fill=X,side=TOP,pady=10)
        self.trainbar = ttk.Progressbar(row,mode='indeterminate')
        self.trainbar.pack(side=TOP,fill=X)

        row=Frame(leftframe)
        row.config(pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='打开图片',command=self.gray_process).pack(expand=YES,fill=X,side=LEFT)
        Button(row,text='识别',command=self.gray_process).pack(expand=YES,fill=X,side=LEFT)
        row=Frame(leftframe)
        row.config(pady=10)
        row.pack(side=TOP, fill=X)
        Label(row,text='识别结果:').pack(side=LEFT)

    def begin_preprocess(self):
        self.prebar.start(10)
    
    def begin_train(self):
        self.trainbar.start(10)
        pass
    
    def median_process(self):
        img = self._open_img()
        if not img:return
            
        img = median_filter(img)
        path= self.tmpfile(self.lastup_file)
        img.save(path,'JPEG')
        self.update_photo(path)
            
    def gaussian_process(self):
        img = self._open_img()
        if not img:return
            
        img = gaussian_filter(img)
        path= self.tmpfile(self.lastup_file)
        img.save(path,'JPEG')
        self.update_photo(path)

    def ostu_process(self):
        img = self._open_img()
        if not img:return
            
        img = ostu_capture(img,True)
        path= self.tmpfile(self.lastup_file)
        img.save(path,'JPEG')
        self.update_photo(path)
    
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

    def color_detect_process(self):
        sc = self.colortodetect.get()
        c=None
        try:
            c = ImageColor.getrgb(sc)
        except:
            pass
        
        if not c: 
            self.alert('请设置正确的颜色')
        th = self.threshold.get()
        img = self._open_img()
        img = detect_color(img,c,th)
        path= self.tmpfile(self.lastup_file)
        img.save(path,'JPEG')
        self.update_photo(path)
        
    def gray_process(self):
        img = self._open_img()
        if not img:return
            
        img = gray_scale(img)
        path= self.tmpfile(self.lastup_file)
        img.save(path,'JPEG')
        self.update_photo(path)
            
    def enhance_process(self):
        img = self._open_img()
        if not img:return
            
        img = enhance(img,self.enhance_factor.get())
        print self.enhance_factor.get()
        path= self.tmpfile(self.lastup_file)
        img.save(path,'JPEG')
        self.update_photo(path)
    
    scaling=False
    def do_scale(self,scale):
        if(self.scaling):return
        scale=float(scale)
        if scale==0:return
        img = self._open_img()
        if not img:return
        self.scaling=True
        img = scale_img(img,scale)
        path= self.tmpfile(self.lastup_file)
        img.save(path,'JPEG')
        self.update_photo(path)
        self.scaling=False
            
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
        
    
