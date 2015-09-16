

import java.rmi.RMISecurityManager;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.lang.Runtime.*;
import java.lang.Thread;


import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.util.*;


public class Controller {

	public static int numProcesses = 0;

	private static Map<Integer, TokenServiceMgr> processCache;

	private static Random random = new Random();

	public static void main(String[] args){
		

		if(args.length < 1) {
			System.out.println("La cantidad de argumentos no es válida, el proceso se cerrará");
			System.exit(0);
		}
		try {
			numProcesses = (int)Integer.parseInt(args[0]);
		} catch (NumberFormatException e) {
			System.err.println("Argumentos" + args[0] + " or "+ args[1] + " deben ser integers.");
			System.exit(1);
		}


		//Crea un Security Manager
		if (System.getSecurityManager() == null) {
		    System.setSecurityManager(new RMISecurityManager());
		}

		try {
			int first = random.nextInt(numProcesses);
			//busca a los objetos remotos disponibles y los guarda en un cache, para así invocar el método start() de todos ellos y el algoritmo quede en standby para obtener el token.
			processCache = new HashMap<Integer, TokenServiceMgr>(numProcesses);
			llenarCache();
			//Envía a un objeto remoto, de forma aleatoria, el token para iniciar el algoritmo.
			Token token = TokenData.instantiate(numProcesses);
			if (token != null){
				System.out.println("existe el token!");
				processCache.get(new Integer(first)).passToken(token);
			}
		} catch(Exception e) {
			System.exit(0);
		}
	}


	public static void llenarCache() {	
		for(int i = 0; i < numProcesses ; i++) {
			//llena con los stubs de los demas objetos remotos
			getProcess(new Integer(i));
		}
		 //Para mostrar los elementos remotos
		/*for (Integer i: processCache.keySet()) {  
			String key =i.toString();
			String value = processCache.get(i).toString();  
			System.out.println(key + " " + value + "\n");   
		} */
	}


	private static void getProcess(Integer numProc) {
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
}
