package cl.utfsm.inf.sd.token;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.io.Serializable;

/*
	TokenServiceProxy: Interfaz local (en un proceso/nodo), o proxy, a un servicio de Token
    implementado usando el algoritmo de Suzuki-Kasami.
 */

public interface TokenServiceProxy {
	public void getToken();			// Solicitar el token y entrar para ingresar SC
	public void freeToken();		// Liberar el token al salir de SC
	public boolean hasToken();      // verifica si se tiene el Token (útil en estado ocioso)
}


/*
    Representa el Token, que puede ser serializado para pasarlo de un proceso a otro. Los métodos son:
    finishRequest: Este método actualiza el Token, considerando que el proceso con identificador "id"
                    ha terminado de usar el token, y el estado actualizado del vector de solicitudes
                    RN es usado para actualizar internamente el vector LN y cola de solictudes pendientes.
    isEmptyQueue:   verifica si la cola del Token esta vacia.
    getFirstQueue:  Obtiene y extrae primer elemento de la cola del Token.
 */
public interface Token extends Serializable {
	public void finishRequest( int id, int RN[], int n);   // actualizar Token para solicitudes existentes (actualiza cola)
	public boolean isEmptyQueue();
	public int getFirstQueue();
}

/*
	Interfaz que representa el servicio distribuido de token, y que debe ser usado por la implementación de
    TokenServiceProxy para solicitar el Token a los demás procesos y para pasarle el Token a un determinado
    proceso. Además se disponen de dos métodos para hacer arrancar o detener el servicio.
 */
public interface TokenServiceMgr extends Remote {
	public void start() throws RemoteException;
//	public void stop() throws RemoteException;
	public void requestToken(int id, int sn) throws RemoteException;
	public void passToken(Token tkn) throws RemoteException;

}

