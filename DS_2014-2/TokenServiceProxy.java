

/*
	TokenServiceProxy: Interfaz local (en un proceso/nodo), o proxy, a un servicio de Token
    implementado usando el algoritmo de Suzuki-Kasami.
 */

public interface TokenServiceProxy {
	public void getToken();			// Solicitar el token y entrar para ingresar SC
	public void freeToken();		// Liberar el token al salir de SC
	public boolean hasToken();      // verifica si se tiene el Token (útil en estado ocioso)
}
