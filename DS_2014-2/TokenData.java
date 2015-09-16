
import java.util.*;

public class TokenData implements Token {

	List<Integer> LN;	//Last Request Number
	List<Integer> Q;	//Queue de solicitudes
	private static boolean isInstantiated = false;

	/**
	* Un token para todo el sistema
	* @param numProcesses - numero de procesos en el sistema
	*/
	private TokenData(int numProcesses){
		LN = new ArrayList<Integer>();
		Q = new ArrayList<Integer>();	
		for (int i = 0; i < numProcesses; i++){
			LN.add(0);
		}
		System.out.println("LN: " + LN);
		System.out.println("Q: " + Q );

	}

	/**
	* Instantiates token if executes for the first time
	* @return token after first execution, null otherwise
	*/
	public static TokenData instantiate(int numProcesses){
		if (!isInstantiated){
			isInstantiated = true;
			return new TokenData(numProcesses);
		}
		return null;
	}

	public List<Integer> getLN() {
		return LN;
	}

	public void finishRequest(int id, int RN[], int n){   // actualizar Token para solicitudes existentes
		//Actualiza la cola del token, RN[id] se ha ejecutado
		LN.set(id, RN[id]);
		//System.out.println("(" + id + ") despachará el token");
		//System.out.println("RN: " + Arrays.toString(RN));
		//System.out.println("LN: " + LN);
		//System.out.println("Q: " + Q);
		//Actualizar la cola de solicitudes pendientes
		for(int k = 0; k < n ; k++) {	
			boolean isInQ = false;
			for(int l = 0; l < Q.size(); l++){
				if(Q.get(l) == k)
					isInQ = true;			
			}
			if (!isInQ && (RN[k] >= (LN.get(k)))) {
					Q.add(k);
			}
		}
	} 
	public boolean isEmptyQueue() {
		if(Q != null) {
			if(Q.size() > 0)	//Queue tiene aún elementos, manda falso
				return false;
		}
		return true;		//Queue no tiene elementos, manda verdadero
	}
	public int getFirstQueue() {
		int first = Q.get(0);
		Q.remove(0);
		return first;
	}
}
