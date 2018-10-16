from flask import Flask
from flask_restful import Api, Resource
from colas import colas


def processApiAction(action):
    print('Process API -> ' + action)
    if action in ('up', 'down', 'left', 'right', 'stop', 'auto'):
        qrBT.put(msg)
    elif action == 'camera':
        print("Camara")

def processBTAction(self):
    print('Process BT -> ' + action)
    msg = qpBT.get()
    return msg



class ControlApiRest(Resource):

    def get(self,name):
        print('MSG Recibido del APIRest(->qrBT): ' + name)
        processApiAction(name)
        return "OK", 200


class ResponseApiRest(Resource):

    def get(self,name):
        msg=''
        msg = processBTAction()
        print('MSG Recibido de (qpBT->): ' + msg)
        return msg, 200


if __name__ == '__main__':

    pepaIP = "192.168.1.9"
    pepaPort = 8004
    qrRes = colas("rRest")
    qpRes = colas("pRest")
    qrBT  = colas("rBT")
    qpBT = colas("pBT")

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ControlApiRest, "/pepa/Control/<string:name>")
    api.add_resource(ResponseApiRest, "/pepa/Request/<string:name>")


    app.run(host=pepaIP, port=pepaPort, debug=True)


