

public class TokenServiceProxyImp implements TokenServiceProxy {

	private TokenController tknCntrller;

	//Constructor
	public TokenServiceProxyImp(int idProc, int total) {
		tknCntrller = new TokenController(idProc, total);
	}

	public void getToken() {		// Solicitar el token y entrar para ingresar SC
		this.tknCntrller.sendingRequestToken();
	}

	public void freeToken() {		// Liberar el token al salir de SC
		this.tknCntrller.sendingRequestFree();
	}

	public boolean hasToken() {		// verifica si se tiene el Token (útil en estado ocioso)
		if(this.tknCntrller.tsm.token != null)
			return true;
		return false;
	}

	public void inCriticalSection() {
		tknCntrller.inCriticalSection();
	}

	public void outCriticalSection() {
		tknCntrller.outCriticalSection();
	}

	public void startAlg() {
		tknCntrller.tsm.start();
	}
}
