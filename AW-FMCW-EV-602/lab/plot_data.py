import numpy as np
import re
import logging
import subprocess   
import time
import os
import Reference_GUI.Reference_GUI as RefGUI

import Reference_GUI.utils as utils


class Args:
    def __init__(self, gui, arena, path):
        self.gui = gui
        self.arena = arena

        self.path = path


def get_config():
    with open(f"{os.getcwd()}\\Config.txt", 'r') as file:
        for line in file:
            if r'V_ENABLE_GUI=' in line:
                gui = int(re.findall(r'V_ENABLE_GUI=(\d+)', line)[0])
            if r'LOG_PATH=' in line:
                log_path = re.findall(r'LOG_PATH="(.*?)"', line)[0]
            if r'ARENA=' in line:
                arena = (re.findall(r'ARENA=\"(.*?)\"', line)[0]).split(", ")
                for i in range(len(arena)):
                    arena[i] = float(arena[i])
                arena = np.asarray(arena, dtype=np.float64)
            
    # Deal with wrong main configuration

    args = Args(gui, arena, log_path)
    
    return args


def main():

    args = get_config()


    RefGUI.main(args)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
