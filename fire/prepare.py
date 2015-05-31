# -*- coding: utf-8 -*-
'''
整理下载的教材图片，统一切割为一定像素的小图
从中人工分类出A.有火情  B.无火情的两类图片
'''
import os
import os.path as ospath
import imgtool

download_dir='images/origin'
splited_dir='images/splited'
img_w=30
img_h=30

def prepare():
    print 'preparing images in dir:%s' % download_dir
    for f in os.listdir(download_dir):
        f=ospath.join(download_dir,f)
        if(ospath.isfile(f)):
            imgtool.split_then_save(f,splited_dir, img_w,img_h)
            
        print 'preparing images done to dir:%s' % splited_dir

def preprocess():
    """图像预处理
    预处理步骤:
    1.去噪
    2.阀值取色,生成一个局部图像
    3.锐化增强
    4.将得到的局部图像缩放到一个固定的大小
    5.返回缩放后的图片
    """
    pass


