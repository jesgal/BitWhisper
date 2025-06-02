import requests
import time
import random

# Compone mensaje a enviar
contentToSend = "Hola, ¿qué tal estás?"
endedWord     = "ENDED010203" # Palabra de control para indicar fin.
message       = f"{contentToSend}{endedWord}"

# Transforma el mensaje en bits.
bits = ''.join(format(ord(c), '08b') for c in message)
print("Mensaje a enviar en bits:", bits)

url = "http://localhost:5000/c2"

# Itera cada bit para transformar en tamaño variable
for bit in bits:
    if bit == '0': size = 200 # Tamaño 200 para bit 0
    else:          size = 300 # Tamaño 300 para bit 1
    # Creación del payload a enviar en la petición POST
    payload = b'a' * size

    # Establece rango de tiempo aleatorio para el envío de cada bit.
    seconds = random.uniform(0.001, 0.002)
    time.sleep(seconds)

    # Envío de la petición POST.
    response = requests.post(url, data=payload)
    print(f"Enviado bit {bit} con tamaño {size}, respuesta: {response.status_code}")