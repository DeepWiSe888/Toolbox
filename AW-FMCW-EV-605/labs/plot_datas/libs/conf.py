# speed of light
c = 3e8

# ADC sample rate of 1MHz
sample_rate_Hz = 1e6  

chirp_time = 0.000411238                

# RX antenna 1 activated
num_rx = 3

# TX antenna 1 activated  
num_tx = 1

# lower frequency: 59.133931281 GHz               
min_RF_frequency_Hz = 58000000000

# upper frequency: 62.366068720 GHz   
max_FR_frequency_Hz = 63000000000

#Bandwith
B = max_FR_frequency_Hz - min_RF_frequency_Hz

# slope
S = B / chirp_time

# an object at a distance d produces an IF frequence of:
# f_if = (2 * S) * d / c
# maximum range 
d_max = sample_rate_Hz / 2 * c / (2 * S)


# 128 samples per chirp
num_samples_per_chirp = 128   

# 4 chirps per frame
num_chirps_per_frame = 4    

# Frame repetition time default 0.025s (frame rate of 40Hz)         
fps = 40

# pack flag
flag = b'\x77\x69\x72\x75\x73\x68\x2d\x76\x70\x61\x73\x3a'
flag_size = 12

# remove dc
remove_dc = True

# the number of points of range fft
num_range_nfft = 128

# the number of points of range bin
num_range_bins = num_range_nfft // 2

# the number of points of doppler fft
num_doppler_nfft = 64

SEC = 6

FPS = SEC * fps

FRAMES = FPS

STEP = 1 * fps

OFFSET = 0

MAX_BIN = num_range_bins

RANGE_RESOLUTION = d_max / num_range_nfft

RANGE_SATRT = 0

NFFT = num_doppler_nfft