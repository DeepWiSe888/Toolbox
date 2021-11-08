
from data_collect import SerialCollect


def main():
    recv = SerialCollect("COM3")
    if not recv.state:
        print('serial init error.')
        exit(0)
    recv.recv()

if __name__ == '__main__':
    main()