"""
MOVIMENTO LINEARE E POSA - muoversi in linea retta, e leggere la
posizione in termini di X/Y/Z
==================================================================

Comandi trattati in questo file:
  - MovL()     muove l'utensile in linea retta nello spazio
  - GetPose()  legge la posizione attuale dell'utensile come X, Y, Z, Rx, Ry, Rz

A differenza di MovJ (movimento dei giunti), MovL garantisce che la
punta dell'utensile percorra una linea fisica retta tra la
posizione attuale e quella di destinazione. Questo è utile ogni
volta che il PERCORSO conta - ad esempio muoversi lungo la
superficie di un tavolo senza scendere dentro di essa.

Le coordinate qui sono in termini "Cartesiani":
  X, Y, Z    = posizione in millimetri, rispetto a un punto di riferimento
  Rx, Ry, Rz = orientamento (rotazione) dell'utensile, in gradi

Questo è più complesso da ragionare rispetto agli angoli dei
giunti, poiché devi conoscere il sistema di coordinate del robot -
ma è essenziale per compiti come afferrare un oggetto in un punto
specifico dello spazio.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_pose(response_string):
    """Stessa idea di parse_angles() nell'esempio del movimento dei
    giunti, ma per leggere i valori X/Y/Z/Rx/Ry/Rz invece degli
    angoli dei giunti."""
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Cancellazione degli errori e abilitazione...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

print("Impostazione della velocità al 20%...")
print(dashboard.SpeedFactor(20))
sleep(0.5)

# Leggi la posizione attuale dell'utensile prima di muoverti.
current_pose = parse_pose(dashboard.GetPose())
print("Posa attuale (X, Y, Z, Rx, Ry, Rz):", current_pose)

# MovL(X, Y, Z, Rx, Ry, Rz, mode)
# IMPORTANTE: i numeri esatti qui sotto sono solo un ESEMPIO. Le
# coordinate Cartesiane dipendono interamente dalla posizione di
# montaggio del tuo robot e dal sistema di riferimento - copiare
# questi numeri direttamente nella tua configurazione potrebbe
# inviare il robot in un punto inatteso o irraggiungibile. Parti
# sempre da una posizione letta con GetPose() e apporta PICCOLE
# modifiche a partire da lì durante i test.
if current_pose:
    target_x = current_pose[0]
    target_y = current_pose[1]
    target_z = current_pose[2] + 50  # sposta 50mm verso l'alto, come esempio
    rx, ry, rz = current_pose[3], current_pose[4], current_pose[5]

    print(f"\nSpostamento di 50mm verso l'alto dalla posizione attuale...")
    result = dashboard.MovL(target_x, target_y, target_z, rx, ry, rz, 1)
    print(result)
    sleep(3)

    new_pose = parse_pose(dashboard.GetPose())
    print("Nuova posa:", new_pose)

    print("\nRitorno alla posizione originale...")
    dashboard.MovL(*current_pose, 1)
    sleep(3)
else:
    print("Impossibile leggere la posa attuale - movimento saltato per sicurezza.")

print("Disabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
