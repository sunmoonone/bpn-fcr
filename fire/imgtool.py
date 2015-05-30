# -*- coding: utf-8 -*-
'''
experiment on image manipulating
'''
import Image
import os.path as ospath
from math import sqrt

def split(imgfile,width,height,patch=True):
    """分割图片，如果尺寸不够分割，则使用附近区域进行补充
    """
    pass

file_no=1
def split_then_save(imgfile,dest_dir, img_w, img_h):
    """将一张图片按尺寸分割后，将结果图片存入目标目录，不够分割的部分舍弃
    """
    global file_no
    im = Image.open(imgfile)
    w,h=im.size
    left,upper=0,0
    right = left+img_w 
    lower = upper+img_h
    while(right <= w and lower <= h):
        box=(left,upper,right,lower)
        piece = im.crop(box)
        piece.save(ospath.join(dest_dir,"img_%s.jpg" % file_no),'JPEG')
        file_no = file_no + 1
        left = right
        if(left >= w):
            #next row
            left = 0
            upper = lower
            lower = upper+img_h
        #end if 
        right = left+img_w
        


#灰度

#二值化

#中值滤波

#圆形度

#输出向量

#缩小


class memoized(object):
    """
    Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args, **kwargs):
        try:
            if 'cacheable' in kwargs and kwargs['cacheable'] != True:
                raise TypeError('') # Dummy hack

            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            return self.func(*args)
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


@memoized
def check_receptor(imgfile,img_pixels, pixels):
    """
    Prepare the input of the neural network
    @param img: a PIL.Image at size (img_pixels, img_pixels)
    @return: a list() that should be used to feed your neural network
    """
    img =Image.open(imgfile)
    print 'image info:' ,img.format, img.size, img.mode
    raw = img.load()
    receptor_states = [0] * (pixels * pixels)

    xstep = img_pixels / float(pixels)
    ystep = img_pixels / float(pixels)

    for i in xrange(0, img_pixels):
        for j in xrange(0, img_pixels):

            x = int(j / xstep)
            y = int(i / ystep)

            color = raw[j, i]


            value = sqrt(color[0] ** 2 + \
                         color[1] ** 2 + \
                         color[2] ** 2)
            receptor_states[y * pixels + x] += value


    imax = max(receptor_states)

    if imax > 0:
        receptor_states = map(lambda x: x / imax, receptor_states)

    return receptor_states
