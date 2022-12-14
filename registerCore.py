from pyopp import cSimpleModule, cMessage, EV, SimTime, simTime
import random
from messages import *

class registerCore(cSimpleModule):
    
    def broadcast(self, msg):
        
        numProcesses=self.n 
        for pid in range(0, numProcesses):
            # need to send to ourselves as well if pid!=self.getIndex():
            destProcess=self.networkModule.getSubmodule("procs",pid).getSubmodule("core");
            delay=random.randint(0, self.networkModule.par("maxDelay").intValue())
            self.sendDirect(msg.dup(), SimTime(delay), SimTime(0.0),  destProcess, "remoteIn")

    def initialize(self):
      #  print("in initialize for core id="+str(self.getParentModule().getIndex()))
        self.networkModule=self.getParentModule().getParentModule()
        self.n=int(self.networkModule.par("numProc").intValue())
        self.ackwritemsgs=[]
        self.ackreadreqmsgslist=[]        
        self.ackreadreqmsgs={}
        self.writing=False
        self.reading=False
        self.mywsn=0
        self.myrrsn=0
        self.myreg=0
  #      print("end of initialize for core id="+str(self.getParentModule().getIndex()))
        
        #if self.getIndex() ==0:
        #    EV << "process "<< self.getIndex()<<" broadcasting"
         #   self.broadcast(cMessage('write'))

    def handleMessage(self, msg):
        msgType=msg.getName()
        msgclass=type(msg)
        #print("message of class "+str(msgclass))
        #EV<<"message of class "<<msgclass
        if msgType=="writeoperation": 
            self.writing=True
            self.mywsn=self.mywsn+1 
            self.myreg=msg.value          
            self.broadcast(Write(self.mywsn,msg.value)) 
    
        if msgType=="readoperation":
            self.reading=True
            self.myrrsn=self.myrrsn+1
            self.broadcast(ReadReq(self.myrrsn)) 
        
        if msgType=="write":
            if msg.wsn>=self.mywsn:
                self.mywsn=msg.wsn
                self.myreg=msg.value
            self.sendDirect(AckWrite(msg.wsn).dup(), msg.getSenderModule(),"remoteIn")    
#            self.delete(msg) # delete because it was broadcast
            
        if msgType=="readreq":
            self.sendDirect(AckReadReq(msg.rsn, self.mywsn, self.myreg).dup(), msg.getSenderModule(),"remoteIn")    
#            self.delete(msg) # delete because it was broadcast
#            print(str(self.getParentModule().getIndex())+" deleted readreq")
            
        if msgType=="ackreadreq":
#            print(str(self.getParentModule().getIndex())+"processing ackreadreq")
            if msg.rsn==self.getParentModule().getSubmodule("iface").rreqsn and self.reading: # do not process if this is a stale ack    
                self.ackreadreqmsgs[msg.wsn]=msg.regvalue
                self.ackreadreqmsgslist.append(msg.wsn)
                if (len(self.ackreadreqmsgslist)>self.n/2): # we have a majority
                    maxwsn=max(sn for sn in self.ackreadreqmsgs.keys())
                    value=self.ackreadreqmsgs[maxwsn]
                    self.reading=False
                    self.send(AckReadReqMaj(self.getParentModule().getSubmodule("iface").rreqsn, maxwsn, value).dup(),"msgToIface")
        

        if msgType=="ackwrite":
            # collect responses 
            if msg.wsn==self.getParentModule().getSubmodule("iface").wsnw and self.writing: # do not process if this is a stale ack    
                self.ackwritemsgs.append(msg.wsn)
                if (len(self.ackwritemsgs)>self.n/2): # we have a majority
                    self.writing=False
                    self.send(AckWriteMaj(msg.wsn).dup(),"msgToIface")
        
        #EV<< "At "<<simTime()<<" process "<< self.getIndex()<<" received message "<<msg<<" from process "<< msg.getSenderModule().getIndex()
      #  self.send(msg, 'out')
      #  self.delete(msg)                  

#        self.delete (msg)
#        msg=None

