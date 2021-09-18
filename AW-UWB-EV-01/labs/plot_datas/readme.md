##### Command

Command format:AT+command value,vlaue/r/n，command and values are directly whitespace.

| AT       | send                | return:OK    | return:ERROR     | description              |
| -------- | ------------------- | ------------ | ---------------- | ------------------------ |
| AT+DIST  | AT+DIST 0.2,5.0/r/n | DIST:OK/r/n  | DIST:ERROR*/r/n  | Set the radar scan range |
| AT+FPS   | AT+FPS 40/r/n       | FPS:OK/r/n   | FPS:ERROR*/r/n   | Set the radar fps        |
| AT+START | AT+START/r/n        | START:OK/r/n | START:ERROR*/r/n | Start receiving data     |
| AT+STOP  | AT+STOP/r/n         | STOP:OK/r/n  | STOP:ERROR*/r/n  | Stop receiving data      |

##### Packet Parsing

Each frame contains 820 bytes, and each field is sequentially concatenated  

| NO   | field            | data type        | data type size    | packet size | value            | description                                        |
| ---- | ---------------- | ---------------- | ----------------- | ----------- | ---------------- | -------------------------------------------------- |
| 1    | head flag        |                  | 4                 | 4           | 0xe90xcf0x930x72 | data packet head flag                              |
| 2    | frame no         | unsignedintlong  | 4                 | 8           |                  | frame number after radar start                     |
| 3    | timestamp        | unsignedlonglong | 8                 | 16          |                  | the timestamp from device boot to present          |
| 4    | buffer size      | unsignedshortint | 2                 | 18          |                  |                                                    |
| 5    | frame size       | unsignedshorint  | 2                 | 20          |                  | each frame size                                    |
| 6    | I channal signal | float            | frame_size / 2 *4 | ≤420        |                  | frame size <=200                                   |
| 7    | Q channal signal | float            | frame_size / 2 *4 | ≤820        |                  | the Q channal signal follows the I channal  signal |

##### Use python environment

1. Install dependent libraries:
    ```python
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
    ```
2. Run plot data program in terminal:
    ```
    python plot_data.py
    ```
3. Run save data program in terminal:
    ```
    python record_data.pys
    ```
##### Use conda virtual environment
1. install anaconda and update conda
    ```
    #install anaconda

    #update conda
    conda update conda
    ```
2. creat python environment
    ```
    conda create -n py39 python=3.9
    ``` 
3. activate env
    ```
    #linux
    source activate py39

    #windows
    activate py39
    ```
4. install libs
    ```
    # requirements.txt,
    # the installation package version is automatically selected
    numpy
    scipy
    pyqtgraph
    pyserial
    PyOpenGL
    spyder
    PyQt5

    #install 
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

    ```
5. run
    ```
    # change the serial port name and plot data
    python plot_data.py

    # record data
    python record_data.py
    ```
##### Tested Environment(s)
1. Python:3.7.9
    ```
    1. Python version:3.7.9
    2. PyQtGraph version:0.12.2
    3. PyQt5 version:5.15.4
    4. NumPy version:1.19.5
    5. Scipy version:1.5.2
    6. PyOpenGl version:3.1.5
    7. Spyder version:5.1.1
    8. PySerial version:3.5
    ```
2. Python:3.9.6
    ```
    1. Python version:3.9.6
    2. PyQtGraph version:0.12.2
    3. PyQt5 version:5.12.3
    4. NumPy version:1.21.2
    5. Scipy version:1.7.1
    6. PyOpenGl version:3.1.5
    7. Spyder version:5.1.1
    8. PySerial version:3.5
    ```
##### Config
1. Changing the serial name in the main function.
    ```
    def main():
        recv = SerialCollect("COM6")
        if not recv.state:
            print('serial init error.')
            exit(0)

        collect = threading.Thread(target=recv.recv)
        collect.setDaemon(True)
        collect.start()
        plot()
        #....
    ```
2. Modifying configuration Items in the './config.ini'
    1. Modify sampling rate,supports a maximum of 800Hz,the datatype is int.
        ```
        [radar]
        fps  = 40
        ```
    2. Modify scan area,from range start to range end,the datatype is float and one decimal digit is reserved.
        ```
        [radar]
        range_start = 0.2
        range_end  = 5.0
        ```
    3. Modify the calculation step length,the default value is 1s and same as the sampling rate.
        ```
        [alg]
        step = 40
        ```
    4. Modify the bin offset,the default value is 0.
        ```
        [alg]
        bin_offset = 0
        ```

##### FAQ

1. **How do I know the serial port name**
    ```
    1. windows:"Control Panel" -> "Device Manager" -> "COM And LPT",and you will see the port name such as "COM1",then change the port name in the code.
    2. mac:open the Terminal and run the script"ls /dev/tty.*",and you will see the port name such as "/dev/tty.usbmodem1431",then change the port name in the code.
    3. ubuntu:open the Terminal and run the script"ls /dev/ttyUSB*",and you will see the port name such as "/dev/ttyUSB1",then change the port name in the code.
    ```
2. **What environment should I install**
    I recommend using the Anaconda virtual environment, where you can easily manage Python versions and software versions.
