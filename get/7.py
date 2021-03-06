import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

def dec2bin(num):
    return [int(e) for e in bin(num)[2:].zfill(8)]
def bin2dec(y):
    x = list(map(str, y))
    return int(''.join(x), base = 2 )
def dec2dac(num):
    GPIO.output(dac, dec2bin(num))
    return (dec2bin(num))
def dec2leds(num):
    GPIO.output(leds, dec2bin(num))
    return (dec2bin(num))
def adc():
    outp = [0]*8
    for i in range(8):
        outp[i] = 1
        GPIO.output(dac, outp)
        time.sleep(0.002)
        com_out = GPIO.input(comp)
        if not com_out:
            outp[i] = 0
    dv = bin2dec(outp)
    volt = dv*3.3/256
    print('Digital value: {} , analog value: {:.2f}'.format(dv, volt))
    return dv

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2 ** bits
max_volt = 3.3
comp = 4
troy = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troy, GPIO.OUT)

try:
    data_list = []
    start = time.time()
    val = 0
    GPIO.output(troy, GPIO.HIGH)
    print('Зарядка началась')
    time.sleep(0.5)
    while val < 240:
        val = adc()
        dec2leds(val)
        data_list.append(val)
    
    GPIO.output(troy, GPIO.LOW)
    print('Зарядка окончена')
    time.sleep(0.5)
    print('Разрядка началась')
    time.sleep(0.5)
    while val > 5:
        val = adc()
        dec2leds(val)
        data_list.append(val)
    print('Разрядка окончена')
    time.sleep(0.5)
    stop = time.time()
    dur = stop - start
    plt.plot(data_list)
    freq = len(data_list) / dur
    step = 3.3 / levels

    data_str = list(map(str, data_list))
    with open('data.txt', 'w') as data:
        data.write('\n'.join(data_str))
    
    with open('settings.txt', 'w') as s:
        s.write('Duration: {}\n'.format(str(dur)))
        s.write('Frequency: {}\n'.format(str(freq)))
        s.write('Step: {}\n'.format(str(step)))

    print('Duration: {}'.format(str(dur)))
    print('Time: {}'.format(str(1 / freq)))
    print('Frequency: {}'.format(str(freq)))
    print('Step: {}'.format(str(step)))
    plt.show()

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(leds)
    print('GPIO cleanup completed')