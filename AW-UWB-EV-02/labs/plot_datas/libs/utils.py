import os
import time
import struct
import numpy as np
from libs.conf import *


def parse_pack(pack):
    """
    parse pack

    Parameters
    ----------
    pack : bytes
        stream packet

    Returns
    -------
    pack_dict : dict
        packet dict after parse
    
    """
    cursor = 0
    cursor = cursor + flag_size
    # sec
    sec_pack_tmp = pack[cursor:cursor + 4]
    sec = list(struct.unpack('i',sec_pack_tmp))[0]
    cursor = cursor + 4

    # usec
    usec_pack_tmp = pack[cursor:cursor + 4]
    usec = list(struct.unpack('i',usec_pack_tmp))[0]
    usec = usec / 10000
    cursor = cursor + 4

    # tx
    tx_pack_tmp = pack[cursor:cursor + 4]
    tx = list(struct.unpack('i',tx_pack_tmp))[0]
    cursor = cursor + 4

    # rx
    rx_pack_tmp = pack[cursor:cursor + 4]
    rx = list(struct.unpack('i',rx_pack_tmp))[0]
    cursor = cursor + 4

    # frame no
    fno_pack_tmp = pack[cursor:cursor + 4]
    fno = list(struct.unpack('i',fno_pack_tmp))[0]
    cursor = cursor + 4

    # i
    i_pack_tmp = pack[cursor:cursor + 138*4]
    i = list(struct.unpack('138f',i_pack_tmp))
    cursor = cursor + 138*4

    # q
    q_pack_tmp = pack[cursor:cursor + 138*4]
    q = list(struct.unpack('138f',q_pack_tmp))

    # iq
    iq = np.array(i) + 1j*np.array(q)

    pack_dict = {'fno':fno,'tx':tx,'rx':rx,'t':sec + usec,'iq':iq}
    return pack_dict

def downsampling(frames):
    total_frame = len(frames)
    spacing = round(RAW_FPS / FPS)
    index = np.arange(0,total_frame,spacing)
    d_frames = frames[index]
    return d_frames
