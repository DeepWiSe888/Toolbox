##### Packet Parsing

Each frame contains 1124 bytes, and each field is sequentially concatenated  

| NO   | field            | data type | data type size | packet size | value | description               |
| ---- | ---------------- | --------- | -------------- | ----------- | ----- | ------------------------- |
| 1    | sec              | int       | 4              | 4           |       | integral oart of second   |
| 2    | usec             | int       | 4              | 4           |       | fractional part of second |
| 3    | tx no            | int       | 4              | 4           |       | tx antenna no default 1   |
| 4    | rx no            | int       | 4              | 4           |       | rx antenna no default 1   |
| 5    | frame no         | int       | 4              | 4           |       | frame no                  |
| 6    | I channel signal | float     | 4              | 138 * 4     |       | i data                    |
| 7    | Q channel signal | float     | 4              | 138 * 4     |       | q data                    |

##### Use python environment

1. Install dependent libraries:
    ```python
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
    ```

2. Power on and connect the device to the computer using a network cable.

3. Change the IP address of the network adapter to 192.168.0.3 

4. Run the udp receiving tool from '../../tools/receive_tools.exe',and will save the radar data to local.

5. Modifying the radar data path,folder  can only store dataset with the suffix txt.

    ```python
    path = "./datas/"
    range_data = read_data(path)
    (frame_cnt,bin_cnt) = range_data.shape
    ```

6. Run plot data program in terminal:

    ```
    python plot_data_from_file.py
    ```

7. You can down-sampling the data:

    ```python
    # By default,raw data fps is 2042
    RAW_FPS = 2042
    
    # The fps after sampling, FPS < RAW_FPS
    FPS = 100
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
    PyOpenGL
    spyder
    PyQt5
    
    #install 
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
    ```
5. Run same as the python environment.
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
    ```



##### FAQ

1. **What environment should I install**  
    I recommend using the Anaconda virtual environment, where you can easily manage Python versions and software versions.
2. **About Radar init fail**

    if radar init fail，you can restar the tools.

3. **About the frame number of first frame**

   the first frame number is abnormal due to data loss.
