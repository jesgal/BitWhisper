# 🕵️‍♂️ BitWhisper

**BitWhisper** es un proyecto que demuestra el uso de un canal encubierto usando peticiones HTTP POST con tamaños de payload variables para transmitir datos de forma sigilosa entre un cliente y un servidor.

Las técnicas de canal encubierto se utilizan comúnmente en el ámbito de la ciberseguridad ofensiva para evadir medidas de control de análisis de tráfico.

---

## 🔐 ¿Para qué sirve?

Este proyecto puede utilizarse para:

- Demostrar técnicas de evasión y canales encubiertos.
- Investigar mecanismos de detección de tráfico anómalo.
- Aprender sobre codificación binaria y manipulación de tráfico HTTP.

---

## 🧠 ¿Qué es BitWhisper?

BitWhisper permite transmitir mensajes sin usar el contenido del mensaje como tal, para ello hace uso del **el tamaño del contenido**. El servidor interpreta el tamaño de cada payload recibido para reconstruir el mensaje bit a bit, pasando desapercibido para tecnologías de detección que no inspeccionan la inspección de tráfico de forma profunda o la identificación de tráfico anómalo.

---

## 📂 Estructura del proyecto

bitwhisper/

├── cliente.py  # Cliente que codifica y envía el mensaje como tamaños de payload.

├── servidor.py # Servidor que decodifica los tamaños en bits y reconstruye el mensaje.

└── README.md

---

## 🚀 Cómo ejecutar

### 1. Requisitos

- Python 3.x
- Flask
- Requests

Instala las dependencias con pip:

```bash
pip install flask requests
````


### 2. Ejecuta el servidor

```bash
python servidor.py
````
Esto iniciará un servidor HTTP en `http://localhost:5000`.


### 3. Ejecuta el cliente

```bash
python cliente.py
````
El cliente enviará un mensaje codificado bit a bit usando:

- `0` → payload de 200 bytes
- `1` → payload de 300 bytes

El servidor reconstruirá el mensaje y lo mostrará por consola cuando detecte el marcador de fin (`ENDED010203`).

---

## ⚠️ USO

**Este proyecto es solo para fines educativos y de investigación.**

Está diseñado para ayudar a comprender cómo funcionan los canales encubiertos y las técnicas de transmisión de mensajes encubiertos a través de protocolo de comunicación de capa 7. No debe utilizarse para actividades ilegales, maliciosas o no autorizadas.

El uso indebido de este código para exfiltración de datos o evasión de sistemas de seguridad puede quebrantar las regulaciones locales, nacionales o internacionales, así como las políticas corporativas.

Al usar este proyecto, asumes toda la responsabilidad y te comprometes a respetar la ética y las normativas vigentes.
