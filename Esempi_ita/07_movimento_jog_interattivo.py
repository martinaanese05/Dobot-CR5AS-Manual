"""
CONTROLLO INTERATTIVO DEI GIUNTI - un semplice menu per muovere un giunto alla volta
=====================================================================

Comandi trattati in questo file:
  - GetAngle()  legge tutti e sei gli angoli dei giunti
  - MovJ()      muove il robot (qui usato per un singolo giunto)

COSA FA QUESTO SCRIPT:
Invece di codificare una sequenza fissa di movimenti, questo
script chiede a TE, in un ciclo, quale giunto muovere e dove. È un
piccolo blocco di base per qualsiasi cosa tu voglia rendere
interattiva in seguito - ad esempio un pannello di jog
personalizzato, uno strumento di posizionamento manuale, oppure un
modo per esplorare in sicurezza il raggio di movimento del robot,
un giunto alla volta.

Ad ogni ciclo:
  1. Legge e mostra la posizione attuale di tutti e sei i giunti
  2. Chiede quale giunto (1-6) vuoi muovere
  3. Chiede a quale angolo muoverlo
  4. Chiede conferma prima di muoversi effettivamente
  5. Muove solo quel giunto, lasciando gli altri cinque intatti
Digita 'quit' al prompt del giunto per uscire.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_angles(response_string):
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Cancellazione degli errori e abilitazione...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

print("Impostazione della velocità al 50%...")
dashboard.SpeedFactor(50)
sleep(0.5)

print("\nControllo interattivo dei giunti")
print("Inserisci un numero di giunto (1-6) per muoverlo, oppure 'quit' per uscire.\n")

while True:
    # Rileggi sempre la posizione attuale ad ogni ciclo, poiché il
    # robot potrebbe essersi mosso dall'ultimo controllo.
    current_angles = parse_angles(dashboard.GetAngle())
    if current_angles is None:
        print("Impossibile leggere gli angoli dei giunti - arresto.")
        break

    print("\nPosizioni attuali dei giunti:")
    for i in range(6):
        print(f"  J{i+1}: {current_angles[i]:.4f}°")

    user_input = input("\nQuale giunto vuoi muovere? (1-6, oppure 'quit'): ").strip().lower()

    if user_input in ("quit", "exit"):
        break

    # Convalida il numero del giunto
    try:
        joint_num = int(user_input)
        if joint_num < 1 or joint_num > 6:
            print("Inserisci un numero tra 1 e 6.")
            continue
    except ValueError:
        print("Inserisci un numero tra 1 e 6.")
        continue

    # Chiedi l'angolo di destinazione
    target_input = input(f"Muovere J{joint_num} a quale angolo (gradi)? ").strip()
    try:
        target_angle = float(target_input)
    except ValueError:
        print("Inserisci un numero valido.")
        continue

    # Conferma prima di muoverti - sempre buona pratica per
    # qualsiasi cosa guidata da input dell'utente in tempo reale
    # piuttosto che da uno script fisso.
    confirm = input(f"Muovere J{joint_num} a {target_angle}°? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("Movimento annullato.")
        continue

    # Costruisci il comando completo a sei angoli, cambiando solo
    # il giunto scelto dall'utente e lasciando gli altri alle loro
    # posizioni attuali.
    move_angles = current_angles.copy()
    move_angles[joint_num - 1] = target_angle

    print(f"\nSpostamento di J{joint_num}...")
    result = dashboard.MovJ(*[float(a) for a in move_angles], 1)
    print(result)
    sleep(3)

print("\nDisabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
