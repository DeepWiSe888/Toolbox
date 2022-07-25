import numpy as np
import struct
try:
    from conf import *
except:
    from libs.conf import *

def parse_pack(pack):
    cursor = 0
    cursor = cursor + len(flag)
    
    # sec
    sec_pack_tmp = pack[cursor:cursor + 8]
    sec = list(struct.unpack('q',sec_pack_tmp))[0]
    cursor = cursor + 8

    # usec
    usec_pack_tmp = pack[cursor:cursor + 8]
    usec = list(struct.unpack('q',usec_pack_tmp))[0]
    usec = usec / 1000000
    cursor = cursor + 8

    # rx
    rx_pack_tmp = pack[cursor:cursor + 4]
    rx = list(struct.unpack('i',rx_pack_tmp))[0]
    cursor = cursor + 4

    # tx
    tx_pack_tmp = pack[cursor:cursor + 4]
    tx = list(struct.unpack('i',tx_pack_tmp))[0]
    cursor = cursor + 4

    # frame no
    fno_pack_tmp = pack[cursor:cursor + 4]
    fno = list(struct.unpack('i',fno_pack_tmp))[0]
    cursor = cursor + 4

    # DATA
    adc_data_pack_tmp = pack[cursor:]
    adc_data = list(struct.unpack('{}f'.format(len(adc_data_pack_tmp)//4),adc_data_pack_tmp))

    pack_dict = {'fno':fno,'tx':tx,'rx':rx,'t':sec + usec,'data':adc_data}
    return pack_dict


def range_fft(data,range_fft_n):
    data =  data * np.hanning(len(data))
    data_fft = np.fft.fft(data,range_fft_n)
    return data_fft
    