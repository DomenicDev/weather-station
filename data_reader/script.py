import os
import serial
from questdb.ingress import Sender, TimestampNanos
import re
import time

# Retrieve the QuestDB configuration from environment variable
conf = os.getenv('QUESTDB_CONF', 'http::addr=localhost:9000;')

def extract_data(line):
    # Regex patterns to extract temperature and humidity from the input line
    temp_match = re.search(r'Temperature: (\d+\.\d+)°C', line)
    hum_match = re.search(r'Humidity: (\d+\.\d+)%', line)
    
    temperature = float(temp_match.group(1)) if temp_match else None
    humidity = float(hum_match.group(1)) if hum_match else None
    
    return temperature, humidity

def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    temperature, humidity = None, None

    with Sender.from_conf(conf) as sender:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(f"Received line: {line}")

                temp, hum = extract_data(line)

                if temp is not None:
                    temperature = temp
                    print(f"Extracted temperature: {temperature}°C")
                if hum is not None:
                    humidity = hum
                    print(f"Extracted humidity: {humidity}%")

                if temperature is not None and humidity is not None:
                    sender.row(
                        'sensors',
                        symbols={'id': 'arduino'},
                        columns={'temperature': temperature, 'humidity': humidity},
                        at=TimestampNanos.now()
                    )
                    sender.flush()
                    # Reset temperature and humidity after sending to QuestDB
                    temperature, humidity = None, None

	    # Sleep for a short period to reduce CPU usage
            time.sleep(0.2)

if __name__ == '__main__':
    main()
