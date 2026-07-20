"""
MOVIMENTO DEI GIUNTI - muovere il robot con MovJ()
=============================================

Comandi trattati in questo file:
  - MovJ()      muove usando un movimento nello spazio dei giunti
  - GetAngle()  legge l'angolo attuale di ogni giunto
  - SpeedFactor() imposta la velocità dei movimenti

Il movimento JOINT (dei giunti) significa che ogni giunto ruota
direttamente verso il suo angolo di destinazione. NON garantisce
che l'utensile si muova in linea retta nello spazio - per questo,
vedi 03_linear_motion.py (MovL).

Il movimento dei giunti è il tipo di movimento più semplice e
sicuro da cui partire, poiché ragioni in termini di "ruota questo
giunto a questo angolo" invece che di coordinate 3D.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_angles(response_string):
    """
    Il robot invia le sue risposte come testo, ad es.:
      "0,{30.0000,0.0000,0.0000,0.0000,0.0000,0.0000},GetAngle();"
    Questa funzione estrae i sei numeri da quel testo e li
    restituisce come una normale lista Python di numeri, così
    possiamo usarli nei calcoli (es. current_angles[0] per J1).
    """
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Cancellazione degli errori e abilitazione...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

# Inizia sempre lentamente mentre fai i test. 100 = velocità
# massima, che dovresti usare solo quando ti fidi pienamente di
# uno script.
print("Impostazione della velocità al 20%...")
print(dashboard.SpeedFactor(20))
sleep(0.5)

# Leggi dove si trova attualmente il robot prima di muovere qualcosa.
current = parse_angles(dashboard.GetAngle())
print("Angoli dei giunti attuali:", current)

# MovJ(J1, J2, J3, J4, J5, J6, mode)
# L'ultimo argomento, 1, dice al robot che questi sei numeri sono
# ANGOLI DEI GIUNTI in gradi (e non coordinate X/Y/Z/Rx/Ry/Rz, che
# è invece ciò che usa MovL).
print("\nSpostamento di J1 a 30 gradi, tutti gli altri giunti invariati...")
result = dashboard.MovJ(30, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)

new_angles = parse_angles(dashboard.GetAngle())
print("Nuovi angoli dei giunti:", new_angles)

print("\nRitorno alla posizione a zero...")
dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
sleep(3)

print("Disabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
