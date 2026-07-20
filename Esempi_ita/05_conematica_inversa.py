"""
CINEMATICA INVERSA - convertire X/Y/Z in angoli dei giunti
==========================================================

Comandi trattati in questo file:
  - InverseKin()  converte un target Cartesiano (X/Y/Z/Rx/Ry/Rz)
                  negli angoli dei giunti (J1-J6) necessari per
                  raggiungerlo

PERCHÉ QUESTO È IMPORTANTE:
Sia MovL() che MovJ() accettano coordinate Cartesiane o angoli dei
giunti a seconda del flag di modalità - ma a volte vuoi sapere IN
ANTICIPO a quali angoli dei giunti corrisponde una posizione di
destinazione, senza effettivamente muoverti lì. Ad esempio:
  - verificare se un target è addirittura raggiungibile prima di
    impegnarsi nel movimento
  - confrontare gli angoli dei giunti tra diverse posizioni candidate

InverseKin() fa i calcoli al posto tuo: dagli una posizione di
destinazione nello spazio, e calcola gli angoli dei giunti
corrispondenti.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_values(response_string):
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Cancellazione degli errori e abilitazione...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

# Leggi la posizione attuale del robot, solo per avere un target
# realistico con cui fare i test (posizioni vicine e raggiungibili).
current_pose = parse_values(dashboard.GetPose())
print("Posa attuale:", current_pose)

if current_pose:
    # Costruisci un target di esempio: stessa posizione, ma 30mm più in alto.
    target = current_pose.copy()
    target[2] += 30  # Asse Z, sposta 30mm verso l'alto

    # InverseKin(X, Y, Z, Rx, Ry, Rz) - chiedi al robot "se volessi
    # trovarmi a QUESTA posizione, di quali angoli dei giunti
    # avrei bisogno?"
    # NOTA: questo NON muove il robot - calcola soltanto.
    print(f"\nCalcolo degli angoli dei giunti per il target: {target}")
    result = dashboard.InverseKin(*target)
    print("Risultato:", result)

    calculated_angles = parse_values(result)
    if calculated_angles:
        print("Angoli dei giunti necessari per raggiungere questa posizione:")
        joint_names = ["J1", "J2", "J3", "J4", "J5", "J6"]
        for name, angle in zip(joint_names, calculated_angles):
            print(f"  {name}: {angle:.4f} gradi")
else:
    print("Impossibile leggere la posa attuale.")

print("\nDisabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
