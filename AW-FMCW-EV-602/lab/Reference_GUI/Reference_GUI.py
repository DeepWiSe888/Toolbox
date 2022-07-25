import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Reference_GUI.utils as utils


def main(args):
    f = utils.monitor(args)

    def update(_):
        # nonlocal txt
        # nonlocal fig
        last_pcl = 0
        pcl_size, trk_size = 0, 0
        pcl_data = np.empty((0, 4), int)
        trk_data = np.empty((0, 4), int)
        mid_x = (args.arena[0] + args.arena[0]) / 2
        for line in f:
            line = line.decode()
            if r'Pcl_size:' in line:  # size of point cloud
                pcl_size = int(re.findall(r'Pcl_size: (\d+)', line)[0])
                continue

            if r'pcl#=' in line:
                # Checks if the printed point target matches to point target pattern
                if utils.pattern.match(line):
                    pcl_data, last_pcl = utils.handle_pcl_or_trk(line, 't_id', pcl_data)
                    continue
                continue

            if r'Targets:' in line:  # size of tracker
                trk_size = int(re.findall(r'Targets: (\d+)', line)[0])
                continue

            if r't_id=' in line:
                trk_data = utils.handle_pcl_or_trk(line, 't_id', trk_data)[0]
                continue



            if r'endOfFrame' in line:
                utils.scatter(ax3d, "sc_pcl", pcl_data)
                utils.scatter(ax2d, "sc_pcl", pcl_data)
                utils.scatter(ax3d, "sc_trk", trk_data)
                utils.scatter(ax2d, "sc_trk", trk_data)
                if falling['enabled']:
                    utils.falling_alarm(falling, fig)
                break

    fig = plt.figure()
    # Creating 2 dictionaries, each represents a different subplot: 2D and 3D
    ax3d = {}
    ax2d = {}
    falling = {'text': fig.text(0.5, 0.1, ""), 'enabled': False, 'line': ""}

    # iterating the dicts to assign relevant attributes to the subplots
    utils.init_ax(fig, ax3d, '3d', args)
    utils.init_ax(fig, ax2d, '2d', args)

    # Initial fixed text; Saved in a variable to be updated in the animation
    # Placement 0, 0 would be the bottom left, 1, 1 would be the top right.
    txt = ax3d["subplot"].text2D(0, 1, "", transform=ax3d["subplot"].transAxes)
    plt.grid()

    _ = animation.FuncAnimation(fig, update, interval=0)
    plt.tight_layout()
    plt.show()
