import serial
import yagmail
import time
import re

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

sender = 'luxwheeluca21@gmail.com'
receiver = ''
app_password = 'atxi fxfd sgtr byvk'

yag = yagmail.SMTP(sender, app_password)

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
time.sleep(2)
ser.reset_input_buffer()

last_value = None
last_sent_time = 0

def extraire_valeur(ligne):
    match = re.search(r"(\d+(\.\d+)?)", ligne)
    if match:
        return float(match.group(1))
    return None

while True:
    if ser.in_waiting > 0:
        ligne = ser.readline().decode('utf-8', errors='replace').strip()
        print("Reçu :", repr(ligne))

        if "Light" in ligne:
            valeur = extraire_valeur(ligne)
            if valeur is not None:
                maintenant = time.time()
                if valeur != last_value and (maintenant - last_sent_time) > 60:
                    print(f"Nouvelle mesure détectée : {valeur} lux, envoi email...")
                    try:
                        yag.send(
                            to=receiver,
                            subject="Mesure de luminosité LuxWheel",
                            contents=f"Nouvelle mesure de luminosité : {ligne}"
                        )
                        print("Email envoyé.")
                        last_value = valeur
                        last_sent_time = maintenant
                    except Exception as e:
                        print("Erreur lors de l'envoi de l'email :", e)
                else:
                    print("Valeur inchangée ou délai non écoulé, pas d'email envoyé.")
            else:
                print("Impossible d'extraire la valeur numérique.")
    else:
        time.sleep(0.1)

