# -*- coding: utf-8 -*-
'''
整理下载的教材图片，统一切割为一定像素的小图
从中人工分类出A.有火情  B.无火情的两类图片
'''
import os
import os.path as ospath
import imgtool

download_dir='../download'
splited_dir='images/splited'
img_w=30
img_h=30

def prepare():
    print 'preparing images in dir:%s' % download_dir
    for parent,_,files in os.walk(download_dir):
        for f in files:
            imgtool.split_then_save(ospath.join(parent,f),splited_dir, img_w,img_h)
            
        print 'preparing images done to dir:%s' % splited_dir


