from bluetooth import *
import time
from colas import colas
from threading import Thread


class btcomm(Thread):

    def __init__(self, btaddr):
        self.btaddr = btaddr
        self.opentBT()
        self.qrBT = colas("rBT")
        self.qpBT = colas("pBT")

        Thread.__init__(self)

    def run(self):
        msg = ''
        while msg != 'bye':
            time.sleep(0.2)
            msg = self.qrBT.get()
            if len(msg) > 0:
                print("BT Sending [%s]" % msg)
                self.sock.send(msg + '\n')
            msg = self.sock.recv(1024).strip()
            if len(msg) > 0:
                print("BT receiving [%s]" % msg)
                self.qpBT.put(msg)


    def opentBT(self):
        # nearby_devices = discover_devices(addr)

        count = 1
        name = None
        while name is None:
            print(" BT: Trying to Locate " + self.btaddr + " " + str(count) + "/3")
            name = lookup_name(self.btaddr)
            count = count + 1
            if count > 3:
                print(self.btaddr + ' Not located, exiting')
                exit(2)

        print('Located ' + str(lookup_name(self.btaddr)) + " [" + str(self.btaddr) + "]")
        port = 1
        self.sock = BluetoothSocket(RFCOMM)
        count = 1
        while True:
            print(" BT: Trying to connect " + name + " " + str(count) + "/3")
            try:
                self.sock.connect((self.btaddr, port))
                break
            except:
                count = count + 1
                if count > 3:
                    print(str(self.btaddr) + ' Unable to connect, exiting')
                    exit(2)
        print("BT: Connected")
        # self.sock.setblocking(0)
        self.sock.send("Hola Pepa!!")

    def closeBT(self):
        self.sock.close()


if __name__ == '__main__':

    pepaBaseAddr = "98:D3:31:FC:3C:61"

    btObj = btcomm(pepaBaseAddr)
    btObj.start()
    btObj.join()


