# -*- coding: utf-8 -*-
'''
然后训练bp神经网络
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
network_persist_file='fcr.pkl'



def train_fire_recognition():
    input_len,train_set=get_train_set()
    
    print 'building network (%s,%s,%s)' %(input_len, input_len/3, 1)
    n = Network(input_len, input_len/3, 1)
    

    count = len(train_set)
    print 'train set size: %s, start training...' % count
    for _ in xrange(10000):
        n.train(train_set[randint(0,count-1)],[1])
        time.sleep(0.0001)

    out=[1]
    print 'asserting train result...'
    for k, inp in train_set.items():
        assert round(n.test(inp)[0]) == out[0]

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
            tset[i] = imgtool.check_receptor(ospath.join(parent,f), IMG_PIXELS, PIXELS)
            i = i+1

    return PIXELS*PIXELS,tset

    
