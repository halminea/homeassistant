from ruuvitag_sensor.ruuvi import RuuviTagSensor
import json

def handle_data(found_data):
    # Muutetaan json-muotoon ja kirjoitetaan tiedostoon.
    with open("/usr/share/hassio/homeassistant/tag1.json", "w") as fp:
        json.dump(found_data[1], fp)

# Vain saunan mittari: 
mac = 'D7:FE:5A:B0:AB:59'

# Tämä pyörittää etsintää ad infinitum
RuuviTagSensor.get_datas(handle_data, mac)