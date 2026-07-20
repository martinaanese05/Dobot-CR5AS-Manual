"""
SPOSTAMENTO ALLA POSIZIONE RAGGIUNGIBILE PIÙ VICINA - gestire target irraggiungibili
======================================================================

Comandi trattati in questo file:
  - MovL()    tenta uno spostamento in linea retta verso un target Cartesiano
  - GetPose() legge la posizione attuale X/Y/Z/Rx/Ry/Rz

IL PROBLEMA CHE RISOLVE:
Non tutte le coordinate X/Y/Z che puoi digitare sono effettivamente
raggiungibili - il robot ha un raggio di lavoro limitato, e alcune
posizioni sono al di fuori di esso, oppure sono angolazioni scomode
che il braccio non può fisicamente raggiungere. Se invii un target
irraggiungibile con MovL(), il robot semplicemente rifiuterà il
comando e resterà dove si trova.

L'APPROCCIO DI QUESTO SCRIPT:
Invece di arrendersi al primo fallimento, tenta il target, e se
fallisce, si ritira passo dopo passo - prima abbassando Z
(l'altezza), poi Y, poi X - riprovando ogni volta, finché non
trova una posizione che il robot PUÒ raggiungere, oppure rinuncia
dopo un numero prefissato di tentativi.

Questa è una strategia semplice, "abbastanza buona" - non
garantisce il punto raggiungibile assolutamente più vicino, solo
uno nelle vicinanze trovato per tentativi ed errori. Per
applicazioni in cui "più vicino" deve essere matematicamente
preciso, servirebbe invece un controllo di raggiungibilità basato
su una vera cinematica.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_pose(response_string):
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


def try_position(x, y, z, rx, ry, rz, step_size=10, max_attempts=20):
    """
    Tenta di spostarsi verso (x, y, z). Se il movimento fallisce, si
    ritira in Z, poi Y, poi X, a piccoli passi, e riprova - fino a
    max_attempts volte.

    Restituisce (success, final_x, final_y, final_z) - la posizione
    che ha effettivamente tentato, sia che abbia avuto successo o meno.
    """
    current_x, current_y, current_z = x, y, z

    for attempt in range(max_attempts):
        result = dashboard.MovL(current_x, current_y, current_z, rx, ry, rz, 1)
        result_str = str(result)

        # Un risultato che inizia con "0," generalmente significa successo.
        # Qualsiasi altra cosa di solito indica che il movimento è stato rifiutato.
        if result_str.startswith("0,"):
            print(f"  Successo a X={current_x:.1f}, Y={current_y:.1f}, Z={current_z:.1f}")
            sleep(3)
            return True, current_x, current_y, current_z

        print(f"  Irraggiungibile a X={current_x:.1f}, Y={current_y:.1f}, Z={current_z:.1f}, ritiro in corso...")

        # Prova prima ad abbassare Z (di solito l'asse più flessibile),
        # poi Y, poi X, finché non finisce lo spazio per ritirarsi.
        if current_z > 50:
            current_z -= step_size
        elif current_y > 0:
            current_y -= step_size
        elif current_x > 100:
            current_x -= step_size
        else:
            print("  Spazio per ritirarsi esaurito - rinuncio.")
            break

        sleep(0.5)

    return False, current_x, current_y, current_z


print("Cancellazione degli errori e abilitazione...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

print("Impostazione della velocità al 40%...")
dashboard.SpeedFactor(40)
sleep(0.5)

print("\nSpostamento verso la posizione HOME...")
dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
sleep(3)

current_pose = parse_pose(dashboard.GetPose())
if current_pose:
    print(f"Posizione attuale: X={current_pose[0]:.2f}, Y={current_pose[1]:.2f}, Z={current_pose[2]:.2f}")

print("\nInserisci le coordinate target X Y Z, 'home' per tornare alla posizione home, oppure 'quit' per uscire.\n")

while True:
    user_input = input("Target (X Y Z), oppure comando: ").strip().lower()

    if user_input in ("quit", "exit"):
        break

    if user_input == "home":
        print("Spostamento verso HOME...")
        dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
        sleep(3)
        continue

    coords = user_input.split()
    if len(coords) != 3:
        print("Inserisci esattamente 3 valori: X Y Z")
        continue

    try:
        target_x, target_y, target_z = (float(c) for c in coords)
    except ValueError:
        print("Inserisci numeri validi.")
        continue

    print(f"\nTentativo di raggiungere X={target_x:.1f}, Y={target_y:.1f}, Z={target_z:.1f}...")
    success, final_x, final_y, final_z = try_position(target_x, target_y, target_z, 0, 0, 0)

    if success:
        print(f"Target raggiunto (o corrispondenza esatta): X={final_x:.1f}, Y={final_y:.1f}, Z={final_z:.1f}")
    else:
        print(f"Impossibile raggiungere il target. Il miglior tentativo è stato: X={final_x:.1f}, Y={final_y:.1f}, Z={final_z:.1f}")

print("\nSpostamento verso HOME...")
dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
sleep(3)

print("Disabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
