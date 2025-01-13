import time
import network

ssid = 'xxxx'
password = 'xxxx'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(0.5)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    # print(wlan.ifconfig())
    return ip

ip = connect()

import machine
from mlx90614 import MLX90614  # Initialize I2C bus
from picozero import Speaker

import urequests as requests
import ujson as json

URL = 'https://172.20.10.8:5001/board'
TEMP_TRESHOLD = 25

timestamp = time.time()

# states
LOW_TEMP = 1
HIGH_TEMP_ON = 2
HIGH_TEMP_OFF = 3

def time_passed():
    print(f'Time passed: {(time.time() - timestamp)}')
    return (time.time() - timestamp)

def beep(speaker):
    global timestamp
    timestamp = time.time()
    # TODO: action speaker
    speaker.play('c4', 100, wait=False)

def stop_beep(speaker):
    speaker.off()


def get_temperature(sensor):
    object_temp = sensor.object_temp
    # ambient_temp = sensor.ambient_temp

    # print(f"Ambient Temperature: {ambient_temp:.2f}C")
    print(f"Object Temperature: {object_temp:.2f}C")
    
    return object_temp

def setup_temp_sensor():
    i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0), freq=100000)# Scan for I2C devices
    devices = i2c.scan()
    if devices:
        print("I2C devices found:", [hex(device) for device in devices])
    else:
        print("No I2C devices found")# Initialize the MLX90614 sensor

    return MLX90614(i2c)

sensor = setup_temp_sensor()
speaker = Speaker(5)
current_state = LOW_TEMP
previous_state = current_state
while True:
    temp = get_temperature(sensor)
    beeps = current_state == HIGH_TEMP_ON
    should_beep = beeps and (previous_state == HIGH_TEMP_OFF or previous_state == LOW_TEMP)

    post_data = json.dumps({ 'beeps': beeps, 'should_beep': should_beep, 'temp': temp })
    try:
        response = requests.post(url=URL, headers={'content-type': 'application/json'}, data=post_data)
    except:
        print('Server is down...')
        time.sleep(1)
        continue
    should_beep = response.json()['should_beep']

    previous_state = current_state
    if previous_state == LOW_TEMP:
        print('State: LOW_TEMP')
        if temp >= TEMP_TRESHOLD:
            # switch to HIGH_TEMP_ON
            current_state = HIGH_TEMP_ON
    elif current_state == HIGH_TEMP_ON:
        print('State: HIGH_TEMP_ON')
        if temp < TEMP_TRESHOLD:
            current_state = LOW_TEMP
        elif not should_beep:  # user turned the speaker off
            current_state = HIGH_TEMP_OFF
    elif current_state == HIGH_TEMP_OFF:
        print('State: HIGH_TEMP_OFF')
        if temp < TEMP_TRESHOLD:
            current_state = LOW_TEMP
        elif time_passed() >= 7:
            current_state = HIGH_TEMP_ON

    if current_state == HIGH_TEMP_ON:
        beep(speaker)
    else:
        stop_beep(speaker)

    time.sleep(1)
