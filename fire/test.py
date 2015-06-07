# -*- coding: utf-8 -*-
'''
鉴别
夜景，室内需分别建立训练库进行训练

对于明火与灯光、蜡烛的区分，不能通过bp网络来做，应该通过聚类算法，事先排除灯光和蜡烛
之后再通过bp网络进行鉴定
'''
import os
import cPickle
import os.path as ospath
from fire import imgtool
import train
source_dir = 'images/origin'

def test_file(imgfile):
    with open(train.network_persist_file,'r') as f:
        net= cPickle.load(f)
    for img in imgtool.split(imgfile, train.IMG_PIXELS, train.IMG_PIXELS):
        inp = imgtool.check_receptor(img, train.IMG_PIXELS, train.PIXELS)
        out = net.test(inp)
        out = out[0]
        if(out > 0.5):
            return 'danger'
    return 'safe'

def test():
    """
    """
    #加载网络训练结果
    with open(train.network_persist_file,'r') as f:
        net= cPickle.load(f)

    #创建danger子目录
    danger_dir = ospath.join(source_dir,'danger') 
    if(not ospath.exists(danger_dir)):
        os.mkdir(danger_dir)

    for f in os.listdir(source_dir): 
        fp = ospath.join(source_dir,f)
        if(ospath.isfile(fp)):
            print 'testing file %s...' % fp
            for img in imgtool.split(fp, train.IMG_PIXELS, train.IMG_PIXELS):
                inp = imgtool.check_receptor(img, train.IMG_PIXELS, train.PIXELS)
                out = net.test(inp)
                out = out[0]
                if(out > 0.5):
                    print 'copy to danger: %s' % fp
                    with open(ospath.join(danger_dir,ospath.basename(fp)), "wb") as df:
                        df.write(open(fp, "rb").read())
                    break
                    
                    
                    
                    