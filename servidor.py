from flask import Flask, request

# Instancia flask
app = Flask(__name__)

# Define variable
receivedBits   = []
contentReceived = ''

# Crea ruta de acceso con método POST
@app.route('/c2', methods=['POST'])
def c2_endpoint():
    global contentReceived
    # Obtiene el largo del payload recibido
    contentLength = request.content_length
    # Si no contiene payload indica error.
    if contentLength is None: return 'No content length', 400
    # Define umbral para interpretar bit
    if contentLength == 200: bit = '0' # Tamaño payload 200
    else:                    bit = '1' # Tamaño payload 300

    # Añade bit a lista bits
    receivedBits.append(bit)
    # Decodifica cada conjunto de 8 bits (1 byte) a texto.
    if len(receivedBits) % 8 == 0:
        # Decodifica cada byte
        byteString      = ''.join(receivedBits[-8:])
        # Transforma en carácter
        contentReceived += chr(int(byteString, 2))
        # Limpia la lista
        receivedBits.clear()

        # Identifica si se ha recibido la palabra de fin emisión.
        if "ENDED010203" in contentReceived:
            # Elimina palabra final
            contentReceived = contentReceived.replace("ENDED010203","")
            # Imprime el resultado
            print(f"Contenido recibido: '{contentReceived}'")
            # Limpia la variable
            contentReceived = ""
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)