# -*- coding: utf-8 -*-
'''
整理下载的教材图片，统一切割为一定像素的小图
从中人工分类出A.有火情  B.无火情的两类图片
'''
import os
import os.path as ospath
import imgtool
from bpnn.network import Network
from random import randint
import time
import cPickle
from fire import train
from fire.imgtool import openimg



def prepare():
    download_dir='images/origin'
    splited_dir='images/splited'
    img_w =30
    img_h=30
    print 'preparing images in dir:%s' % download_dir
    for f in os.listdir(download_dir):
        f=ospath.join(download_dir,f)
        if(ospath.isfile(f)):
            imgtool.split_then_save(f,splited_dir, img_w,img_h)
            
        print 'preparing images done to dir:%s' % splited_dir

def batch_preprocess(dt,rdt,img_w,img_h,threshold=100,color=None,ondone=None):
    """图像预处理
    预处理步骤:
    1.去噪
    2.锐化增强
    3.阀值取色
    4.生成固定大小的局部图像
    """
    file_no=0
    for f in os.listdir(dt):
        f=ospath.join(dt,f)
        if not ospath.isfile(f):
            continue
        try:
            img = imgtool.openimg(f)
        except:
            continue
        print 'preprocess %s' % ospath.basename(f)
        img = imgtool.median_filter(img)
        img = imgtool.detect_color(img, color, threshold)
#         img = imgtool.gray_scale(img)
        for im in imgtool.split(img, img_w, img_h):
            #ignore balck piece
            if(imgtool.all_balck(im,20)):
                continue
            im.save(ospath.join(rdt,"img_%s.jpg" % file_no),'JPEG')
            file_no = file_no + 1
            
    print 'preparing images done to dir:%s' % rdt
    if ondone:ondone()

def test(imgfile,w,h,threshold,color):
    with open(train.network_persist_file,'r') as f:
        net= cPickle.load(f)
    data = openimg(imgfile)
    data = imgtool.median_filter(data)
    data = imgtool.detect_color(data, color, threshold)
    for img in imgtool.split(data, w,h):
        if(imgtool.all_balck(img, 10)):
            continue
        inp = imgtool.check_receptor(img, w,h)
        out = net.test(inp)
        out = out[0]
        if(out > 0.5):
            return 'danger'
    return 'safe'


network_persist_file='fcr.pkl'
def train_fire_recognition(srcdir,pixw,pixh,callback):
    """训练火焰识别
    """
    input_len = pixw * pixh
    train_set = get_train_set(srcdir,pixw,pixh)
    print 'building network (%s,%s,%s)' %(input_len, input_len/3, 1)
    n = Network(input_len, input_len/3, 1)
    

    count = len(train_set)
    print 'start training...'
    for _ in xrange(100):
        pair = train_set[randint(0,count-1)]
        n.train(pair[0],pair[1])
        time.sleep(0.0001)

    print 'asserting train result...'
    err_count=0
    for inp in train_set.values():
        rt = n.test(inp[0])[0]
        if ( rt < 0.5 and  inp[1] ==1):
            print 'not match round(%s) <-> %s' % (rt,inp[1])
            err_count = err_count+1
    print 'match rate: %.3f' % ( (count - err_count)*1.0 / count)

            

    print 'persisting network state to file: %s...' % network_persist_file
    with open(network_persist_file,'w') as f:
        cPickle.dump(n, f)
    callback()
    
def get_train_set(source_dir_fire,pixw,pixh):
    """返回输入向量和每个向量的长度
    """
    print 'initializing train set from %s' % source_dir_fire
    i=0
    tset={}
    for f in os.listdir(source_dir_fire):
        f=ospath.join(source_dir_fire,f)
        if(not ospath.isfile(f)):
            continue
        try:
            img = imgtool.openimg(f)
        except:
            continue
        tset[i] = (imgtool.check_receptor(img, pixw, pixh), [1])
        i = i+1
            

#     for parent,_,files in os.walk(source_dir_safe,True):
#         for f in files:
#             tset[i] = (imgtool.check_receptor(ospath.join(parent,f), IMG_PIXELS, PIXELS) ,[0] )
#             i = i+1
    print 'train set size: %s' % (i+1)
    return tset


