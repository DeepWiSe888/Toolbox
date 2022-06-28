import os
import time
import struct
import numpy as np
from libs.conf import *


def parse_pack_from_file(pack):
    """
    parse save file packet

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
    # sec
    sec_pack_tmp = pack[0:cursor + 4]
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
    tx = int(tx / 8)
    cursor = cursor + 4

    # rx
    rx_pack_tmp = pack[cursor:cursor + 4]
    rx = list(struct.unpack('i',rx_pack_tmp))[0]
    rx = int(rx / 8)
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

def parse_pack_from_stream(pack):
    """
    parse save file packet

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
