# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

""" Compress the json generated by road segmentor """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import numpy as np
import math


epsilon = 2


def dist(p1, p2):
    """
    Calculated euclidean distance bw two points

    :param p1: first point p1
    :param p2: second point p2
    :return: eculidean distance
    """
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def perpendicular_distance(point, p1, p2):
    """
    Calculates perpendicular distance between the point and a line
    segment formed by the points p1 and p2
    :param point: the point lying on the either side of the line segment
    :param p1: point 1 constituting the line segment
    :param p2: point 2 constituting the line segment
    """
    point = [point[0], point[1]]
    p1 = [p1[0], p1[1]]
    p2 = [p2[0], p2[1]]
    if (p1 == p2):
        return dist(point, p1)
    else:
        n = abs((p2[0] - p1[0]) * (p1[1] - point[1]) -
                (p1[0] - point[0]) * (p2[1] - p1[1]))
        d = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        return n / d


def minimize_line_iter(line, eps, mask):
    """
    Iterative version of the Algorithm.
    Recursive version will result in a stack overflow.

    :param line: list containing the list of points(x, y)
            to be minimized
    :param eps: threshold distance between two points
            to be considered as skeleton.
    :param mask: list to identify the points which
            form the skeleton.
    """

    stack = []
    stack.append([0, len(line) - 1])
    while(stack):
        start, end = stack.pop()
        dmax = 0.0
        index = start
        for idx in range(start + 1, end):
            d = perpendicular_distance(line[idx], line[start], line[end])
            if d > dmax:
                dmax = d
                index = idx
        if dmax > eps:
            stack.append((start, index))
            stack.append((index, end))
        mask[start] = 1
        mask[end] = 1


def minimize(points, eps):
    """
    Recursive line minimization algorithm.
    :param line: list containing the list of points(x, y)
            to be minimized
    :param eps: threshold distance between two points
            to be considered as skeleton.
    """
    mask = np.zeros((len(points)), dtype=np.uint8)
    minimize_line_iter(points, eps, mask)
    return [points[idx] for idx, ival in enumerate(mask) if mask[idx] > 0]


def main(name2road_js):
    """
    :param name2road_js: json that contains name to road info
    :return: compressed json of name to road info
    """
    roads = name2road_js
    newroads = {}
    for i in roads:
        road = roads[i]
        newroads[i] = minimize(road, epsilon)
    return newroads
