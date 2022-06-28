import os
import time
import struct
import socket
import threading
import numpy as np
from queue import Queue

from pyqtgraph.Qt import QtGui, QtWidgets
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from libs.recv import Receive,Cache
from libs.conf import *
from libs.utils import *

           
def main():
    global curve1,curve2,curve3,curve4,curve5,curve6

    # Set graphical window, its title and size
    win = pg.GraphicsLayoutWidget(show=True)
    win.resize(1500,600)
    win.setWindowTitle('plot radar data')
    win.setBackground("w")

    pg.setConfigOptions(antialias=True)

    colorMap = pg.colormap.get("CET-D1")
    range_ticks = [i for i in range(MAX_BIN - OFFSET + 1) if i % 10 == 0]
    time_ticks = [i for i in range(FRAMES + 1) if i % FPS == 0]

    p1 = win.addPlot(title="range bin")
    curve1 = p1.plot(pen='r')
    p1.setLabels(left='amplitude', bottom='range(m)')
    ax1 = p1.getAxis('bottom')
    ax1.setTicks([[(v, '{:.2f}'.format((v + OFFSET) * RANGE_RESOLUTION + RANGE_SATRT)) for v in range_ticks]])

    p2 = win.addPlot(title="max bin iq")
    curve2 = p2.plot(pen='g')
    p2.setLabels(bottom='i',left='q')

    p3 = win.addPlot(title="max bin time series")
    curve3 = p3.plot(pen='b')
    p3.setLabels(left='amplitude',bottom='time(s)')
    ax3 = p3.getAxis('bottom')
    ax3.setTicks([[(v, '{}'.format(int(v / FPS) )) for v in time_ticks]])


    win.nextRow()
    p4 = win.addPlot(title='time-range')
    curve4 = pg.ImageItem()
    p4.addItem(curve4)
    p4.setLabels(left='time(s)',bottom='range(m)')
    bar4 = pg.ColorBarItem( values=(0,1), colorMap=colorMap) 
    bar4.setImageItem(curve4)  
    ax4 = p4.getAxis('bottom')
    ax4.setTicks([[(v, '{:.2f}'.format((v + OFFSET) * RANGE_RESOLUTION + RANGE_SATRT)) for v in range_ticks]]) 
    ax4 = p4.getAxis('left')
    ax4.setTicks([[(v, '{}'.format(int(v / FPS) )) for v in time_ticks]])

    p5 = win.addPlot(title='time-range remove the background')
    curve5 = pg.ImageItem()
    p5.addItem(curve5)
    p5.setLabels(left='time(s)',bottom='range(m)')
    bar5 = pg.ColorBarItem( values=(0,1), colorMap=colorMap) 
    bar5.setImageItem(curve5) 
    ax5 = p5.getAxis('bottom')
    ax5.setTicks([[(v, '{:.2f}'.format((v + OFFSET) * RANGE_RESOLUTION + RANGE_SATRT)) for v in range_ticks]]) 
    ax5 = p5.getAxis('left')
    ax5.setTicks([[(v, '{}'.format(int(v / FPS) )) for v in time_ticks]])

    p6 = win.addPlot(title='range-doppler')
    curve6 = pg.ImageItem()
    p6.addItem(curve6)
    p6.setLabels(left='doppler(Hz)',bottom='range(m)')
    bar6 = pg.ColorBarItem(values=(0,1), colorMap=colorMap) 
    bar6.setImageItem(curve6)  
    ax6 = p6.getAxis('bottom')
    ax6.setTicks([[(v, '{:.2f}'.format((v + OFFSET) * RANGE_RESOLUTION + RANGE_SATRT)) for v in range_ticks]])
    ax6 = p6.getAxis('left')
    freq_ticks = [i for i in range(NFFT + 1) if i % FPS == 0]
    ax6.setTicks([[(v, '{}'.format(int((v - NFFT / 2) * FPS / NFFT)) ) for v in freq_ticks]])

    local_udp_ip = "192.168.0.3"
    local_udp_port = 8080
    
    r = Receive(local_udp_ip,local_udp_port)
    msg,result = r.setting()
    if result < 0:
        print(msg)
        exit(0)

    recv_thd = threading.Thread(target=r.recv_data)
    recv_thd.setDaemon(True)
    recv_thd.start()

    last_fn = 0
    recv_buffer = bytes()
    framelist = []
    
    pack_size = 0
    try:
        while True:
            if Cache.empty():
                time.sleep(0.001)
                continue
            else:
                cache_pack = Cache.get()
                data = cache_pack['byte']
                recv_buffer = recv_buffer + data
                while True:
                    start_index = recv_buffer.find(flag)
                    if(start_index == -1):
                        break
                    end_index = recv_buffer.find(flag,start_index+flag_size)
                    if(end_index == -1):
                        break
                    pack = recv_buffer[start_index:end_index]
                    pack_dict = parse_pack(pack)
                    timestamp = pack_dict['t']
                    frame_no = pack_dict['fno']
                    tx_antenna_no = pack_dict['tx']
                    rx_antenna_no = pack_dict['rx']
                    if frame_no - last_fn != 1:
                        print(timestamp,tx_antenna_no,rx_antenna_no,frame_no,last_fn,frame_no - last_fn)
                    last_fn = frame_no
                    recv_buffer = recv_buffer[end_index:]
                    
                    #plot data
                    framelist.append(pack_dict['iq'])
                    
                    if len(framelist) >= SEC * RAW_FPS:
                        frames = np.array(framelist)
                        frames = downsampling(frames)
                        x = frames[:,OFFSET:MAX_BIN]
                        #remove the background
                        iq_data = x - np.mean(x,0)
                        iq_abs = np.abs(iq_data)
                        iq_bin_sum = np.sum(iq_abs,0)

                        #determine the target bin
                        iq_bin = np.mean(np.abs(iq_data),0)
                        bin_offset = 0
                        bin_idx = np.where(np.max(iq_bin[bin_offset:]) <= iq_bin[bin_offset:])[0][0]
                        bin_idx += bin_offset
                        org_wave = iq_data[:,bin_idx]

                        #fft
                        fft_data = np.fft.fft(iq_data,n = NFFT,axis=0)
                        fft_shift_data = np.fft.fftshift(fft_data,axes=0)
                        fft_abs = np.abs(fft_shift_data)

                        #update plot data
                        curve1.setData(iq_bin_sum)
                        curve2.setData(org_wave.real,org_wave.imag)
                        curve3.setData(iq_abs[:,bin_idx])
                        curve4.setImage(np.abs(x).T)
                        curve5.setImage(iq_abs.T)
                        curve6.setImage(fft_abs.T)

                        #update plot immediate
                        QtWidgets.QApplication.processEvents()
                        
                        framelist = framelist[1*RAW_FPS:]

    except KeyboardInterrupt:
        pass
            

if __name__ == '__main__':
    main()