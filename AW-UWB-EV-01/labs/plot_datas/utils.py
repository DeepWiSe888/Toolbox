import os
import numpy as np
import configparser


class ReadConfig(object):
    def __init__(self,config_file = None):
        self.config_file = None
        if config_file:
            self.config_file = config_file
        else:
            root_dir = os.path.dirname(os.path.abspath('.'))
            self.config_file = os.path.join(root_dir,"config.ini")
        self.conf = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            self.conf.read(self.config_file)
            print("config file is {}".format(self.config_file))
        else:
            print('config file not exist')
    def get_conf(self,section,option,type):
        value = None
        try:
            if type == 'int':
                tmp = self.conf.getint(section, option)
                value = tmp if tmp >=0 else None
            elif type == 'float':
                tmp = self.conf.getfloat(section, option)
                value = tmp if tmp > 0 else None
            elif type == 'bool':
                value = self.conf.getboolean(section, option)
            else:
                value = self.conf.get(section, option)
        except (configparser.NoOptionError,configparser.NoSectionError) as e:
            print(e)
        return value

#read the config
print("=============== start read config ===============")
conf = ReadConfig('./config.ini')

#radar,fps,int
fps_value = conf.get_conf('radar','fps','int')
FPS = 40 if fps_value is None else fps_value
print('radar fps:{}'.format(FPS))

#radar,pps,int
pps_value = conf.get_conf('radar','pps','int')
PPS = 128 if pps_value is None else pps_value
print('radar pps:{}'.format(PPS))

#radar,iter,int
iter_value = conf.get_conf('radar','iter','int')
if iter_value & (iter_value - 1) != 0:
    print("iter should be 2**n.")
ITER = 8 if iter_value is None else iter_value
print('radar iter:{}'.format(ITER))

#radar,dmin,int
dmin_value = conf.get_conf('radar','dmin','int')
DMIN = 949 if dmin_value is None else dmin_value
print('radar dac min:{}'.format(DMIN))

#radar,dmax,int
dmax_value = conf.get_conf('radar','dmax','int')
DMAX = 1100 if dmax_value is None else dmax_value
print('radar dac max:{}'.format(DMAX))

#radar,range_start,float,The minimum distance of scan
range_start_value = conf.get_conf('radar','range_start','float')
RANGE_SATRT = 0.2 if range_start_value is None else range_start_value
print('radar range start:{}'.format(RANGE_SATRT))

#radar,range_end,float,The maximum distance of scan
range_end_value = conf.get_conf('radar','range_end','float') 
RANGE_END= 5.0 if range_end_value is None or range_end_value > 5.0 else range_end_value
print('radar range end:{}'.format(RANGE_END))

#alg,frames,int,calculate step,default value is 1s(fps)
# step_value = conf.get_conf('alg','step','int')
STEP = FPS
print('plot calculate step:{}'.format(STEP))

#alg,bin_offset,int,0-95
bin_offset_value = conf.get_conf('alg','bin_offset','int')
OFFSET = 0 if bin_offset_value is None or bin_offset_value > 95 else bin_offset_value
print('plot calculate bin offset:{}'.format(OFFSET))

#alg,max_bin=96(5m),int,1-96
MAX_BIN = 96 

#alg,frames,int,calculate window 6s
FRAMES = 6 * FPS 
NFFT = FRAMES

#default
RANGE_RESOLUTION = 0.0514

print("=============== read config end ===============")
