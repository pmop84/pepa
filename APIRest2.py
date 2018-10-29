from flask import Flask, render_template, Response
from colas import colas
from camera import Camera

app = Flask(__name__)


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

def generate(Camera):
    while True:
        frame = Camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/pepa/Control/<name>')
def manageControl(name):
    print('MSG Recibido del APIRest(->qrBT): ' + name)
    processApiAction(name)
    return Response("OK")

@app.route('/pepa/Request')
def manageRequest():
    msg = processBTAction()
    print('MSG Recibido de (qpBT->): ' + msg)
    return Response(msg)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pepa/Camera')
def video_feed():
    return Response(generate(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    pepaIP = "192.168.1.252"
    pepaPort = 8004
    qrBT  = colas("rBT")
    qpBT = colas("pBT")

    app.run(host=pepaIP, port=pepaPort, threaded=True, debug=True)