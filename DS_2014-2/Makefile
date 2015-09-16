JFLAGS = -g
JC = javac

all:
	$(JC) Token.java TokenData.java TokenServiceProxy.java TokenServiceMgr.java TokenServiceMgrImp.java TokenServiceProxyImp.java TokenController.java Semaforo.java Controller.java
	rmiregistry &

# Argumento del final es la cantidad de procesos que tendra el algoritmo SK.
controller:
	java -Djava.security.policy=java.policy Controller 3

sem1:
	java -Djava.security.policy=java.policy Semaforo 3 0
sem3:
	java -Djava.security.policy=java.policy Semaforo 3 2
sem2:
	java -Djava.security.policy=java.policy Semaforo 3 1

clean:
	$(RM) ./*.class
	$(RM) *.java~
	$(RM) Makefile~
	$(RM) README~
	
