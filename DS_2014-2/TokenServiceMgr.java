

import java.rmi.Remote;
import java.rmi.RemoteException;


/*
	Interfaz que representa el servicio distribuido de token, y que debe ser usado por la implementación de
    TokenServiceProxy para solicitar el Token a los demás procesos y para pasarle el Token a un determinado
    proceso. Además se disponen de dos métodos para hacer arrancar o detener el servicio.
 */
public interface TokenServiceMgr extends Remote {
	public void start() throws RemoteException;
	//public void stop() throws RemoteException;
	public void requestToken(int id, int sn) throws RemoteException;
	public void passToken(Token tkn) throws RemoteException;
}
