# -*- coding: utf-8 -*-
'''
experiment on image manipulating
'''
import Image
import os.path as ospath
from math import sqrt
from PIL import ImageFilter,ImageEnhance
from Image import ANTIALIAS

def openimg(path):
    return Image.open(path)

def split(imgfile,img_w,img_h,patch=True):
    """分割图片，如果尺寸不够分割，则使用附近区域进行补充
    """
    im = Image.open(imgfile)
    w,h=im.size
    left,upper=0,0
    right = left+img_w 
    lower = upper+img_h
    while(right <= w or lower <= h):
        if(right > w):
            right = w
            left = w - img_w
            
        if(lower > h):
            lower = h
            upper = h - img_h
    
        box=(left,upper,right,lower)
        yield im.crop(box)
        left = right
        if(left >= w):
            #next row
            left = 0
            upper = lower
            lower = upper+img_h
            if(upper>= h):
                return
        #end if 
        right = left+img_w

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
        


def gray_scale(img):
    """转换为灰度图像
    """
    return img.convert('L')

def median_filter(img):
    """中值滤波
    """
    return img.filter(ImageFilter.MedianFilter)

def gaussian_filter(img):
    """高斯滤波
    """
    return img.filter(ImageFilter.GaussianBlur)

def enhance(img,factor=0.7):
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)

def detect_edge(img):
    """获取轮廓
    """
    return img.filter(ImageFilter.FIND_EDGES)

def detect_fire():
    """最大类间方差法分离火焰与背景图像
    """
def scale_img(img,scale):
    w,h = img.size
    w= int(w*scale if scale>=0 else w/abs(scale))
    h= int (h*scale if scale>=0 else h/abs(scale))
    if w==0:w=1
    if h==0:h=1
    return img.resize((w,h),resample=ANTIALIAS)

def detect_color(img, target, threshold):
    """阈值取色:根据颜色范围
    @param img: pil image object
    @param target: rgb tuple
    @param threshold: an integer value
    """
    raw = img.load()
    w,h= img.size
     
    for x in xrange(0, w):
        for y in xrange(0,h):
            color = raw[x,y]
            dis= abs(color[0]-target[0]) +  abs(color[1]-target[1]) +  abs(color[1]-target[1]) 
            if dis < threshold:
                pass
#                 raw[x,y]=255
            else:
                raw[x,y]=0
    return img
            

def calc_shape(img):
    """计算区域形状
    """
    pass

def sobel_sharp(image):  #sobel算子
    SobelX = [-1,0,1,-2,0,2,-1,0,1]
    SobelY = [-1,-2,-1,0,0,0,1,2,1]
    image = sharp(image,SobelX,SobelY)
    return image

def prewitt_sharp(image):#perwit算子
    PrewittX = [1,0,-1,1,0,-1,1,0,-1]
    PrewittY = [-1,-1,-1,0,0,0,1,1,1]
    image = sharp(image,PrewittX,PrewittY)
    return image
    
def isotropic_sharp(image):#isotropic算子
    IsotropicX = [1,0,-1,1.414,0,-1.414,1,0,-1]
    IsotropicY = [-1,-1.414,-1,0,0,0,1,1.414,1]
    image = sharp(image,IsotropicX,IsotropicY)
    return image
    
def sharp(image,arrayX,arrayY):
    w = image.size[0]
    h = image.size[1]
    size = (w,h)

    iSharpImage = Image.new('L', size)
    iSharp = iSharpImage.load()
    image = image.load()
    
    tmpX = [0]*9
    tmpY = [0]*9
    for i in range(1,h-1):
        for j in range(1,w-1):
            for k in range(3):
                for l in range(3):
                    tmpX[k*3+l] = image[j-1+l, i-1+k]*arrayX[k*3+l]
                    tmpY[k*3+l] = image[j-1+l, i-1+k]*arrayY[k*3+l]
            iSharp[j,i] = abs(sum(tmpX))+abs(sum(tmpY))
    return iSharpImage

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
            if(self.cache.has_key(args)):
                print 'get img data from cache'
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
def check_receptor(img,img_pixels, pixels):
    """
    Prepare the input of the neural network
    @param img: a PIL.Image at size (img_pixels, img_pixels)
    @return: a list() that should be used to feed your neural network
    """
    if(isinstance(img, (basestring))):
        img =Image.open(img)
    
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



