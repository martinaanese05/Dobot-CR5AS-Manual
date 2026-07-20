"""
REGISTRAZIONE DI PUNTI CARTESIANI - trascina, registra posizioni X/Y/Z e riproduci
========================================================================

Comandi trattati in questo file:
  - StartDrag() / StopDrag()  modalità drag guidata a mano
  - GetPose()                 legge X/Y/Z/Rx/Ry/Rz (non gli angoli dei giunti)
  - MovL()                    riproduce ogni punto in linea retta

IN COSA DIFFERISCE DA 06_drag_record_and_replay.py:
Quel file registrava e riproduceva ANGOLI DEI GIUNTI (usando
GetAngle e MovJ). Questo invece registra e riproduce POSIZIONI
CARTESIANE (usando GetPose e MovL) - il che significa che ricorda
DOVE si trova qualcosa nello spazio fisico (coordinate X/Y/Z), non
a quale angolo si trovava ciascun giunto.

PERCHÉ QUESTO È IMPORTANTE:
Se ti interessa solo "metti l'utensile esattamente in questo punto
nello spazio", i punti Cartesiani sono di solito il modo più
naturale di ragionarci - specialmente per compiti come afferrare un
oggetto in una posizione specifica. MovL viaggia anche in linea
retta tra i punti, a differenza di MovJ.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_pose(response_string):
    """Estrae X, Y, Z, Rx, Ry, Rz dal testo di risposta del robot."""
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Cancellazione degli errori e abilitazione...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

print("Impostazione della velocità al 40%...")
dashboard.SpeedFactor(40)
sleep(0.5)

recorded_poses = []

confirm = input("Entrare in modalità drag per registrare punti Cartesiani? (yes/no): ").strip().lower()

if confirm in ("yes", "y"):
    print("\nIngresso in modalità drag...")
    dashboard.StartDrag()
    sleep(2)

    print("Muovi il robot in una posizione, poi premi INVIO per registrarla.")
    print("Digita 'stop' e premi INVIO quando hai finito.\n")

    while True:
        user_input = input("Premi INVIO per registrare, oppure digita 'stop': ").strip().lower()
        if user_input == "stop":
            break

        pose = parse_pose(dashboard.GetPose())
        if pose:
            recorded_poses.append(pose)
            print(f"Punto {len(recorded_poses)} registrato:")
            print(f"  X={pose[0]:.2f}, Y={pose[1]:.2f}, Z={pose[2]:.2f}, "
                  f"Rx={pose[3]:.2f}, Ry={pose[4]:.2f}, Rz={pose[5]:.2f}")
        else:
            print("Impossibile leggere una posa - riprova.")

    print("\nUscita dalla modalità drag...")
    dashboard.StopDrag()
    sleep(2)
else:
    print("Modalità drag saltata - nessun punto registrato.")

if recorded_poses:
    print(f"\nRiproduzione di {len(recorded_poses)} punti registrati usando MovL...")

    dashboard.ClearError()
    sleep(1)
    dashboard.EnableRobot()
    sleep(2)
    dashboard.SpeedFactor(40)
    sleep(0.5)

    for i, pose in enumerate(recorded_poses, start=1):
        print(f"\nSpostamento verso il PUNTO {i}...")
        result = dashboard.MovL(*pose, 1)
        print(result)
        sleep(3)

        actual = parse_pose(dashboard.GetPose())
        if actual:
            print(f"Arrivato vicino a: X={actual[0]:.2f}, Y={actual[1]:.2f}, Z={actual[2]:.2f}")

    print(f"\nSequenza completata - riprodotti {len(recorded_poses)} punti.")
else:
    print("\nNessun punto è stato registrato, niente da riprodurre.")

print("\nDisabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
