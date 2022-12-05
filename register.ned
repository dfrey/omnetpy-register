simple registerCore{
	gates:
	    input bcastFromIface;
	    output msgToIface;
	    input remoteIn @directIn;
}

simple registerInterface{
	gates:
	    input msgFromCore;
	    output bcastToCore;
}

module regularRegister{
	//gates:
//	    remotein @directin
	submodules:
	    iface: registerInterface;
	    core: registerCore;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
	connections: 
	    core.bcastFromIface <-- iface.bcastToCore;
	    core.msgToIface --> iface.msgFromCore;
}

network Distalgo
{
    parameters:
        int numProc;  // number of processes
        int maxDelay; //maximum message delay
    submodules:
        procs[numProc]: regularRegister;
        
}