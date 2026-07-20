"""
PINZA: INIZIALIZZAZIONE, APERTURA, CHIUSURA - basato sul progetto Robot Barman
=========================================================================

Questo esempio rispecchia esattamente come viene controllata la
pinza nel progetto Robot Barman - tre script Lua con nome
memorizzati sul controller del robot ("gripper_init", "gripper_open",
"gripper_close"), ciascuno attivato allo stesso modo: chiudi il
Dashboard, invia lo script tramite un socket grezzo, aspetta, poi
riconnetti il Dashboard.

PERCHÉ "INIZIALIZZAZIONE" È UN PASSO SEPARATO:
Alcune pinze necessitano di una routine di inizializzazione/homing
una tantum prima di rispondere in modo affidabile ai comandi di
apertura/chiusura - in modo simile a come una stampante 3D esegue
l'homing dei propri assi prima di stampare. In Robot Barman, questo
viene eseguito una volta all'inizio di una sessione (`gripper_init`),
prima che vengano inviati comandi di apertura/chiusura.

LEZIONE IMPORTANTE DA ROBOT BARMAN (la parte più insidiosa di questo):
Ogni volta che viene eseguito uno script della pinza, la connessione
Dashboard viene chiusa e riaperta dietro le quinte. Questo può
lasciare silenziosamente il robot in uno stato in cui i comandi
MovJ/MovL vengono IGNORATI, anche se apparentemente non sembra
nulla di sbagliato. La soluzione usata in tutto Robot Barman è
chiamare sempre di nuovo ClearError() + EnableRobot() subito dopo
qualsiasi azione della pinza, prima di provare a muovere il
braccio. Questo esempio segue lo stesso schema di sicurezza.

REQUISITO: questo presuppone che gli script "gripper_init",
"gripper_open" e "gripper_close" esistano già sul controller del
tuo robot. Questo script si limita ad attivarli, non li crea.
"""

import socket
from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
PORT = 29999


def run_gripper_script(dashboard, script_name):
    """
    Esegue uno script Lua con nome memorizzato sul controller del
    robot. Restituisce un oggetto dashboard (possibilmente nuovo),
    poiché la connessione viene chiusa e ricreata come parte di
    questo processo.
    """
    print(f"Esecuzione dello script della pinza: {script_name}")

    # Passo 1: chiudi la connessione Dashboard attuale per liberare la porta
    if dashboard:
        try:
            dashboard.close()
        except Exception:
            pass
        sleep(1.0)

    # Passo 2: apri un socket grezzo e invia direttamente il comando RunScript
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5)
        sock.connect((IP, PORT))

        sock.sendall((f"RunScript({script_name})\n").encode())
        sleep(1.0)

        try:
            response = sock.recv(1024)
            print("Risposta della pinza:", response.decode().strip())
        except socket.timeout:
            print("Nessuna risposta dalla pinza (timeout)")
    except Exception as e:
        print(f"Errore nell'esecuzione dello script della pinza: {e}")
    finally:
        try:
            sock.close()
        except Exception:
            pass

    # Passo 3: riconnetti il Dashboard
    new_dashboard = DobotApiDashboard(IP, PORT)
    sleep(0.5)
    return new_dashboard


def ensure_motion_ready(dashboard):
    """
    Riarma il robot per il movimento dopo che è stato eseguito uno
    script della pinza. Questo è il passo critico su cui si basa
    Robot Barman - senza di esso, la pinza sembra funzionare, ma il
    braccio ignora silenziosamente qualsiasi comando MovJ/MovL
    inviato successivamente.
    """
    try:
        dashboard.ClearError()
        sleep(0.5)
        dashboard.EnableRobot()
        sleep(1)
        print("Braccio riarmato per il movimento (errori cancellati, robot abilitato)")
    except Exception as e:
        print(f"Attenzione: impossibile riarmare il robot per il movimento: {e}")


# ---- Script principale ----

dashboard = DobotApiDashboard(IP, PORT)

print("Cancellazione degli errori e abilitazione...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

# FASE 1: Inizializza la pinza (una tantum, all'inizio di una sessione)
print("\nInizializzazione della pinza...")
dashboard = run_gripper_script(dashboard, "gripper_init")
sleep(5)  # gripper_init ha bisogno di tempo per completarsi del tutto prima di qualsiasi altra cosa

# Gli script della pinza chiudono/riaprono il Dashboard - riarma
# sempre il robot per il movimento in seguito, anche se non ti
# stai ancora muovendo.
ensure_motion_ready(dashboard)

# FASE 2: Chiudi la pinza
print("\nChiusura della pinza...")
dashboard = run_gripper_script(dashboard, "gripper_close")
ensure_motion_ready(dashboard)

sleep(3)

# FASE 3: Apri la pinza
print("\nApertura della pinza...")
dashboard = run_gripper_script(dashboard, "gripper_open")
ensure_motion_ready(dashboard)

print("\nDisabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
