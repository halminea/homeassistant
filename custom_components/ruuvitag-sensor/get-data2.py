from ruuvitag_sensor.ruuvi import RuuviTagSensor
import json

def handle_data(found_data):
    # Muutetaan json-muotoon ja kirjoitetaan tiedostoon.
    with open("/usr/share/hassio/homeassistant/custom_components/ruuvitag-sensor/tag2.json", "w") as fp:
        json.dump(found_data[1], fp)

# Vain ulkomittari mittari: 
mac = 'CE:9D:F3:C1:ED:F5'

# Tämä pyörittää etsintää ad infinitum
RuuviTagSensor.get_datas(handle_data, mac)