import os
import sys
import time
import threading
import numpy as np
import scipy.io as sio


from data_collect import SerialCollect
from data_cache import  data_queue
from utils import *


def plot():
    print("start plot")
    frecv = True
    datas = None
    while True:
        if data_queue.empty():
            time.sleep(0.01)
            continue
        else:
            # print("queue size:{}".format(data_queue.qsize()))
            data = data_queue.get()
            data = data.reshape(1,-1,2)
            if frecv:
                datas = data
                frecv = False
            else:
                datas = np.vstack((datas,data))
            datas_len = datas.shape[0]
            
            if(datas_len >= FRAMES):
                iq = datas[-FRAMES:,:,:]

                org = iq[:,OFFSET:,0]+1j*iq[:,OFFSET:,1]
                x = org[:,:]

                file_name = time.strftime("%Y%m%d_%H%M%S.mat",time.localtime())
                sio.savemat('./{}/{}'.format('datas',file_name),{'data':x})
                #step = FPS
                datas = datas[STEP:,:,:]
                      
    return


def main():
    recv = SerialCollect("COM6")
    if not recv.state:
        print('serial init error.')
        exit(0)

    collect = threading.Thread(target=recv.recv)
    collect.setDaemon(True)
    collect.start()
    plot()


if __name__ == '__main__':
    main()