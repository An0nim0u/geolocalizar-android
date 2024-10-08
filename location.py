import requests
import os
import time

# URL del servidor
url = "https://1641-186-166-142-157.ngrok-free.app"

def obtener_gps():
    os.system('gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock')
    
    while True:
        # Obtenemos datos del GPS
        stream = os.popen('gpspipe -w -n 10')
        for line in stream:
            try:
                # Parseamos los datos JSON del GPS
                if '"class":"TPV"' in line:
                    data = json.loads(line)
                    latitud = data.get('lat')
                    longitud = data.get('lon')
                    geolocalizacion = data.get('mode')
                    
                    if latitud and longitud:
                        enviar_datos(latitud, longitud, geolocalizacion)
            except Exception as e:
                print(f"Error: {e}")

def enviar_datos(latitud, longitud, geolocalizacion):
    payload = {
        'latitud': latitud,
        'longitud': longitud,
        'geolocalizacion': geolocalizacion
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Datos enviados con éxito.")
        else:
            print(f"Error al enviar datos: {response.status_code}")
    except Exception as e:
        print(f"Error en la solicitud: {e}")

if __name__ == "__main__":
    obtener_gps()
