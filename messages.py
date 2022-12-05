from pyopp import cMessage

        
class WriteOperation(cMessage):
    def __init__(self, wsn, value):
        super().__init__("writeoperation")
        self.value=value
        self.wsn=wsn
        
    def dup(self):
        return WriteOperation(self.wsn,self.value)   
    
class ReadOperation(cMessage):
    def __init__(self, rsn):
        super().__init__("readoperation")
        self.rsn=rsn
        
    def dup(self):
        return ReadOperation(self.rsn)   
        
class AckWriteMaj(cMessage):
    def __init__(self, wsn):
        super().__init__("ackwritemaj")
        self.wsn=wsn
    def dup(self):
        return AckWriteMaj(self.wsn)   
    
class AckReadReqMaj(cMessage):
    def __init__(self, rsn, wsn, regvalue):
        super().__init__("ackreadreqmaj")
        self.rsn=rsn
        self.wsn=wsn
        self.regvalue=regvalue
    def dup(self):
        return AckReadReqMaj(self.rsn, self.wsn, self.regvalue)   



         

class Write(cMessage):
    def __init__(self, wsn, value):
        super().__init__("write")
        self.wsn=wsn
        self.value=value
        
    def dup(self):
        return Write(self.wsn,self.value)

class AckReadReq(cMessage):
    def __init__(self, rsn, wsn, regvalue):
        super().__init__("ackreadreq")
        self.rsn=rsn
        self.wsn=wsn
        self.regvalue=regvalue
    def dup(self):
        return AckReadReq(self.rsn,self.wsn,self.regvalue)   

       
class AckWrite(cMessage):
    def __init__(self, wsn):
        super().__init__("ackwrite")
        self.wsn=wsn
    def dup(self):
        return AckWrite(self.wsn)   


class ReadReq(cMessage):
    def __init__(self, rsn):
        super().__init__("readreq")
        self.rsn=rsn
    def dup(self):
        return ReadReq(self.rsn)   
        
        
