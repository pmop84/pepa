from threading import Thread
import time
from colas import colas
from btcomm import btcomm

class consumerBT(Thread):

    def __init__(self):
        Thread.__init__(self)


    def run(self):
        msg = ''
        while msg != "bye":
            time.sleep(0.2)
            #print('consumerBT')
            msg = qpBT.get()
            if len(msg) > 0 :
                self.processBTAction(msg)
                qrRest.put(msg)


    def processBTAction(self,action):
        print('Process BT -> ' + action)
        return action

class consumerRest(Thread):

    def __init__(self):
        Thread.__init__(self)


    def run(self):
        msg = ''
        while msg != "bye":
            time.sleep(0.2)
            #print('consumerRest')
            msg = qpRest.get()
            if len(msg) > 0 :
                msg=self.processApiAction(msg)
                qrBT.put(msg)

    def processApiAction(self,action):
        print('Process API -> ' + action)
        return action



if __name__ == '__main__':

    pepaBaseAddr = "98:D3:31:FC:3C:61"

    qrRest = colas("rRest")
    qrRest.create()
    #qrRest.put('hello')
    qpRest = colas("pRest")
    qpRest.create()
    #qpRest.put('hello')
    qrBT = colas("rBT")
    qrBT.create()
    #qrRest.put('hello')
    qpBT = colas("pBT")
    qpBT.create()
    #qpRest.put('hello')

    btObj = btcomm(pepaBaseAddr)
    btObj.start()

    cBT = consumerBT()
    cBT.start()

    cRE = consumerRest()
    cRE.start()


    cBT.join()
    cRE.join()
    btObj.join()


