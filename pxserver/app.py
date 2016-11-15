# -*- coding: utf-8 -*-
from flask_restplus import Api, Resource as OrigResource, reqparse

from pxserver.database import pgexceptions
from pxserver import px


class Resource(OrigResource):
    # add a postgresql exception decorator for all api methods
    method_decorators = [pgexceptions]


api = Api(
    version='0.1', title='Panoramix Server',
    description='API for accessing metadatas panoramics images',
    validate=True
)

# -----------------------------------------------------------------------------
# basic api
# -----------------------------------------------------------------------------
infos_ns = api.namespace('infos/',
                         description='Information about panoramix-server')


@infos_ns.route("/global")
class InfosGlobal(Resource):

    def get(self):
        return "Server for metadatas of panoramics images / Oslandia"


@infos_ns.route("/contact")
class InfosContact(Resource):

    def get(self):
        return "infos@oslandia.com"


@infos_ns.route("/online")
class InfosOnline(Resource):

    def get(self):
        return "Congratulation, panoramix-server is online!!!"

# -----------------------------------------------------------------------------
# panoramix api
# -----------------------------------------------------------------------------
pxserver_ns = api.namespace('panoramix/',
                            description='Entry to retrieve metadatas')


# infos
@pxserver_ns.route('/infos')
class PXServerInfos(Resource):

    def get(self):
        return px.PXInfos().run()


# frustum
frustum_parser = reqparse.RequestParser()
frustum_parser.add_argument('latitude', type=float, required=True)
frustum_parser.add_argument('longitude', type=float, required=True)
frustum_parser.add_argument('radius', type=float, required=True)
frustum_parser.add_argument('type', type=str, required=False,
                            choices=['all', 'cube', 'equi'], default='all')


@pxserver_ns.route('/frustum')
class PXServerFrustum(Resource):

    @api.expect(frustum_parser, validate=True)
    def get(self):
        args = frustum_parser.parse_args()
        return px.PXFrustum().run(args)


# metadata
metadata_parser = reqparse.RequestParser()
metadata_parser.add_argument('view', type=int, required=True)


@pxserver_ns.route('/metadata')
class PXServerMetadata(Resource):

    @pxserver_ns.response(404, 'View not found')
    @api.expect(metadata_parser, validate=True)
    def get(self):
        args = metadata_parser.parse_args()
        res = px.PXMetadata().run(args)
        if not res:
            pxserver_ns.abort(404, 'View not found')
        return res


# map
map_parser = reqparse.RequestParser()
map_parser.add_argument('view', type=int, required=False)
map_parser.add_argument('radius', type=float, required=False)


@pxserver_ns.route('/map')
class PXServerMap(Resource):

    @pxserver_ns.response(404, 'View not found')
    @api.expect(map_parser, validate=True)
    def get(self):
        args = map_parser.parse_args()
        res = px.PXMap().run(args)
        if not res:
            pxserver_ns.abort(404, 'View not found')
        return res
