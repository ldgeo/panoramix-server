# -*- coding: utf-8 -*-
from flask import Response, send_file
import json
import os
import tempfile

from pxserver.database import Database
from pxserver.utils import draw_map, point_to_list


class PXInfos(object):

    def run(self):
        infos = {}

        infos['total'] = Database.count()
        infos['equirectangular'] = Database.count_equirectangular()
        infos['cube'] = Database.count_cube()
        infos['extent'] = Database.extent()

        resp = Response(json.dumps(infos))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'text/plain'

        return resp


class PXFrustum(object):

    def run(self, args):
        views = Database.views_in_frustum(args['latitude'], args['longitude'],
                                          args['radius'], args['type'])
        infos = {}
        infos['views'] = views

        resp = Response(json.dumps(infos))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'text/plain'

        return resp


class PXMetadata(object):

    def run(self, args):
        infos = {}

        results = Database.from_view(args['view'])
        if not results:
            return None

        res = results[0]
        infos['view'] = res['view']
        infos['exif'] = res['exif']
        infos['type'] = res['type']
        infos['root'] = os.path.dirname(res['filename'])

        if infos['type'] == 'equi':
            infos['files'] = [os.path.basename(res['filename'])]
        else:
            files = []
            for r in results:
                f = os.path.basename(r['filename'])
                files.append(f)
            infos['files'] = files

        pos = point_to_list(Database.position(args['view'])[0])
        infos['position'] = {'longitude': pos[0], 'latitude': pos[1]}

        resp = Response(json.dumps(infos))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'text/plain'

        return resp


class PXMap(object):

    def run(self):
        filename = tempfile.NamedTemporaryFile(delete=False)
        draw_map(filename)
        return send_file(filename, mimetype='image/gif')
