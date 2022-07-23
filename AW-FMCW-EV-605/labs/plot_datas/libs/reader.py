
import os

try:
    from utils import *
except:
    from libs.utils import *

class RawDataReader():
    def __init__(self,path):
        self.path = path
        self.raw_fid = None
        self.pack_buffer = bytes()
        self.buffer_size =  num_tx * num_rx * num_chirps_per_frame * num_samples_per_chirp * 4 + 40
        self._open(self.path)

    def get_next_frame(self):
        while True:
            if len(self.pack_buffer)  < self.buffer_size * 2:
                pack = self.raw_fid.read(self.buffer_size)
                if not pack:
                    return None
                self.pack_buffer += pack
            start_index = self.pack_buffer.find(flag)
            if(start_index == -1):
                continue
            end_index = self.pack_buffer.find(flag,start_index+flag_size)
            if(end_index == -1):
                continue
            else:
                pack = self.pack_buffer[start_index:end_index]
                pack_dict = parse_pack(pack)
                self.pack_buffer = self.pack_buffer[end_index:]
                break
        return pack_dict
        
    def _open(self,f):
        self.raw_fid = open(f,'rb')
        
    def _close(self):
        if self.raw_fid is not None:
            self.raw_fid.close()