from pyopp import cSimpleModule, cMessage, EV, SimTime, simTime
import random
from messages import *

class registerInterface(cSimpleModule):
     
    
        
    def __init__(self):
        super().__init__(16535)
        
    def initialize(self):
        self.wsnw=0
        self.rreqsn=0 
     #   print("in initialize for interface id="+str(self.getParentModule().getIndex()))
        
       # print("In initialize of registerInterface")
       # EV<<"In initialize of registerInterface"
        
    def activity(self):
       # print("in activity for interface id="+str(self.getParentModule().getIndex()))
       
       # print("In activity of registerInterface")
       # EV<<"In activity of registerInterface"
        
       # print(self.getParentModule())
       # print(self.getParentModule().getIndex())
       # print("after print getindex")
        if self.getParentModule().getIndex() ==0: # I am the writer
        #    print("before write")
            self.wait(10)
            self.write(1)
            self.wait(10)
            self.write(2)
        elif self.getParentModule().getIndex() ==1: # I am not a writer
            self.wait(5)
            val=self.read()
           # EV<<"process "<<self.getParentModule().getIndex()<<" read value "<<val
            print("process "+str(self.getParentModule().getIndex())+" read value "+str(val))
            self.wait(5)
            val=self.read()
          #  EV<<"process "<<self.getParentModule().getIndex()<<" read value "<<val
            print("process "+str(self.getParentModule().getIndex())+" read value "+str(val))
             
        elif self.getParentModule().getIndex() ==2: # I am not a writer
            self.wait(5)
            val=self.read()
           # EV<<"process "<<self.getParentModule().getIndex()<<" read value "<<val  
            print("process "+str(self.getParentModule().getIndex())+" read value "+str(val))
            self.wait(5)
            val=self.read()
           # EV<<"process "<<self.getParentModule().getIndex()<<" read value "<<val
            print("process "+str(self.getParentModule().getIndex())+" read value "+str(val))
           
      #  print("activity done for index "+str(self.getParentModule().getIndex()))
      
    def write(self, v):
        
        self.wsnw = self.wsnw +1
     #   print("before send write")
     #   EV<<"before send write"
        m=WriteOperation(self.wsnw, v)
      #  print("created m"+str(type(m)))
        
#        m1=m.dup()
    #    print("created m1 "+str(type(m1)))
        
        self.send(m, "bcastToCore")
    #    print("write interface waiting")
        EV<<"write interface waiting"
        maj=self.receive()
        self.delete(maj)
#        maj=None
   #     EV<<"write interface received"<<maj
#         if maj.getName=="ackwritemaj" and maj.wsn==self.wsnw: 
#             EV<< "At "<<simTime()<<" process "<< self.getParentModule().getIndex()<<" received majority for write "<<self.wsnw
#         else:
#             EV<< "Somethings Wrong At "<<simTime()<<" process "<< self.getParentModule().getIndex()<<" received majority for write "<<maj.wsn<<" but was expecting "<<self.wsnw

    def read(self):
        self.rreqsn=self.rreqsn+1
        self.send(ReadOperation(self.rreqsn),"bcastToCore")
#         EV<<"read interface waiting"   
        highestAckReadReq=self.receive()
#         EV<<"read interface received"<<maj
        v=highestAckReadReq.regvalue
        self.delete (highestAckReadReq)
#        highestAckReadReq=None
        return (v)    
