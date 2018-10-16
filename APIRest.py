from flask import Flask
from flask_restful import Api, Resource
from colas import colas


class ControlApiRest(Resource):

    def get(self,name):
        print('MSG Recibido del APIRest(->qpRest): ' + name)
        qpRes.put(name)
        return "OK", 200


class ResponseApiRest(Resource):

    def get(self,name):
        msg=''
        msg=qrRes.get()
        print('MSG Recibido de (qpRest->): ' + msg)
        return msg, 200


if __name__ == '__main__':

    pepaIP = "192.168.1.9"
    pepaPort = 8004
    qrRes = colas("rRest")
    qpRes = colas("pRest")

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ControlApiRest, "/pepa/Control/<string:name>")
    api.add_resource(ResponseApiRest, "/pepa/Request/<string:name>")


    app.run(host=pepaIP, port=pepaPort, debug=True)


