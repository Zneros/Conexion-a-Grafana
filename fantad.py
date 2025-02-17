import network
import urequests
import time
import random
import gc  

SSID = "aqui pon tu ssid de tu wifi"
PASSWORD = "aqui pon tu password de tu wifi"
SERVER_URL = "aqui debes de poner la ip de tu laptop, si no te la sabes es con ipconfig y en IPv4 despues se pone el puerto de de nodered" # ejemplo: http://192.168.1.33:1880/data

wlan = network.WLAN(network.STA_IF)

def connect_wifi():
    global wlan  
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Conectando a WiFi...")
    attempt = 0
    while not wlan.isconnected():
        attempt += 1
        if attempt > 15:
            print("No se pudo conectar a WiFi. Reiniciando...")
            machine.reset()
        time.sleep(1)

    print("WiFi conectado. IP:", wlan.ifconfig()[0])

def send_data(sensor):
    value = random.randint(0, 100)
    data = {"sensor": sensor, "value": value}
    headers = {"Content-Type": "application/json"}

    try:
        print(f"Enviando datos: {data}")
        response = urequests.post(SERVER_URL, json=data, headers=headers, timeout=5)
        print(f"Respuesta del servidor: {response.status_code} - {response.text}")
        response.close()
    except Exception as e:
        print(f"Error enviando datos: {e}")

connect_wifi()

while True:
    if not wlan.isconnected():
        print("WiFi desconectado, reconectando...")
        connect_wifi()
    
    send_data("temperatura")
    gc.collect()  
    time.sleep(20)


