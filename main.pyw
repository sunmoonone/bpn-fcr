# encoding: utf-8
'''
使用说明：
python main.py prepare: 准备教材图片

python main.py train: 训练bp网络

python main.py test 测试bp网络 将包含火情的图片拷贝到danger子目录

python main.py monitor <dir_path> 监控目录，将其中有火情的图片转移的该目录的子目录danger 里
'''
import sys
from gui.main import mainloop

def cmdmain():
    usage = 'Usage: %s prepare | train | test | monitor <dir_path>' % sys.argv[0]
    if(len(sys.argv) < 2):
        print usage
        sys.exit(0)
    cmd = sys.argv[1]
    
    if(cmd == 'prepare'):
        from fire.prepare import prepare
        sys.exit(prepare())
    
    elif(cmd == 'train'):
        from fire.train import train_fire_recognition
        sys.exit(train_fire_recognition())
    
    elif(cmd=='test'):
        from fire.test import test
        sys.exit(test())
    else:
        print "%.3f" % (2.0/3)
    
if __name__ == '__main__':
    mainloop()
    
