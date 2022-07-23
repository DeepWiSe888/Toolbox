# configuration


'''
The radar data acquisition parameters
'''
flag = b'\x77\x69\x72\x75\x73\x68\x2d\x76\x70\x61\x73\x3a'
flag_size = 12





'''
The Process Parameters
'''
# remove dc
remove_dc = True

# the number of points of range fft
num_range_nfft = 512

# the number of points of range bin
num_range_bins = num_range_nfft // 2

# the number of points of doppler fft
num_doppler_nfft = 64

# the number of points of angle fft
num_angle_nfft = 180

# range resolution
range_res = 0.0514

# the range searched on the distance dimension
search_start = 0

# scann area,unit:m
scann_area = 3
search_end = 138

# target bin cnt 
target_range_bin = 3

# each target select doppler points
target_speed_cnt = 15

# By default,raw data fps is 2042
RAW_FPS = 2042

# The fps after sampling, FPS < RAW_FPS
FPS = 40

# radar,range_start,float,The minimum distance of scan
RANGE_SATRT = 0.2

# radar,range_end,float,The maximum distance of scan
RANGE_END= 7.0

#alg,frames,int,calculate step,default value is 1s(fps)
STEP = FPS

#alg,bin_offset,int,0-138
OFFSET = 0 

#alg,max_bin=138(7m),int,0-138
MAX_BIN = 130 

#alg,frames,int,calculate window 6s
SEC = 20
FRAMES = SEC * FPS 
NFFT = FRAMES

#default
RANGE_RESOLUTION = range_res





