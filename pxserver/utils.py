#! /usr/bin/env python
# -*- coding: utf-8 -*-

from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from pxserver.database import Database


def box_to_list(box_str):
    '''
    Convert BOX(x0 y0,x1 y1) to [x0, y0, x1, y1]
    '''
    box_str = box_str.replace('BOX(', '')
    box_str = box_str.replace(')', '')
    box_str = box_str.replace(',', ' ')
    l = box_str.split(' ')
    return [float(i) for i in l]


def point_to_list(pnt_str):
    '''
    Convert POINT(x y) to [x, y]
    '''
    pnt_str = pnt_str.replace('POINT(', '')
    pnt_str = pnt_str.replace(')', '')
    l = pnt_str.split(' ')
    return [float(i) for i in l]


def draw_map(output, view=None, radius=None):
    # get extent and positions from database
    if not view or not radius:
        ext = box_to_list(Database.extent())
        pos = Database.positions()
    else:
        viewpos = point_to_list(Database.position(view)[0]['st_astext'])
        viewsid = Database.views_in_frustum(viewpos[1], viewpos[0], radius)
        ext = Database.radius_extent(viewpos[1], viewpos[0], radius)
        ext = box_to_list(ext)

        pos = []
        for id in viewsid:
            pos.append(Database.position(id)[0])

    # init map
    map = Basemap(projection='merc',
                  resolution='h', area_thresh=0.1,
                  llcrnrlon=ext[0], llcrnrlat=ext[1],
                  urcrnrlon=ext[2], urcrnrlat=ext[3])

    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='white')
    map.drawmapboundary()

    # init plot
    fig = plt.figure()

    # draw trajectory
    ax1 = fig.add_subplot(131)
    ax1.set_title('Trajectory')
    for p in pos:
        lng, lat = point_to_list(p['st_astext'])
        x, y = map(lng, lat)
        map.plot(x, y, 'bo', markersize=1)

    # draw cube
    ax2 = fig.add_subplot(132)
    ax2.set_title('Cube views')
    for p in pos:
        lng, lat = point_to_list(p['st_astext'])
        x, y = map(lng, lat)

        if p['type'] == 'cube':
            map.plot(x, y, 'bo', markersize=1)
            plt.text(x, y, p['view'], fontsize=6, color='b')

    # draw equirectangular
    ax3 = fig.add_subplot(133)
    ax3.set_title('Equirectangular views')
    for p in pos:
        lng, lat = point_to_list(p['st_astext'])
        x, y = map(lng, lat)

        if p['type'] == 'equi':
            map.plot(x, y, 'bo', markersize=1)
            plt.text(x, y, p['view'], fontsize=6, color='b')

    # show map
    plt.savefig(output)
