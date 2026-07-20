"""
TEST DI CONFRONTO VELOCITÀ - vedere direttamente l'effetto di SpeedFactor
================================================================

Comandi trattati in questo file:
  - SpeedFactor()  imposta la percentuale di velocità globale
  - MovJ()         muove il robot
  - GetAngle()     conferma dove è finito il robot

COSA FA QUESTO SCRIPT:
Esegue esattamente lo stesso movimento - il giunto 1 (la base) da
0° a 180° - a cinque diverse impostazioni di velocità di fila: 10%,
25%, 50%, 75% e 100%. Tra un test e l'altro, torna prima a 0°, così
ogni test parte dallo stesso punto.

PERCHÉ È UTILE:
SpeedFactor è facile da leggere ma difficile da capire finché non
lo VEDI - questo script ti permette di osservare direttamente (e
cronometrare, se aggiungi un cronometro) come lo stesso movimento
si percepisce a velocità diverse. È anche un buon script da usare
quando si regola la velocità di un nuovo script prima di decidere
quale valore codificare altrove.

NOTA DI SICUREZZA: la velocità al 100% è inclusa qui per
confronto, ma eseguire movimenti non familiari a piena velocità non
è generalmente consigliato. Assicurati che l'area di lavoro sia
completamente libera prima di eseguire questo file.
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

speeds_to_test = [10, 25, 50, 75, 100]

for speed in speeds_to_test:
    print(f"\n{'='*50}")
    print(f"Test velocità: {speed}%")
    print(f"{'='*50}")

    dashboard.SpeedFactor(speed)
    sleep(1)

    # Inizia sempre ogni test dalla stessa posizione (0 gradi),
    # così il confronto tra le velocità è equo.
    print("Spostamento di J1 a 0°...")
    dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
    sleep(3)

    start_angles = parse_angles(dashboard.GetAngle())
    print(f"Posizione di partenza: J1 = {start_angles[0]:.4f}°")

    print(f"Spostamento di J1 a 180° a velocità {speed}%...")
    dashboard.MovJ(180, 0, 0, 0, 0, 0, 1)
    sleep(5)  # attesa generosa, poiché le velocità più lente richiedono più tempo

    end_angles = parse_angles(dashboard.GetAngle())
    print(f"Posizione finale: J1 = {end_angles[0]:.4f}°")
    print(f"Velocità {speed}% completata.")

# Torna a una posizione sicura e conosciuta al termine.
print("\nRitorno di J1 a 0°...")
dashboard.SpeedFactor(50)
sleep(0.5)
dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
sleep(3)

print("\nDisabilitazione del robot...")
dashboard.DisableRobot()
print("Fatto!")
