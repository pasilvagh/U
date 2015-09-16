
import java.io.Serializable;

/*
    Representa el Token, que puede ser serializado para pasarlo de un proceso a otro. Los métodos son:
    finishRequest: Este método actualiza el Token, considerando que el proceso con identificar "id"
                    ha terminado de usar el token, y el estado actualizado del vector de solicitudes
                    RN es usado para actualizar internamente el vector LN y cola de solictudes pendientes.
    isEmptyQueue:   verifica si la cola del Token esta vacia.
    getFirstQueue:  Obtiene y extrae primer elemento de la cola del Token.
 */
public interface Token extends Serializable {
	public void finishRequest( int id, int RN[], int n);   // actualizar Token para solicitudes existentes
	public boolean isEmptyQueue();
	public int getFirstQueue();
}

