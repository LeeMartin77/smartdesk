import time
import board
import digitalio
import usb_hid
import busio

import adafruit_ssd1306

def setup_input():
    left_pin = digitalio.DigitalInOut(board.GP17)
    left_pin.direction = digitalio.Direction.INPUT
    left_pin.pull = digitalio.Pull.DOWN

    right_pin = digitalio.DigitalInOut(board.GP16)
    right_pin.direction = digitalio.Direction.INPUT
    right_pin.pull = digitalio.Pull.DOWN
    return (left_pin, right_pin)

def setup_display():
    # SSD1306
    # https://pupilsys.com/index.php?route=product/product&product_id=88
    spi = busio.SPI(board.GP2, board.GP3) # D0, D1

    res = digitalio.DigitalInOut(board.GP26) # RES

    dc = digitalio.DigitalInOut(board.GP22) # DC

    cs = digitalio.DigitalInOut(board.GP21) # CD

    display = adafruit_ssd1306.SSD1306_SPI(128, 64, spi, dc, res, cs)

    display.fill(0)
    display.text(f'Loading...', 20, 20, 1)
    display.show()
    return display

def input_handler(declaration_to_display, left_pin, right_pin):
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
    return declaration_to_display

def update_display(display, declaration_to_display, declarations):
    display.fill(0)
    display.text(f'Hello {declarations[declaration_to_display]}', 20, 20, 1)
    display.show()

(left_pin, right_pin) = setup_input()

display = setup_display()

declaration_to_display = 0
declarations = ['Friends', 'Daniel', 'Timothy']

# Main Loop
while True:
    start_declaration = declaration_to_display
    declaration_to_display = input_handler(declaration_to_display, left_pin, right_pin)
    if declaration_to_display != start_declaration:
        update_display(display, declaration_to_display, declarations)

    