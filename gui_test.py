from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import jpegdec
from time import sleep
from pimoroni import RGBLED, Button
import gc
from gui import Listbox

gc.collect()

display = PicoGraphics(DISPLAY_PICO_DISPLAY_2, rotate=270)
WIDTH, HEIGHT = display.get_bounds()

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

data = ['Apple', 'Pear', 'Giraffe', 'Polo']
inset = 20
box = Listbox(display, data, 10, inset, WIDTH, HEIGHT)

while True or KeyboardInterrupt:
    if button_x.read():
        box.down()
    if button_y.read():
        box.up()
    box.draw()
