from . import main
from flask_restful import Resource, Api

api = Api(main)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
