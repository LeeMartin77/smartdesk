import time
import board
import digitalio
import usb_hid
import busio

import adafruit_ssd1306

def setup_display():
    # SSD1306
    # https://pupilsys.com/index.php?route=product/product&product_id=88
    spi = busio.SPI(board.GP2, board.GP3) # D0, D1

    res = digitalio.DigitalInOut(board.GP8) # RES

    dc = digitalio.DigitalInOut(board.GP9) # DC

    cs = digitalio.DigitalInOut(board.GP10) # CD

    return adafruit_ssd1306.SSD1306_SPI(128, 64, spi, dc, res, cs)


left_pin = digitalio.DigitalInOut(board.GP17)
left_pin.direction = digitalio.Direction.INPUT
left_pin.pull = digitalio.Pull.DOWN

right_pin = digitalio.DigitalInOut(board.GP16)
right_pin.direction = digitalio.Direction.INPUT
right_pin.pull = digitalio.Pull.DOWN

display = setup_display()
declaration_to_display = 0
declarations = ['Friends', 'Daniel', 'Timothy']

display.fill(0)
display.text(f'Hello {declarations[declaration_to_display]}', 20, 20, 1)
display.show()

while True:
    start_declaration = declaration_to_display
    if left_pin.value:
        declaration_to_display = declaration_to_display - 1
        while left_pin.value:
            pass
    if right_pin.value:
        declaration_to_display = declaration_to_display + 1
        while right_pin.value:
            pass
    
    if declaration_to_display > len(declarations) - 1:
        declaration_to_display = 0
    
    if declaration_to_display < 0:
        declaration_to_display = len(declarations) - 1

    if declaration_to_display != start_declaration:
        display.fill(0)
        display.text(f'Hello {declarations[declaration_to_display]}', 20, 20, 1)
        display.show()

    