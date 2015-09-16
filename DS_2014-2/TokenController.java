import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.util.*;
import java.net.InetAddress;

import java.lang.Thread;


public class TokenController {

	private static final int TOKEN_WAIT_DELAY = 50; //Delay maximo para esperar a token
	public Map<Integer, TokenServiceMgr> processCache; //cache para buscar los procesos remotos (numProceso, procRemoto)
	public TokenServiceMgrImp tsm;
	private int total;
	private int id;
	public boolean inCriticalSection;

	public TokenController(int procId, int n) {
		total = n;
		id = procId;
		inCriticalSection = false;
		processCache = new HashMap<Integer, TokenServiceMgr>(total);
		String name;
		try {
			if(processCache.get(new Integer(id)) == null) {
				//bind del objeto remoto
				name = "Semaforo" + id;
				tsm = new TokenServiceMgrImp(id, total, this);
				processCache.put(new Integer(id),tsm);
				//TokenServiceMgr stub = (TokenServiceMgr) UnicastRemoteObject.exportObject(tsm, 0); //TokenServiceMgr extends a UnicastRemoteObject, por lo tanto esta linea esta de mas.
				Registry registry = LocateRegistry.getRegistry();
				registry.rebind(name, tsm);
				String[] list = Naming.list(name);
				System.out.println("Lista: ");
				for (String i: list) {
					System.out.println(i);
				}
			}
		} catch (Exception e) {
			System.err.println("Error al crear bind");
			e.printStackTrace();
		}
		//lenar cache hasta que todos los stubs esten disponibles
		llenarCache();
	}

	public void llenarCache() {	
		try {
			Thread.sleep(6000);

			for(int i = 0; i < total ; i++) {
				//llena con los stubs de los demas objetos remotos
				if(i != id)
					getProcess(new Integer(i));
			}
			 //Para mostrar los elementos remotos
			/*for (Integer i: processCache.keySet()) {  
				String key =i.toString();
				String value = processCache.get(i).toString();  
				System.out.println(key + " " + value + "\n");   
			} */

		} catch (InterruptedException e) {
			throw new RuntimeException(e);
		}
	}

	private void getProcess(Integer numProc) {
		TokenServiceMgr result = processCache.get(numProc);
		if (result == null) {
			String name = "Semaforo" + numProc;
			try {
				result = (TokenServiceMgr) Naming.lookup(name);
			} catch (RemoteException e1) {
				throw new RuntimeException(e1);
			} catch (MalformedURLException e2) {
				throw new RuntimeException(e2);
			} catch (NotBoundException e3) {
				throw new RuntimeException(e3);
			}
			processCache.put(numProc, result);
		}
	}


	public void sendingRequestToken() { //request token para entrar en SC - listo
		int newSn = tsm.RN[id] + 1;
		tsm.RN[id] = newSn;
		for(int i = 0; i < total; i++) {
			try {
				if(i != id)
					processCache.get(new Integer(i)).requestToken(id, newSn);
			} catch (RemoteException e) {
				throw new RuntimeException(e);
			}					
		}
	}

	public void sendingRequestFree() { //falta por terminar
		if(!inCriticalSection && (tsm.token != null)) {
			tsm.token.finishRequest(id, tsm.RN, total);
			if(!tsm.token.isEmptyQueue()) {
				int first = tsm.token.getFirstQueue();
				if(id != first) {
					try {
						Token tmpToken = tsm.token;
						tsm.token = null;
						processCache.get(new Integer(first	)).passToken(tmpToken);
						System.out.println("free----------proceso " + id + " pasa token a proceso " + first);
					} catch (RemoteException e) {
						throw new RuntimeException(e);
					}								
				}
			}
		}
	}

	public void inCriticalSection() {
		inCriticalSection = true;
		tsm.inCritSect = true;
	}

	public void outCriticalSection() {
		inCriticalSection = false;
		tsm.inCritSect = false;
	}
}
