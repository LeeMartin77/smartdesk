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

def setup_shift_register_pins():
    ser_output = digitalio.DigitalInOut(board.GP6)
    ser_output.direction = digitalio.Direction.OUTPUT
    ser_output.value = False

    rclk_output = digitalio.DigitalInOut(board.GP7)
    rclk_output.direction = digitalio.Direction.OUTPUT
    rclk_output.value = False

    srclk_output = digitalio.DigitalInOut(board.GP8)
    srclk_output.direction = digitalio.Direction.OUTPUT
    srclk_output.value = False

    output_enable = digitalio.DigitalInOut(board.GP10)
    output_enable.direction = digitalio.Direction.OUTPUT
    output_enable.value = False

    shiftregister_clear = digitalio.DigitalInOut(board.GP11)
    shiftregister_clear.direction = digitalio.Direction.OUTPUT
    shiftregister_clear.value = True
    shiftregister_clear.value = False
    shiftregister_clear.value = True


    return [ser_output, rclk_output, srclk_output, output_enable, shiftregister_clear]

def increment_shift_register(shift_register_value, shift_register_pins):
    shift_register_value = shift_register_value + 1
    if shift_register_value > 7:
        shift_register_value = 0
    for i in range(7):
        # print(f'{shift_register_value}:{i}')
        shift_register_pins[2].value = False
        shift_register_pins[0].value = i == shift_register_value 
        shift_register_pins[2].value = True
        shift_register_pins[2].value = False
    shift_register_pins[1].value = True
    shift_register_pins[1].value = False
    return shift_register_value

(left_pin, right_pin) = setup_input()

display = setup_display()

declaration_to_display = 0
declarations = ['Friends', 'Daniel', 'Timothy']

shift_register_pins = setup_shift_register_pins()

loop_time = time.time()

shift_register_value = 0

# Main Loop
while True:
    start_declaration = declaration_to_display
    declaration_to_display = input_handler(declaration_to_display, left_pin, right_pin)
    if declaration_to_display != start_declaration:
        update_display(display, declaration_to_display, declarations)
    if time.time() > loop_time:
        loop_time = time.time()
        shift_register_value = increment_shift_register(shift_register_value, shift_register_pins)
    
    