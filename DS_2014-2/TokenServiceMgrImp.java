

import java.rmi.Remote;
import java.rmi.RemoteException;

import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.*;


public class TokenServiceMgrImp extends UnicastRemoteObject implements TokenServiceMgr {

	private static final long serialVersionUID = 2526720373028386278L;
	public int[] RN; //Array de Request Number
	private int index; //ID del proceso
	private int numProcesses; //Cantidad de procesos participando
	public TokenData token = null;
	public boolean inCritSect = false;
	private TokenController tokenC;


	public TokenServiceMgrImp(int id, int total, TokenController tc) throws RemoteException {
		numProcesses = total;
		index = id;
		tokenC = tc;
		RN =  new int[total];
	}

	public void start() {
		requestToken(index, index);
	}

	public synchronized void requestToken(int id, int sn) { // Proceso i recibe requestToken de proceso j, con sn e id de j. 
		try {
			while(true) {
				if(!this.inCritSect)
					break;
				else
					wait();
			}	
			RN[id] = (RN[id] > sn) ? RN[id] : sn; //actualiza el sn por la petición de otro proceso		
			if(!this.inCritSect)
				notify();
			if((this.token != null) && !this.inCritSect && (this.RN[id] > this.token.LN.get(id))) {
				Token tmpToken = token;
				this.token = null;
				this.tokenC.processCache.get(new Integer(id)).passToken(tmpToken);
				System.out.println("req----------proceso " + index + " pasa token a proceso " + id);
			}
		}catch(Exception e) {
			
		}
	}


	public void passToken(Token tkn) { // Pasar el token a otro proceso
		token = (TokenData)tkn;
		System.out.println("++++++++++proceso " + index + " recibe token");
	}

}


