##### Packet Parsing

Each frame contains 1124 bytes, and each field is sequentially concatenated  

| NO   | field    | data type | data type size | packet size                                                  | value | description               |
| ---- | -------- | --------- | -------------- | ------------------------------------------------------------ | ----- | ------------------------- |
| 1    | flage    |           |                |                                                              |       |                           |
| 2    | sec      | long      | 8              | 8                                                            |       | integral oart of second   |
| 3    | usec     | long      | 8              | 8                                                            |       | fractional part of second |
| 4    | rx no    | int       | 4              | 4                                                            |       | rx antenna no default 1   |
| 5    | tx no    | int       | 4              | 4                                                            |       | tx antenna no default 1   |
| 6    | frame no | int       | 4              | 4                                                            |       | frame no                  |
| 7    | adc      | float     | 4              | num_tx * num_rx * num_chirps_per_frame * num_samples_per_chirp * 4 |       | adc data                  |

##### Use python environment

1. Install dependent libraries:
    ```python
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
    ```

2. Power on and connect the device to the computer using a network cable.

3. Change the serial name in the main function

5. Run 'plot_data.py' to plot radar data real time.

    ```python
    python plot_data.py
    ```

6. Run 'receiving_data_and_save.py' to save radar data.

    ```python
    python receiving_data_and_save.py
    ```

7. Modifying the radar data path,folder  can only store dataset with the suffix dat.

    ```python
    path = "./datas/"
    range_data = read_data(path)
    (frame_cnt,rx_cnt,bin_cnt) = range_data.shape
    ```

8. Run plot local data program in terminal:

    ```
    python plot_data_from_file.py
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

4. **About loss data**

   the unstable cpu may cause udp packet loss.
