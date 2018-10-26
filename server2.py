import serial
import time
from colas import colas
from threading import Thread


class btread(Thread):

    def __init__(self, _btserial,):
        self.bts=_btserial
        self.qpBT = colas("pBT")
        self.qpBT.create()

        Thread.__init__(self)

    def run(self):
        msg = ''
        while msg != 'bye':
            time.sleep(0.2)
            msg=self.bts.readline()
            if len(msg) > 0:
                print("BT receiving [%s]" % msg)
                self.qpBT.put(msg)


class btwrite(Thread):

    def __init__(self, _btserial):
        self.bts=_btserial
        self.qrBT = colas("rBT")
        self.qrBT.create()
        Thread.__init__(self)

    def run(self):
        msg = ''
        while msg != 'bye':
            time.sleep(0.2)
            msg = self.qrBT.get()
            if len(msg) > 0:
                print("BT Sending [%s]" % msg)
                self.bts.write(msg)


# rfcomm bind 1 98:D3:31:FC:3C:61 1

if __name__ == '__main__':

    # rfcomm bind 1 98:D3:31:FC:3C:61 1

    btserial = serial.Serial("/dev/rfcomm1", baudrate=9600)


    btObjread = btread(btserial)
    btObjwrite = btwrite(btserial)

    btObjread.setDaemon(True)
    btObjread.start()
    btObjwrite.setDaemon(True)
    btObjwrite.start()

    btObjread.join()
    btObjwrite.join()


