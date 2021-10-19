import time
import board
import digitalio
import usb_hid
import busio

import adafruit_ssd1306

# SSD1306

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

# https://pupilsys.com/index.php?route=product/product&product_id=88
spi = busio.SPI(board.GP2, board.GP3) # D0, D1

res = digitalio.DigitalInOut(board.GP8) # RES

dc = digitalio.DigitalInOut(board.GP9) # DC

cs = digitalio.DigitalInOut(board.GP10) # CD

display = adafruit_ssd1306.SSD1306_SPI(128, 64, spi, dc, res, cs)
count = 0
declarations = ['Friends', 'Daniel', 'Timothy']

while True:
    led.value = not led.value
    display.fill(0)
    display.text(f'Hello {declarations[count]}', 20, 20, 1)
    display.show()
    count = count + 1
    if count > len(declarations) - 1:
        count = 0
    time.sleep(2)
