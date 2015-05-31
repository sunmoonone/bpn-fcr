# -*- coding: utf-8 -*-
'''
训练bp神经网络
'''
import imgtool
import os 
import os.path as ospath
from bpnn.network import Network
import cPickle
from random import randint
import time

img_w=30
img_h=30

PIXELS = 20
IMG_PIXELS = 30

source_dir_fire = 'images/splited/fire'
source_dir_safe = 'images/splited/safe'
network_persist_file='fcr.pkl'



def train_fire_recognition():
    input_len = PIXELS * PIXELS
    train_set = get_train_set()
    print 'building network (%s,%s,%s)' %(input_len, input_len/3, 1)
    n = Network(input_len, input_len/3, 1)
    

    count = len(train_set)
    print 'train set size: %s, start training...' % count
    for _ in xrange(10000):
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
        
def get_train_set():
    """返回输入向量和每个向量的长度
    """
    i=0
    tset={}
    for parent,_,files in os.walk(source_dir_fire,True):
        for f in files:
            tset[i] = (imgtool.check_receptor(ospath.join(parent,f), IMG_PIXELS, PIXELS), [1])
            i = i+1

    for parent,_,files in os.walk(source_dir_safe,True):
        for f in files:
            tset[i] = (imgtool.check_receptor(ospath.join(parent,f), IMG_PIXELS, PIXELS) ,[0] )
            i = i+1

    return tset
