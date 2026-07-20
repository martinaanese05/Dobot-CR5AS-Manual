"""
MODALITÀ DRAG - guidare manualmente il robot con le mani
==============================================

Comandi trattati in questo file:
  - StartDrag()  mette il robot in modalità drag/apprendimento
  - StopDrag()   fa uscire il robot dalla modalità drag

La modalità drag ti permette di afferrare fisicamente il braccio
del robot e muoverlo a mano - i motori diventano abbastanza
"liberi" da poter essere spinti, mentre il robot continua a
tracciare la propria posizione. Questo viene comunemente usato per:
  - guidare manualmente il robot fino a una posizione, e poi
    leggere quella posizione con GetAngle() / GetPose() per
    riutilizzarla in uno script
  - testare rapidamente la raggiungibilità di un punto senza
    programmarlo

NOTA DI SICUREZZA: anche in modalità drag, il robot rimane acceso.
Si applicano comunque i protocolli di sicurezza standard (spazio
libero, attenzione, e-stop a portata di mano).
"""

from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)

print("Cancellazione degli errori e abilitazione...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

# StartDrag() mette il robot in uno stato "libero", guidabile a mano.
print("\nAvvio della modalità drag - ora puoi muovere il braccio a mano.")
print(dashboard.StartDrag())

# In uno script reale, normalmente ti fermeresti qui e lasceresti
# che una persona muova fisicamente il robot, per poi leggerne la
# posizione. Simuliamo questa pausa con input() così lo script
# aspetta te.
input("Muovi il robot a mano, poi premi Invio qui per continuare...")

# GetAngle() ti permette di leggere dove è finito il robot dopo
# essere stato trascinato - utile per registrare una posizione
# appresa.
print("Posizione dopo il trascinamento:", dashboard.GetAngle())

# StopDrag() esce dalla modalità drag e torna al funzionamento
# normale - il robot terrà di nuovo la sua posizione in modo rigido.
print("\nArresto della modalità drag...")
print(dashboard.StopDrag())

sleep(1)
print("Disabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
