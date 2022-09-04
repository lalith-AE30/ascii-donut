from math import cos, pi, sin
import os
import time
import numpy as np


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


"""
        z
        |    y
        |   /
        |  /
        | /
        |/____________ x
       
"""

mean_major_radius = 10
minor_radius = 4


def get_shape_point(theta, phi):
    return (
        (minor_radius*cos(theta)+mean_major_radius)*cos(phi),
        (minor_radius*cos(theta)+mean_major_radius)*sin(phi),
        minor_radius*sin(theta)
    )


def get_shape_normal(theta, phi):
    return (
        cos(theta)*cos(phi),
        cos(theta)*sin(phi),
        sin(theta)
    )


def shade(level):
    if level < 0.1:
        return ' '
    if level < 0.2:
        return '.'
    if level < 0.3:
        return ':'
    if level < 0.4:
        return '-'
    if level < 0.5:
        return '='
    if level < 0.6:
        return '+'
    if level < 0.7:
        return '*'
    if level < 0.8:
        return '#'
    if level < 0.9:
        return '%'
    return '@'


size = 60


def sample(theta_sample, phi_sample, light, img, img_d):
    phi = phi_sample/phi_samples*2*pi
    theta = theta_sample/theta_samples*2*pi
    pos = get_shape_point(theta, phi)
    normal = get_shape_normal(theta, phi)

    cosx = cos(x_rot)
    sinx = sin(x_rot)
    cosz = cos(z_rot)
    sinz = sin(z_rot)

    pos = (
        pos[0],
        cosx*(pos[1])-sinx*(pos[2]),
        sinx*(pos[1])+cosx*(pos[2])
    )

    pos = (
        cosz*pos[0]-sinz*pos[1],
        sinz*pos[0]+cosz*pos[1],
        pos[2]
    )

    normal = (
        normal[0],
        cosx*(normal[1])-sinx*(normal[2]),
        sinx*(normal[1])+cosx*(normal[2])
    )

    normal = (
        cosz*normal[0]-sinz*normal[1],
        sinz*normal[0]+cosz*normal[1],
        normal[2]
    )

    z_idx = int(size/2+pos[2])
    x_idx = int(size/2+pos[0])
    level = light[0]*normal[0]+light[1]*normal[1]+light[2]*normal[2]
    if pos[1] <= img_d[z_idx][x_idx]:
        img_d[z_idx][x_idx] = pos[1]

        img[z_idx][x_idx] = level


theta_samples = 15
phi_samples = 60
x_rot = 0
z_rot = 0
light = (
    1/3**0.5,
    -1/3**0.5,
    1/3**0.5,
)
if __name__ == '__main__':
    while True:
        t1 = time.perf_counter()
        img = np.zeros((size, size))
        img_d = np.full((size, size), size)
        x_rot += pi/60*2
        x_rot %= 2*pi
        z_rot += pi/60*2
        z_rot %= 2*pi

        for phi_sample in range(phi_samples):
            for theta_sample in range(theta_samples):
                sample(theta_sample, phi_sample, light, img, img_d)

        s = ''
        for line in img:
            for c in line:
                s += shade(c)
            s += '\n'
        clear()
        print(s)

        t2 = time.perf_counter()
        print(1/(t2-t1))
