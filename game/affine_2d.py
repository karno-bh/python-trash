from flat_matrix import FlatMatrix
from math import sin, cos


def identical():
    data = [
        1., 0., 0.,
        0., 1., 0.,
        0., 0., 1.,
    ]
    return FlatMatrix(3, 3, new_state=data)


def translate(x, y):
    data = [
        1., 0.,  x,
        0., 1.,  y,
        0., 0., 1.,
    ]
    return FlatMatrix(3, 3, new_state=data)


def scale(w, h):
    data = [
         w, 0., 0.,
        0.,  h, 0.,
        0., 0., 1.,
    ]
    return FlatMatrix(3, 3, new_state=data)


def rotate(theta):
    data = [
        cos(theta), -sin(theta), 0,
        sin(theta),  cos(theta), 0,
                 0,           0, 1,
    ]
    return FlatMatrix(3, 3, new_state=data)


def point(x, y):
    return [x, y, 1]


__all__ = ['identical', 'translate', 'scale', 'rotate', 'point']