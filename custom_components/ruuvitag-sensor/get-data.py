from ruuvitag_sensor.ruuvi import RuuviTagSensor
from ruuvitag_sensor.data_formats import DataFormats
from ruuvitag_sensor.decoder import get_decoder

def handle_data(found_data):
    # Tuple, jossa dataformaatti ja itse data
    #(data_format, encoded) = DataFormats.convert_data(found_data)
    #sensor_data = get_decoder(data_format).decode_data(encoded)

    # Kirjoitetaan tiedostoon
    #file = open("/usr/share/hassio/homeassistant/custom_components/ruuvitag-sensor/tag1.json", "w")
    #file.write(sensor_data)
    #file.close()
    print(found_data[1])

# Vain saunan mittari: 
mac = 'D7:FE:5A:B0:AB:59'
RuuviTagSensor.get_datas(handle_data, mac)