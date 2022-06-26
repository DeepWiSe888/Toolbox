import queue
import socket

from libs.conf import *
from libs.utils import *

Cache = queue.Queue()

class Receive(object):
    def __init__(self,
                local_udp_ip = "192.168.0.3",local_udp_port = 8080):
        
        # udp 
        self.local_udp_ip = local_udp_ip
        self.local_udp_port = local_udp_port
        # receive data buffer
        self.recv_buffer = bytes()
        # last frame no
        self.last_fn = 0

    def setting(self):
        msg = ""
        result = 0
        self.local_upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.local_upd_socket.bind((self.local_udp_ip, self.local_udp_port))
        except:
            self.local_upd_socket.close()
            msg = "upd binding error"
            result = -1
        return msg,result

    def recv_data(self):
        while True:
            try:
                data, remote_address = self.local_upd_socket.recvfrom(4096)
                if not data:
                    print('disconnect')
                    self.local_upd_socket.close()
                    self.recv_buffer = bytes()
                    break
                Cache.put({'data':{},'byte':data})
            except Exception as e:
                print(e)

    def __exit__(self):
        self.local_upd_socket.close()