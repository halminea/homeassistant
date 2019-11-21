from ruuvitag_sensor.ruuvi import RuuviTagSensor

def handle_data(found_data):
    # Kirjoitetaan tiedostoon json-muodossa data
    file = open("/usr/share/hassio/homeassistant/custom_components/ruuvitag-sensor/tag1.json", "w")
    file.write(found_data[1]) # Oikeat tiedot ovat toisena taulukossa, ensimmäisenä on mac-osoite
    file.close()
   

# Vain saunan mittari: 
mac = 'D7:FE:5A:B0:AB:59'

# Tämä pyörittää etsintää ad infinitum
RuuviTagSensor.get_datas(handle_data, mac)