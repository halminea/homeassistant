from ruuvitag_sensor.ruuvi import RuuviTagSensor
import json

def handle_data(found_data):
    # Muutetaan json-muotoon ja kirjoitetaan tiedostoon.
    with open("/usr/share/hassio/homeassistant/custom_components/ruuvitag-sensor/tag3.json", "w") as fp:
        json.dump(found_data[1], fp)

# Vain ulkomittari mittari: 
mac = 'CA:36:56:59:F8:6B'

# Tämä pyörittää etsintää ad infinitum
RuuviTagSensor.get_datas(handle_data, mac)
