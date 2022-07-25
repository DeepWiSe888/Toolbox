##### Frame Structure

| NO   | field            | data type  | description               |
| ---- | ---------------- | ---------- | ------------------------- |
| 1    | Frame            | uint32_t   | Frame id                  |
| 2    | TimeStamp        | char       | Time stamp  |
| 3    | FPS              | char       | Average last 1 frame FPS  |
| 4    | Pcl_size         | float      | Point cloud size          |
| 5    | endOfFrame       |            | The end of this Frame     |

<img src="https://raw.githubusercontent.com/DeepWiSe888/Toolbox/master/AW-FMCW-EV-602/docs/frameStructure.jpg" width="282" height="211"/>  

##### Point Target Structure 

  
A point cloud is a set of data points in space. The points represent a 3D shape or object. Each point has its set of X, Y and Z coordinates. This structure contains Information on a specific point in a point cloud.
For each point, the following data is provided:
| NO   | field            | data type  | description               |
| ---- | ---------------- | ---------- | ------------------------- |
| 1    | x_m              | float      | x position (in meters)   |
| 2    | y_m              | float      | y position (in meters) |
| 3    | z_m              | float      | z position (in meters)   |
| 4    | intensity        | uint16_t   | The intensity of the point in the point cloud  |
| 5    | id               | uint8_t    | The target ID number - unique for each target  |

<img src="https://raw.githubusercontent.com/DeepWiSe888/Toolbox/master/AW-FMCW-EV-602/docs/pointStructure.jpg" width="270" height="220"/>  

##### Use python environment

1. Install dependent libraries:
    ```python
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
    ```

2. Power on and connect the device to the computer using a network cable.

3. Enter the Lab directory.
   ```shell
   cd  Toolbox\\AW-FMCW-EV-602\\lab\\
   ```
4. Run 'plot_data.py' to plot radar data real time.
    ```shell
    python plot_data.py
    ```
5. Run 'get_data.py' to stored piont cloud.
    ```shell
    python get_data.py
    ```
##### FAQ

1. **What environment should I install**  
    I recommend using the Anaconda virtual environment, where you can easily manage Python versions and software versions.

