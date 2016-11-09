# -*- coding: utf-8 -*-
from flask_restplus import Api, Resource as OrigResource

from pxserver.database import pgexceptions


class Resource(OrigResource):
    # add a postgresql exception decorator for all api methods
    method_decorators = [pgexceptions]


api = Api(
    version='0.1', title='Panoramix Server',
    description='API for accessing panoramics images',
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
        return "Server for panoramics images / Oslandia"


@infos_ns.route("/contact")
class InfosContact(Resource):

    def get(self):
        return "infos@oslandia.com"


@infos_ns.route("/online")
class InfosOnline(Resource):

    def get(self):
        return "Congratulation, panoramix-server is online!!!"
