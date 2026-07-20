"""
TRASCINA, REGISTRA E RIPRODUCI - insegnare al robot una sequenza di punti
======================================================================

Comandi trattati in questo file:
  - StartDrag() / StopDrag()  entra ed esce dalla modalità drag guidata a mano
  - GetAngle()                legge gli angoli dei giunti a ogni punto registrato
  - MovJ()                    riproduce ogni punto registrato in ordine

COSA FA QUESTO SCRIPT:
  1. Si sposta nella posizione home (tutti i giunti a 0)
  2. Mette il robot in modalità drag, così puoi muoverlo a mano
  3. Ogni volta che premi INVIO, registra gli angoli dei giunti
     ATTUALI come un "punto" in una lista
  4. Quando digiti "stop", esce dalla modalità drag
  5. Poi riproduce automaticamente ogni punto registrato, in ordine
  6. Infine, torna alla posizione home

PERCHÉ È UTILE:
Questo è il modo in cui "insegni" al robot una sequenza di
posizioni senza scrivere tu stesso le coordinate - lo mostri
fisicamente dove andare, e lo script se lo ricorda. Questa è la
stessa tecnica usata per costruire cose come le routine di
pick-and-place: trascina fino a ogni posizione una volta, poi
lascia che lo script la ripeta all'infinito.

NOTA DI SICUREZZA: anche in modalità drag, il robot è acceso.
Mantieni l'area di lavoro libera e l'e-stop a portata di mano
mentre lo trascini a mano.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_angles(response_string):
    """Estrae i sei numeri degli angoli dei giunti dal testo di risposta del robot."""
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


def move_to_angles(angles, label="posizione"):
    """Invia un comando MovJ agli angoli dei giunti indicati, aspetta
    che finisca, poi stampa dove è effettivamente finito il robot."""
    print(f"\nSpostamento verso {label}...")
    result = dashboard.MovJ(*angles, 1)
    print(result)
    sleep(3)  # attesa grezza - abbastanza buona per scopi di apprendimento

    current = parse_angles(dashboard.GetAngle())
    if current:
        print(f"Arrivato a {label}:")
        for i in range(6):
            print(f"  J{i+1}: {current[i]:.4f}°")


# ---------------------------------------------------------------
# PASSO 1: Parti da una posizione conosciuta
# ---------------------------------------------------------------
print("Cancellazione degli errori e abilitazione...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

print("Impostazione della velocità al 50%...")
dashboard.SpeedFactor(50)
sleep(0.5)

move_to_angles([0, 0, 0, 0, 0, 0], label="posizione HOME")


# ---------------------------------------------------------------
# PASSO 2: Entra in modalità drag e registra i punti
# ---------------------------------------------------------------
recorded_points = []

confirm = input("\nEntrare in modalità drag per registrare i punti? (yes/no): ").strip().lower()

if confirm in ("yes", "y"):
    print("\nIngresso in modalità drag - il robot diventerà libero e potrà essere mosso a mano.")
    print(dashboard.StartDrag())
    sleep(2)

    print("\nMuovi il robot in una posizione, poi premi INVIO per registrarla.")
    print("Digita 'stop' e premi INVIO quando hai finito di registrare.\n")

    while True:
        user_input = input("Premi INVIO per registrare, oppure digita 'stop': ").strip().lower()

        if user_input == "stop":
            break

        angles = parse_angles(dashboard.GetAngle())
        if angles:
            recorded_points.append(angles)
            print(f"Punto {len(recorded_points)} registrato:")
            for i in range(6):
                print(f"  J{i+1}: {angles[i]:.4f}°")
        else:
            print("Impossibile leggere una posizione - riprova.")

    print("\nUscita dalla modalità drag...")
    print(dashboard.StopDrag())
    sleep(2)
else:
    print("Modalità drag saltata - nessun punto registrato.")


# ---------------------------------------------------------------
# PASSO 3: Riproduci la sequenza registrata
# ---------------------------------------------------------------
if recorded_points:
    print(f"\nRiproduzione di {len(recorded_points)} punti registrati...")

    # Dopo la modalità drag, il robot a volte deve essere
    # riabilitato prima di accettare di nuovo i comandi di movimento.
    dashboard.ClearError()
    sleep(1)
    dashboard.EnableRobot()
    sleep(2)
    dashboard.SpeedFactor(50)
    sleep(0.5)

    move_to_angles([0, 0, 0, 0, 0, 0], label="posizione HOME")

    for i, point in enumerate(recorded_points, start=1):
        move_to_angles(point, label=f"PUNTO {i}")

    move_to_angles([0, 0, 0, 0, 0, 0], label="posizione HOME")

    print(f"\nSequenza completata - riprodotti {len(recorded_points)} punti.")
else:
    print("\nNessun punto è stato registrato, niente da riprodurre.")

print("\nDisabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
