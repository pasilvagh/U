

import java.rmi.RMISecurityManager;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.lang.Runtime.*;
import java.lang.Thread;


import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.util.*;

import java.lang.*;
import java.lang.Thread;
import java.util.*;

public class Semaforo {

	public static int id;
	public static int color;	//Colores: 0->verde, 1->amarillo, 2->rojo
	public static int totalProcesses;
	public static boolean inCriticalSection;

	//Colores
	public static final String ANSI_RESET = "\u001B[0m";
	public static final String ANSI_BLACK = "\u001B[30m";
	public static final String ANSI_RED = "\u001B[31m";
	public static final String ANSI_GREEN = "\u001B[32m";
	public static final String ANSI_YELLOW = "\u001B[33m";
	public static final String ANSI_BLUE = "\u001B[34m";
	public static final String ANSI_PURPLE = "\u001B[35m";
	public static final String ANSI_CYAN = "\u001B[36m";
	public static final String ANSI_WHITE = "\u001B[37m";

	/**
	* Maximum delay simulating a computation unit within {@link #compute()} method and a critical section.
	*/
	public static final int MAX_COMPUTATION_DELAY = 3000;

	private static Random random = new Random();


	public static void work(TokenServiceProxyImp proxy) {
		
		//Solicitud del Token a todos los procesos remotos existentes. Si se queda esperando el token, se bloqueará solo esta Thread.		
		if(!proxy.hasToken() && (color == 0)) { //Esta en estado ocioso (verde), pero sin token
			System.out.println("request Token de semaforo");
			color = 1; 
			colorChanged();
			proxy.getToken();
		
		//System.out.println("inicio una thread para obtener el token");
		}	
		try {
			//otro tiempo random que espera
			Thread.sleep(random.nextInt(MAX_COMPUTATION_DELAY));
		} catch (InterruptedException e) {
			throw new RuntimeException(e);
		}
		if(proxy.hasToken()) { //tiene el token y puede estar en estado ocioso (verde) o recién haber recibido 								el token (amarillo->verde)
			color = 0; 
			colorChanged();
			//CS
			proxy.inCriticalSection();
			color = 2;
			colorChanged();
			//Sleep por un tiempo random
			try {
			    Thread.sleep(random.nextInt(MAX_COMPUTATION_DELAY));
			} catch (InterruptedException e) {
			    
			}
			proxy.outCriticalSection();
			color = 0;
			colorChanged();
			//Termina la seccion critica y libera el token
			proxy.freeToken();

		}
		try {
			//otro tiempo random que espera
			Thread.sleep(random.nextInt(MAX_COMPUTATION_DELAY));
		} catch (InterruptedException e) {
			throw new RuntimeException(e);
		}
	}

	public static void main(String[] args) {

		if(args.length < 2) {
			System.out.println("La cantidad de argumentos no es válida, el proceso se cerrará");
			System.exit(0);
		}
		try {
			totalProcesses = (int)Integer.parseInt(args[0]);
			id = (int)Integer.parseInt(args[1]);
			if(id + 1> totalProcesses){
				System.out.println("Los argumentos no son validos");
				System.exit(1);
			}
		} catch (NumberFormatException e) {
			System.err.println("Argumentos" + args[0] + " or "+ args[1] + " deben ser integers.");
			System.exit(1);
		}

		//Crea un Security Manager
		if (System.getSecurityManager() == null) {
		    System.setSecurityManager(new RMISecurityManager());
		}	
		color = 0;
		colorChanged();
		TokenServiceProxyImp proxy = new TokenServiceProxyImp(id, totalProcesses);	
		//inicializa el algoritmo
		proxy.startAlg();
		while(true) {
			work(proxy);
		}
	
	}
	
	public static synchronized void colorChanged() {
		String clr = "";
		String code = "";
		switch(color) {
			case 0:	clr = "Verde"; code = ANSI_GREEN; break;
			case 1: clr = "Amarillo"; code = ANSI_YELLOW; break;
			case 2: clr = "Rojo"; code = ANSI_RED; break;
			default: break; 
		}
		System.out.println("Color Semaforo: " + code + clr + ANSI_RESET);
	}

}
                                             
