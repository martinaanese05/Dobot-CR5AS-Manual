"""
HELLO WORLD - Il tuo primo script per il Dobot CR5AS
=============================================

Cosa fa questo script, passo per passo:
  1. Si connette al robot in rete (porta Dashboard 29999)
  2. Cancella eventuali errori residui e abilita (accende) il robot
  3. Muove TUTTI i giunti alla posizione di 0 gradi
  4. Muove il giunto 0 (la base, J1) a -30 gradi
  5. Muove il giunto 0 di nuovo a +30 gradi
  6. Muove il giunto 0 a +30 gradi un'altra volta (passo ripetuto -
     se ti servono solo due movimenti, sentiti libero di eliminare
     quest'ultimo)
  7. Stampa cosa sta facendo a ogni passo, e disabilita il robot
     al termine

Questo NON richiede di capire la robotica - serve a mostrarti la
"forma" di base che avrà ogni script per Dobot:
  connetti -> abilita -> muovi -> disabilita
"""

from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

# ---------------------------------------------------------------
# PASSO 1: Impostazioni di connessione
# ---------------------------------------------------------------
# Sostituisci questo con l'indirizzo IP REALE del tuo robot.
# Puoi trovarlo nella schermata di connessione di DobotStudio Pro,
# oppure controllando la sezione Password e Connettività di questo
# manuale.
IP = "192.168.201.1"
DASHBOARD_PORT = 29999

# Questa riga apre la connessione. Da questo punto in poi,
# "dashboard" è il nostro telecomando per il robot - ogni comando
# qui sotto viene inviato attraverso di esso.
dashboard = DobotApiDashboard(IP, DASHBOARD_PORT)


# ---------------------------------------------------------------
# PASSO 2: Cancella gli errori e abilita il robot
# ---------------------------------------------------------------
# ClearError() azzera qualsiasi allarme rimasto da una sessione
# precedente. È buona pratica chiamarlo sempre prima di abilitare.
print("Cancellazione degli errori precedenti...")
print(dashboard.ClearError())
sleep(0.5)  # Una breve pausa dà al robot il tempo di elaborare il comando

# EnableRobot() accende i motori. Il robot non si muoverà affatto
# finché questo non va a buon fine - se fallisce, controlla che:
#   - l'indirizzo IP sopra sia corretto
#   - il robot sia impostato in modalità TCP (vedi la sezione sulla
#     modalità TCP)
print("Abilitazione del robot...")
print(dashboard.EnableRobot())
sleep(1)


# ---------------------------------------------------------------
# PASSO 3: Imposta una velocità sicura prima di muoverti
# ---------------------------------------------------------------
# SpeedFactor prende una percentuale (1-100). Si consiglia
# vivamente di iniziare lentamente (es. 20%) mentre si testano
# nuovi script.
print("Impostazione della velocità al 20%...")
print(dashboard.SpeedFactor(20))
sleep(0.5)


# ---------------------------------------------------------------
# PASSO 4: Muovi tutti i giunti a 0 gradi
# ---------------------------------------------------------------
# MovJ() muove il robot usando un movimento nello spazio dei giunti
# (ogni giunto ruota direttamente verso il suo angolo di
# destinazione - questa NON è una linea retta nello spazio, solo il
# modo più semplice di muoversi).
#
# I sei numeri sono l'angolo di destinazione per i giunti da J1 a
# J6, in gradi. L'ultimo "1" dice al robot "questi sono angoli dei
# giunti" (e non coordinate X/Y/Z).
print("\nSpostamento di tutti i giunti a 0 gradi...")
result = dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)  # Dai al robot il tempo di finire il movimento prima di continuare


# ---------------------------------------------------------------
# PASSO 5: Muovi il giunto della base (J1) a -30, poi +30, poi di nuovo +30
# ---------------------------------------------------------------
# Qui cambia solo il PRIMO numero - quello è J1, il giunto della
# base, quello che ruota tutto il braccio a sinistra/destra. Gli
# altri cinque restano a 0.

print("\nSpostamento del giunto base (J1) a -30 gradi...")
result = dashboard.MovJ(-30, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)

print("\nSpostamento del giunto base (J1) a +30 gradi...")
result = dashboard.MovJ(30, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)

print("\nSpostamento del giunto base (J1) a +30 gradi di nuovo...")
result = dashboard.MovJ(30, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)

print("\nSpostamento di tutti i giunti a 0 gradi...")
result = dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)


# ---------------------------------------------------------------
# PASSO 6: Disabilita il robot al termine
# ---------------------------------------------------------------
# Disabilita sempre il robot alla fine di uno script. Questo
# interrompe l'alimentazione dei motori in modo controllato,
# anziché lasciarlo abilitato.
print("\nDisabilitazione del robot...")
dashboard.DisableRobot()

print("Fatto! Ciao, Dobot.")
