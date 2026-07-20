"""
CONNESSIONE E STATO - verificare che il robot sia vivo e in salute
==============================================================

Comandi trattati in questo file:
  - EnableRobot()   accende il robot
  - DisableRobot()  spegne il robot
  - ClearError()    azzera uno stato di allarme/errore
  - RobotMode()     chiede al robot in che stato si trova attualmente

Usa questo file per verificare la tua connessione e leggere lo
stato del robot PRIMA di scrivere qualsiasi script che lo faccia
muovere.
"""

from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)

# ClearError() dovrebbe essere una delle prime cose che chiami in
# qualsiasi script. Non risolve la CAUSA di un errore passato,
# azzera solo il flag "sono in uno stato di errore", così il robot
# è disposto ad accettare di nuovo comandi.
print("Cancellazione degli errori...")
print(dashboard.ClearError())
sleep(0.5)

# EnableRobot() accende i motori. Finché questo non viene chiamato,
# il robot rifiuterà i comandi di movimento.
print("Abilitazione del robot...")
print(dashboard.EnableRobot())
sleep(1)

# RobotMode() restituisce un numero che descrive cosa sta facendo
# il robot in questo momento. Alcuni dei valori più comuni che
# vedrai:
#   4 = acceso ma NON abilitato
#   5 = abilitato e pronto
#   6 = in modalità drag/apprendimento
#   7 = attualmente in esecuzione di un comando di movimento
#  10 = in pausa
# Questo è utile da controllare all'interno di cicli - ad esempio
# "aspetta finché la modalità non è 5 prima di inviare il prossimo
# comando".
print("Modalità robot attuale:", dashboard.RobotMode())

sleep(2)

# DisableRobot() interrompe l'alimentazione dei motori in modo
# controllato. Chiama sempre questo alla fine di uno script,
# invece di chiudere semplicemente la finestra.
print("Disabilitazione del robot...")
print(dashboard.DisableRobot())

print("Fatto!")
