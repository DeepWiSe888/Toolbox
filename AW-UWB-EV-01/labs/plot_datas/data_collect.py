import time
import struct
import serial
import numpy as np

from utils import *
from data_cache import data_queue


class SerialCollect(object):
    def __init__(self,port,baudrate = 4000000):
        self.state = False
        #if open serial error return
        try:
            self._s = serial.Serial(port=port,baudrate=baudrate,timeout=1)
        except serial.SerialException:
            print("open serial error.")
            return
        self._last_fn = 0
        self.state = True
        #pack size
        self._pack_size = 820
        #pack head flag
        self._pack_head = b'\xe9\xcf\x93\x72'
        #tmp cache
        self._packs = bytes()
        #set device param
        self.state = self._set_dev()
        if not self.state:
            self._s.close()

    def _set_dev(self):
        cmd = 'AT+STOP\r\n'
        stop_state = self.send(cmd)
        if stop_state:
            print("stop success.")
        else:
            print("stop error.")
            return False

        #get the version
        cmd = 'AT+VERSION\r\n'
        get_version_state = self.get_version(cmd)
        if not get_version_state:
            print("hardware version error,just support 1.1.")
            return False

        #set fps
        cmd = 'AT+FPS {}\r\n'.format(FPS)
        set_fps_state = self.send(cmd)
        if set_fps_state:
            print("set fps success.")
        else:
            print("set fps error.")
            return False

        #set pps
        cmd = 'AT+PPS {}\r\n'.format(PPS)
        set_pps_state = self.send(cmd)
        if set_pps_state:
            print("set pps success.")
        else:
            print("set pps error.")
            return False

        #set iter
        cmd = 'AT+ITER {}\r\n'.format(ITER)
        set_iter_state = self.send(cmd)
        if set_iter_state:
            print("set iter success.")
        else:
            print("set iter error.")
            return False
        
        #set dac min
        cmd = 'AT+DMIN {}\r\n'.format(DMIN)
        set_dmin_state = self.send(cmd)
        if set_dmin_state:
            print("set dac min success.")
        else:
            print("set dac min error.")
            return False

        #set iter
        cmd = 'AT+DMAX {}\r\n'.format(DMAX)
        set_dmax_state = self.send(cmd)
        if set_dmax_state:
            print("set dac max success.")
        else:
            print("set dac max error.")
            return False

        #set scan area
        cmd = 'AT+DIST {},{}\r\n'.format(RANGE_SATRT,RANGE_END)
        set_area_state = self.send(cmd)
        if set_area_state:
            print("set scan area success.")
        else:
            print("set scan area error.")
            return False

        #send start command
        cmd = 'AT+START\r\n'
        start_state = self.send(cmd)
        if start_state:
            print("start success.")
        else:
            print("start error.")
            return False

        return True

    def get_version(self,cmd):
        self._s.write(cmd.encode())
        print("-->:",cmd.encode())
        response = b''
        start_time = time.time()
        while True:
            end_time = time.time()
            tmp = self._s.read(1)
            if not tmp:
                print('No response received.')
                state = False
                break
            response += tmp
            if len(response) >= 15 and response.find(b'/r/n') >= 0:
                idx = response.find(b'VERSION:')
                print("<--:",response[idx:idx + 15])
                state = True
                break
            if end_time - start_time >= 10: #read timeout 10s
                print("read timeout")
                state = False
                break
        return state

    def send(self,cmd):
        state = True
        self._s.write(cmd.encode())
        print("-->:",cmd.encode())
        response = b''
        start_time = time.time()
        while True:
            end_time = time.time()
            tmp = self._s.read(1)
            if not tmp:
                print('No response received.')
                state = False
                break
            response += tmp
            if len(response) >= 4 and response.find(b'OK\r\n') >= 0:
                idx = response.find(b'OK\r\n')
                print("<--:",response[idx:idx + 4])
                state = True
                break
            if end_time - start_time >= 10: #read timeout 10s
                print("read timeout")
                state = False
                break
        return state

    def recv(self):
        while self.state:
            data = self._s.read(4096)
            if not data:
                print('fails to read data.')
                # self._s.close()
                self._packs = ''
                time.sleep(1)
                continue
            self._packs = self._packs + data
            while True:
                #find the pack head flag
                index = self._packs.find(self._pack_head)
                #parse data
                if index >= 0 and len(self._packs[index:]) >= self._pack_size:
                    pack_data = self._packs[index:index + self._pack_size]
                    #radar frame no
                    frame_no = struct.unpack('I',pack_data[4:4 + 4])[0]
                    if frame_no - self._last_fn > 1:
                        print("frame no error,last frame no:{},current frame no:{}".format(self._last_fn,frame_no))
                    self._last_fn = frame_no
                    #timestamp from startup
                    time_sec = struct.unpack('q',pack_data[8:8 + 8])[0]
                    #buff size(no use)
                    buff_size = struct.unpack('H',pack_data[16:16 + 2])[0]
                    #eache frame size,
                    frame_size = struct.unpack('H',pack_data[18:18 + 2])[0]
                    #i channel org signal
                    i = struct.unpack('{}f'.format(int(frame_size/2)),pack_data[20:20 + int(frame_size * 4 / 2)])
                    #q channel org signal
                    q = struct.unpack('{}f'.format(int(frame_size/2)),pack_data[20 + int(frame_size * 4  / 2):20 + frame_size * 4 ])

                    #global data cache queue
                    tmp = np.zeros((int(frame_size/2),2))
                    tmp[:,0] = i
                    tmp[:,1] = q
                    data_queue.put(tmp)
                    # print(data_queue.qsize())

                    self._packs = self._packs[index + self._pack_size:]
                else:
                    break
