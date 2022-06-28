import os
from libs.utils import *

class RawDataReader():
    def __init__(self,path):
        self.path = path
        self.raw_fid = None
        self.pack_buffer = bytes()
        self.buffer_size = 1136
        self._open(self.path)

    # def get_next_frame(self):
    #     pack = self.raw_fid.read(self.buffer_size)
    #     if not pack or len(pack) < self.buffer_size:
    #         self._close()
    #         return None
    #     pack_dict = parse_pack_from_file(pack)
    #     return pack_dict
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
                pack_dict = parse_pack_from_stream(pack)
                self.pack_buffer = self.pack_buffer[end_index:]
                break
        return pack_dict
        
    def _open(self,f):
        self.raw_fid = open(f,'rb')
        
    def _close(self):
        if self.raw_fid is not None:
            self.raw_fid.close()


if __name__ == "__main__":
    path = "./datas/111/"
    files = []
    if os.path.isdir(path):
        fs = os.listdir(path)
        for f in fs:
            if f.endswith('.txt'):
                files.append(path + f)
    else:
        if path.endswith('.txt'):
            files.append(path)

    framelist = []
    for file in files:
        reader = RawDataReader(file)
        while True:
            frame = reader.get_next_frame()
            if frame is None:
                break
            framelist.append(frame)
    print(len(framelist))