import os
import time
import numpy as np

import threading
from pyqtgraph.Qt import QtGui, QtWidgets
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from libs.recv import *
from libs.conf import *
from libs.utils import *


def main():
    filename = './datas/{}.dat'.format(int(round(time.time() * 1000)))
    fid = open(filename,'ab+')
    s = SerialCollect(port='COM3')
    recv_thd = threading.Thread(target=s.recv_data)
    recv_thd.setDaemon(True)
    recv_thd.start()
    last_fn = 0
    try:
        while True:
            if Cache.empty():
                time.sleep(0.001)
                continue
            else:
                pack_dict = Cache.get()
                raw_data = pack_dict['byte']
                
                timestamp = pack_dict['t']
                frame_no = pack_dict['fno']
                tx_antenna_no = pack_dict['tx']
                rx_antenna_no = pack_dict['rx']
                if frame_no - last_fn != 1:
                    print(timestamp,tx_antenna_no,rx_antenna_no,frame_no,last_fn,frame_no - last_fn)
                last_fn = frame_no

                fid.write(raw_data)
    except KeyboardInterrupt:
        fid.flush()
        fid.close()
            

if __name__ == '__main__':
    main()