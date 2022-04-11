import numpy as np
import keyboard as kb
from tkinter import Tk
import matplotlib as mpl
import matplotlib.pyplot as plt


def refresh_plot(x, y):
    for current_point in current_points:
        current_point.remove()
    current_points.clear()

    plt.xlim(x - 500, x + 500)
    plt.ylim(y - 500, y + 500)

    current_points.append(plt.Circle((x, y), 10, color='#65fda0', fill=True))

    for current_point in current_points:
        ax.add_patch(current_point)
    fig.canvas.draw()
    fig.canvas.flush_events()


def get_blind_info():
    clipboard = Tk().clipboard_get()
    split = clipboard.split(' ')
    coords = split[6:9]
    x = float(coords[0])
    z = float(coords[2])
    refresh_plot(x, z)

    angle = np.arctan2(z, x)

    rings = [[160, 352], [544, 736], [928, 1120], [1312, 1504], [1696, 1888], [2080, 2272], [2464, 2656], [2848, 3040]]
    dist = np.sqrt(x**2 + z**2)

    for i in range(len(rings)):
        if rings[i][0] < dist < rings[i][1]:
            center = (rings[i][0] + rings[i][1]) / 2
            x = center * np.cos(angle)
            z = center * np.sin(angle)
            x = int(round(x))
            z = int(round(z))

            if dist < center:
                to_angle = np.rad2deg(angle)
            else:
                to_angle = np.rad2deg(angle) + 180
            to_angle = to_mc_angle(to_angle)

            print('You are in the ring.\nNearest coordinates in center of the ring: ' + str(x) + ' ' + str(z)
                  + '\nAngle: ' + str(to_angle))
            return

    ring_dist = []
    for i in range(len(rings)):
        ring_dist.append(rings[i][0] - dist if dist < rings[i][0] else rings[i][1] - dist)
    ring = ring_dist.index(min(ring_dist))

    dist_to_go = rings[ring][0] if rings[ring][0] > dist else rings[ring][1]
    nearest_x = dist_to_go * np.cos(angle)
    nearest_z = dist_to_go * np.sin(angle)
    nearest_x = int(round(nearest_x))
    nearest_z = int(round(nearest_z))

    center = (rings[ring][0] + rings[ring][1]) / 2
    center_x = center * np.cos(angle)
    center_z = center * np.sin(angle)
    center_x = int(round(center_x))
    center_z = int(round(center_z))

    if dist < center:
        to_angle = np.rad2deg(angle)
    else:
        to_angle = np.rad2deg(angle) + 180
    to_angle = to_mc_angle(to_angle)

    print('You are not in the ring.\nNearest coordinates in ring ' + str(nearest_x) + ' ' + str(nearest_z)
          + '\nNearest coordinates in center of ring ' + str(center_x) + ' ' + str(center_z)
          + '\nAngle: ' + str(to_angle))


def to_mc_angle(angle):
    angle = angle - 90
    if angle > 180:
        angle = angle - 360
    return int(round(angle))


if __name__ == "__main__":
    current_points = []
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure(figsize=(5, 5))
    fig.patch.set_facecolor('#080b14')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    circles = []
    rings = [160, 352, 544, 736, 928, 1120, 1312, 1504, 1696, 1888, 2080, 2272, 2464, 2656, 2848, 3040]
    rings.reverse()

    for i in range(len(rings)):
        if i % 2 == 0:
            circles.append(plt.Circle((0, 0), rings[i], color='#DF3833', fill=True))
        else:
            circles.append(plt.Circle((0, 0), rings[i], color='#080b14', fill=True))

    for circle in circles:
        ax.add_patch(circle)

    kb.add_hotkey('f3+c', get_blind_info)

    plt.show()
