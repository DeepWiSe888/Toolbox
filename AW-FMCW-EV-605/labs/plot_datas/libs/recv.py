import time
import serial
import struct
from queue import Queue

try:
    from conf import *
    from utils import *
except:
    from libs.conf import *
    from libs.utils import *


Cache = Queue()

class SerialCollect(object):
    def __init__(self,port,baudrate = 4000000):
        self.state = False
        #if open serial error return
        try:
            self._s = serial.Serial(port=port,baudrate=baudrate,timeout=1)
        except serial.SerialException:
            print("open serial error.")
            return
        
        #pack head flag
        self._pack_head = flag
        #tmp cache
        self._packs = bytes()
        
    def recv_data(self):
        while True:
            data = self._s.read(2048)
            if not data:
                print('fails to read data.')
                # self._s.close()
                self._packs = bytes()
                time.sleep(1)
                continue
            self._packs = self._packs + data
            while True:
                start_index = self._packs.find(self._pack_head)
                if(start_index == -1):
                    break
                end_index = self._packs.find(self._pack_head,start_index+len(self._pack_head))
                if(end_index == -1):
                    break
                pack = self._packs[start_index:end_index]
                pack_dict = parse_pack(pack)
                pack_dict['byte'] = pack
                if len(pack_dict['data']) >= num_tx * num_rx * num_chirps_per_frame * num_samples_per_chirp:
                    Cache.put(pack_dict)
                if pack_dict['fno'] % 100 == 0:
                    print('fn:{},tx:{},rx:{},t:{},data_len:{}'.format(pack_dict['fno'],pack_dict['tx'],pack_dict['rx'],pack_dict['t'],len(pack_dict['data'])))
                self._packs = self._packs[end_index:]