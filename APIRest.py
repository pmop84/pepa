from flask import Flask,send_from_directory, stream_with_context
from flask_restful import Api, Resource
from colas import colas
from camera import Camera

def processApiAction(action):
    print('Process API -> ' + action)
    if action in ('u', 'd', 'l', 'r', 's', 'a', 'i','t','g'):
        qrBT.put(action)
    elif action == 'camera':
        print("Camara")

def processBTAction():
    msg = qpBT.get()
    print('Process BT -> ' + msg)
    return msg


class ControlApiRest(Resource):

    def get(self,name):
        print('MSG Recibido del APIRest(->qrBT): ' + name)
        processApiAction(name)
        return "OK", 200


class RequestApiRest(Resource):

    def get(self,name):
        msg=''
        msg = processBTAction()
        print('MSG Recibido de (qpBT->): ' + msg)
        return msg, 200

class Index(Resource):

    def get(self,filename):
        return send_from_directory("/root/pepa/",filename)



def generate(Camera):
    while True:
        frame = Camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


class IpCamera(Resource):

    def get(self):
        return generate(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame'

if __name__ == '__main__':

    pepaIP = "192.168.1.252"
    pepaPort = 8004
    qrBT  = colas("rBT")
    qpBT = colas("pBT")

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ControlApiRest, "/pepa/Control/<string:name>")
    api.add_resource(RequestApiRest, "/pepa/Request/<string:name>")
    api.add_resource(Index, "/pepa/<path:filename>")


    app.run(host=pepaIP, port=pepaPort, debug=True)