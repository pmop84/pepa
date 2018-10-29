import os

class videoq():
    def __init__(self, name):
        self.qFile = "/tmp/v" + name

    def create(self):
        os.mkfifo(self.qFile)

    def put(self, msg):
        pipe = open(self.qFile, "a")
        pipe.write(msg)
        pipe.close()

    def get(self):
        pipe = open(self.qFile, "r")
        msg = pipe.read()
        pipe.close()
        if not msg:
            msg = ''
        return msg


class colas():
    def __init__(self, name):
        self.qFile = "/tmp/q" + name

    def create(self):
        self.put('')

    def put(self, msg):
        pipe = open(self.qFile, "w")
        pipe.write(msg)
        pipe.close()

    def get(self):
        pipe = open(self.qFile, "r")
        msg = pipe.read()
        pipe.close()
        self.put('')
        if not msg:
            msg = ''
        return msg



