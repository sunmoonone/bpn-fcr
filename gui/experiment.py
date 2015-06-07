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


class Experiment(object):
    '''图片处理试验
    
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
        self.threshold=IntVar(uiparent,value=100)
        self.colortodetect=StringVar(uiparent)
        
        leftframe=Frame(uiparent)
        leftframe.config(width=300,height=500)
        leftframe.pack(side=LEFT,anchor=W,padx=10)
        
        rightframe=Frame(uiparent)
        rightframe.pack(side=RIGHT,expand=YES,fill=BOTH,padx=10)
        rightup=Frame(rightframe,pady=10)
        rightup.pack(side=TOP,expand=YES,fill=BOTH)
        rightdown=Frame(rightframe)
        rightdown.pack(side=TOP,expand=YES,fill=BOTH)
        
        self.up=Canvas(rightup,bg='gray',width=820,height=330, relief=SUNKEN,highlightthickness=0)
        hbar=Scrollbar(rightup,command=self.up.xview,orient='horizontal')
        vbar=Scrollbar(rightup,command=self.up.yview)
        
        self.up.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set,scrollregion=(0,0,1000,600))

        vbar.pack(side=RIGHT,expand=YES,fill=Y)
        self.up.pack(side=TOP,expand=YES,fill=BOTH)
        hbar.pack(side=TOP,expand=YES,fill=X)
        
        self.down=Canvas(rightdown,bg='gray',width=820,height=330, relief=SUNKEN,highlightthickness=0)
        hbar2=Scrollbar(rightdown,command=self.down.xview,orient='horizontal')
        vbar2=Scrollbar(rightdown,command=self.down.yview)
        
        self.down.config(xscrollcommand=hbar2.set,yscrollcommand=vbar2.set,scrollregion=(0,0,1000,600))

        vbar2.pack(side=RIGHT,expand=YES,fill=Y)
        self.down.pack(side=TOP,expand=YES,fill=BOTH)
        hbar2.pack(side=TOP,expand=YES,fill=X)
        

        row=Frame(leftframe)
        row.config(pady=10)
        row.pack(side=TOP, fill=X)
        Button(row,text='打开图片...',command=self.open_image).pack(expand=YES,fill=X,side=LEFT)

        row=Frame(leftframe)
        row.config(pady=20)
        row.pack(side=TOP, fill=X)
        Label(row,text='以下处理针对:').pack(side=LEFT)
        Radiobutton(row,text='上图',value=0,variable=self.which).pack(side=LEFT,expand=YES,fill=X)
        Radiobutton(row,text='下图',value=1,variable=self.which).pack(side=LEFT,expand=YES,fill=X)

        row=LabelFrame(leftframe,text='图像滤波',padx=20,pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='中值滤波',command=self.median_process).pack(expand=YES,fill=X,side=TOP,pady=10)
        Button(row,text='高斯滤波',command=self.gaussian_process).pack(expand=YES,fill=X,side=TOP)
        
        row=LabelFrame(leftframe,text='图像分割',padx=20,pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='类间方差分割',command=self.ostu_process).pack(expand=YES,fill=X,side=TOP,pady=10)
        Button(row, text='手动颜色分割',command=self.color_detect_process).pack(side=LEFT)
        Label(row,width='4',text=' 范围:').pack(side=LEFT,padx=2)
        ent = Spinbox(row,width=10,from_=0,to=255,increment=1,textvariable=self.threshold)
        ent.pack(side=LEFT,padx=2)

        Label(row,width='4',text=' 颜色:').pack(side=LEFT,padx=2)
        ent = Entry(row,textvariable=self.colortodetect)
        ent.insert(0, '#ff0000')
        ent.pack(side=RIGHT,expand=YES,fill=X,padx=2)
        
        row=Frame(leftframe)
        row.config(pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='灰度化',command=self.gray_process).pack(expand=YES,fill=X,side=LEFT)
        
        row=Frame(leftframe)
        row.config(pady=20)
        row.pack(side=TOP, fill=X)
        Button(row,text='边缘增强',command=self.enhance_process).pack(side=LEFT)
        
        ent = Spinbox(row,width=10,from_=0,to=1,increment=0.1,textvariable=self.enhance_factor)
        ent.pack(side=LEFT,expand=YES,fill=X,padx=2)
        
        row=Frame(leftframe)
        row.config(pady=20)
        row.pack(side=TOP, fill=X)
        Label(row,text='缩放:').pack(side=LEFT,anchor=W,padx=2)
        sc = Scale(row,from_=-10,to=10,tickinterval=5,orient=HORIZONTAL,resolution=1,
                   variable=self.scale,command=self.do_scale,repeatinterval=600)
        sc.pack(side=LEFT,expand=YES,fill=X)

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
        
    