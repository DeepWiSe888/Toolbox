import time
import re
import numpy as np

import serial.tools.list_ports
import serial
import io


colors = {0.0: 'lightcoral', 1.0: 'lightseagreen', 2.0: 'palegreen', 3.0: 'powderblue', 4.0: 'gold',
          5.0: 'plum', 6.0: 'orchid', 7.0: 'crimson', 8.0: 'cyan', 255.0: 'lightsalmon'}

pattern = re.compile("^pcl#=[0-9]+\st_id=[0-9]+\sx=[+-]?\d+\.\d+\sy=[+-]?\d+\.\d+\sz=[+-]?\d+\.\d+[\r\n]+$")


class SocketIO(io.RawIOBase):
    def __init__(self, sock):
        self.sock = sock

    def get_sock(self):
        return self.sock

    def read(self, sz=-1):
        if (sz == -1): sz = 0x7FFFFFFF
        return self.sock.recv(sz)

    def seekable(self):
        return False


def init_ax(fig, ax, dim, my_args):
    ax["dim"] = dim
    # The Axes object (subplot)
    ax["subplot"] = fig.add_subplot(121 if dim == '3d' else 122, projection='3d' if dim == '3d' else 'rectilinear')
    # initial scattering; saved in the dict in order to be updated in the animation:
    ax["sc_pcl"] = ax["subplot"].scatter([], [], [], c='darkblue', alpha=0.5)
    ax["sc_trk"] = ax["subplot"].scatter([], [], [], c='darkblue', alpha=0.5)
    ax["subplot"].set_xlabel('X')
    ax["subplot"].set_ylabel('Y')
    ax["subplot"].set_xlim(*my_args.arena[-5::-1])
    ax["subplot"].set_ylim(*my_args.arena[-3:-5:-1])
    if dim == '3d':
        ax["subplot"].set_zlabel('Z')
        ax["subplot"].set_zlim(*my_args.arena[4:])


def monitor(my_args):

    file = get_serial()  # run live (UART)
    time.sleep(3)
 
    return file


def handle_pcl_or_trk(line, id_indicator, data):
    id = np.asarray(re.findall(fr'{id_indicator}=(\d+)', line)[0], dtype=np.int32)  # finds target id in tracker line
    xyz = np.asarray(re.findall(r"[+-]?\d+\.\d+", line), dtype=np.float)  # finds target xyz in tracker line
    pcl_id = re.findall(r'pcl#=(\d+)', line)
    temp_append = np.append(id, xyz)
    data = np.append(data, [temp_append], axis=0)
    last_pcl = int(pcl_id[0]) if r'LAST' in line else 0
    return data, last_pcl


def scatter(ax, scatter_name, data):
    ax[scatter_name].remove()
    clr = [colors[i] for i in data[:, 0]] if scatter_name == "sc_pcl" else 'red'
    size = 50 if scatter_name == "sc_pcl" else 100
    if ax["dim"] == '3d':
        ax[scatter_name] = ax["subplot"].scatter(data[:, 1], data[:, 2], data[:, 3], c=clr, s=size)
        
    else:
        ax[scatter_name] = ax["subplot"].scatter(data[:, 1], data[:, 2], c=clr, s=size)
    





def get_com_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB Serial Port' in p.description:
            com = re.findall(r'COM\d+', p.description)
            return com[0]


def get_serial():  # get serial com port
    baud_rate = 921600
    com_port = get_com_port()  # set the correct port before run it
    z1serial = serial.Serial(port=com_port, baudrate=baud_rate)
    z1serial.timeout = 2  # set read timeout
    return z1serial
