# 3D graph clock
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
import datetime


def set_axis():
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_zlim(z_min, z_max)
    ax.set_title('3D graph clock')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.grid()


def update(f):
    ax.cla()  # Clear ax
    set_axis()
    global zz  # Global variables that changes in this function
    # ax.text(x_min, y_min, z_max * 0.7, "Step=" + str(f))

    # Draw time in text
    dt_now = datetime.datetime.now()
    # ax.text(x_min, 0., z_max * 0.9, dt_now.strftime('%Y.%m.%d %H:%M:%S'), fontsize=16)
    ax.text(x_min, 0., z_max * 1.5, dt_now.strftime('%Y.%m.%d'), fontsize=16, c='gray')
    ax.text(x_min, 0., z_max * 0.9, dt_now.strftime('%H:%M:%S'), fontsize=24)

    # theta for clock hands
    theta_second = - dt_now.second / 60. * 2. * np.pi + np.pi / 2.
    theta_minute = - dt_now.minute / 60. * 2. * np.pi + np.pi / 2.
    theta_hour = - (dt_now.hour % 12) / 12. * 2. * np.pi - np.pi / 6. * dt_now.minute / 60. + np.pi / 2.

    # Draw a second hand and circles
    r_second = 2.
    x_second = r_second * np.cos(theta_second)
    y_second = r_second * np.sin(theta_second)
    second_hand = art3d.Line3D([0, x_second], [0, y_second], [0, 0], color='red', ls="-")
    ax.add_line(second_hand)
    second_circle_c = Circle((0., 0.), 0.1, fc='red')
    ax.add_patch(second_circle_c)
    art3d.pathpatch_2d_to_3d(second_circle_c, z=0, zdir="z")
    second_circle_s = Circle((x_second, y_second), 0.1, fc='red')
    ax.add_patch(second_circle_s)
    art3d.pathpatch_2d_to_3d(second_circle_s, z=0, zdir="z")
    second_circle_l = Circle((0, 0), r_second, ec='red', fill=False)
    ax.add_patch(second_circle_l)
    art3d.pathpatch_2d_to_3d(second_circle_l, z=0, zdir="z")

    # Draw a minute hand and circles
    r_minute = 1.5
    x_minute = r_minute * np.cos(theta_minute)
    y_minute = r_minute * np.sin(theta_minute)
    minute_hand = art3d.Line3D([0, x_minute], [0, y_minute], [0, 0], color='blue', ls="-")
    ax.add_line(minute_hand)
    minute_circle_c = Circle((0., 0.), 0.15, fc='blue')
    ax.add_patch(minute_circle_c)
    art3d.pathpatch_2d_to_3d(minute_circle_c, z=0, zdir="z")
    minute_circle_s = Circle((x_minute, y_minute), 0.15, fc='blue')
    ax.add_patch(minute_circle_s)
    art3d.pathpatch_2d_to_3d(minute_circle_s, z=0, zdir="z")
    minute_circle_l = Circle((0, 0), r_minute, ec='blue', fill=False)
    ax.add_patch(minute_circle_l)
    art3d.pathpatch_2d_to_3d(minute_circle_l, z=0, zdir="z")

    # Draw a minute hand and circles
    r_hour = 1.0
    x_hour = r_hour * np.cos(theta_hour)
    y_hour = r_hour * np.sin(theta_hour)
    hour_hand = art3d.Line3D([0, x_hour], [0, y_hour], [0, 0], color='green', ls="-")
    ax.add_line(hour_hand)
    hour_circle_c = Circle((0., 0.), 0.2, fc='green')
    ax.add_patch(hour_circle_c)
    art3d.pathpatch_2d_to_3d(hour_circle_c, z=0, zdir="z")
    hour_circle_s = Circle((x_hour, y_hour), 0.2, fc='green')
    ax.add_patch(hour_circle_s)
    art3d.pathpatch_2d_to_3d(hour_circle_s, z=0, zdir="z")
    hour_circle_l = Circle((0, 0), r_hour, ec='green', fill=False)
    ax.add_patch(hour_circle_l)
    art3d.pathpatch_2d_to_3d(hour_circle_l, z=0, zdir="z")

    # Draw 12 O'clock mark
    x_mark = [-0.1, 0.1, 0.1, -0.1]
    y_mark = [y_max, y_max, y_max - 0.5, y_max - 0.5]
    z_mark = [0, 0, 0, 0]
    poly = list(zip(x_mark, y_mark, z_mark))
    ax.add_collection3d(art3d.Poly3DCollection([poly], color='gray'))

    # Draw graph
    # Select mode (combination of parameters)
    mode = int(f / change_graph_interval) % 7
    if mode == 0:
        zz = yy
    elif mode == 1:
        zz = np.sin(4. * np.sqrt(xx**2. + yy**2.))
    elif mode == 2:
        sigma = 0.2
        zz = 1 / (2. * np.pi * sigma ** 2.) * np.exp(-(xx**2. + yy**2.)/(2.*sigma**.2)) + z_min
    elif mode == 3:
        sigma = 0.2
        xx_offset = xx - r_hour * np.cos(theta_second)
        yy_offset = yy - r_hour * np.sin(theta_second)
        zz = 1 / (2. * np.pi * sigma ** 2.) * np.exp(-(xx_offset ** 2. + yy_offset ** 2.) / (2. * sigma ** 2.)) + z_min
    elif mode == 4:
        zz = np.sqrt(xx ** 2 + yy ** 2) * np.cos(np.arctan2(yy, xx) - theta_second)
    elif mode == 5:
        zz = np.sin(4 * np.sqrt(xx ** 2 + yy ** 2) * np.cos(np.arctan2(yy, xx) - theta_second))
    elif mode == 6:
        zz = np.sin(4 * np.sqrt(xx ** 2 + yy ** 2) * np.cos(np.arctan2(yy, xx) - theta_second) - 4 * f)
    else:
        zz = yy
    # Plot graph
    ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, cmap=cm.coolwarm, alpha=0.2)


# Global variables
min_max = 2.
x_min = -min_max
x_max = min_max
y_min = -min_max
y_max = min_max
z_min = -4.
z_max = 4

change_graph_interval = 50

# Prepare mesh grid
x = y = np.arange(x_min, x_max, 0.2)
xx, yy = np.meshgrid(x, y)
zz = xx * 0. + yy * 0.

# Generate figure and axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw animation
set_axis()
anim = animation.FuncAnimation(fig, update, interval=50)
plt.show()
