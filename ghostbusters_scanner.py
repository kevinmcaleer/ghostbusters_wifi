import network
import binascii
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import jpegdec
from time import sleep
from pimoroni import RGBLED, Button
import gc
from gui import Listbox, hsv_to_rgb
from arms import Arms
import math
import machine

gc.collect()

display = PicoGraphics(DISPLAY_PICO_DISPLAY_2, rotate=270)
WIDTH, HEIGHT = display.get_bounds()

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

s = Arms(0)
s.enable()

led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

print(f'Width {WIDTH}, Height {HEIGHT}')

LOGO_FILENAME = 'splash.jpg'
BACKGROUND = 'list.jpg'
SCANNING = 'scanning.jpg'

white = {'red': 255, 'green': 255, 'blue': 255}
black = {'red': 0, 'green': 0, 'blue': 0}

def draw_jpg(display, filename):
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    j.open_file(filename)

    WIDTH, HEIGHT = display.get_bounds()
    display.set_clip(0, 0, WIDTH, HEIGHT)

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    display.remove_clip()
    display.update()

def get_column_width(columns):
    """ returns the max width of each column """
    
    # create a list of widths
    widths = [[len(row) for row in column] for column in columns ]
        
    # Transpose the rows and columns of widths:
    new_list = [list(x) for x in zip(*widths)]
 
    return [max(row) for row in new_list]
    
def draw_table(columns):
    
    #            ssid,   bssid,   channel, security  ,hidden,sec_type, strength
    headings = ['SSID', 'BSSID', 'Channel', 'Security','Hidden','Sec-type', 'Strength']
    
    # Add headings to columns
    data = []
    data.append(headings)
    data.extend(columns)
    columns = data
    
    column_widths = get_column_width(columns)
    print(column_widths)
    no_of_hotspots = len(columns)-1
    print(f"hotspots found: {no_of_hotspots}")
    
    # Print the headings
    for index, col in enumerate(columns[0]):
        spacing = column_widths[index]
        line = '{:{}s}'.format(col, spacing+1)
        print(line, end="")
    print("")
    
    # Print the headings underline
    for column in column_widths:
        print('-' * column, end=" ")
    print("")
    
    for row in columns[1:]:        
        for index, col in enumerate(row):

            spacing = column_widths[index]
            line = '{:{}s}'.format(col, spacing+1)
            print(line, end="")
        print()
    print("Scan complete.")


def scan_wifi()->list:
    """ scan for wifi hotspots, returns a list of hotspots and their details """
    security_type = {0:'Open', 1:'WEP', 2:'WPA-PSK', 3:'WPA2-PSK', 4:'WPA/WPA2-PSK'}
    print('Setting up wifi')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('Wifi online')
    print('scanning')

    # scan returns: ssid, bssid, channel, RSSI, security, hidden, strength
    wifi_list = wlan.scan()
    print('scan complete')
    new_list = []
    print('processing list...')
    for hotspot in wifi_list:
        ssid = str(hotspot[0].decode('utf-8'))
        bssid = str(binascii.hexlify(hotspot[1]).decode('utf-8'))
        channel = str(hotspot[2])
        strength = str(hotspot[3])
        security = str(hotspot[4])
        hidden = str(hotspot[5])
        sec_type = str(security_type.get(int(hidden)-1))
        print(f'found: {ssid}')
        
        item = [ssid, bssid, channel, security  ,hidden,sec_type, strength]
        new_list.append(item)

    print('processing complete')
    return new_list
    
def short_list(long_list):
    """ returns a list of just SSIDs """
    short_list = [item[0] for item in new_list]
    return short_list

def draw_list(new_list):
    """ draw the list of hotspots on the Screen """
    print('drawing list')
    scale = 2
    current_line = 0
    line_height = 10 * scale
    display.set_font("bitmap8")
    pen = display.create_pen(black['red'], black['green'], black['blue'])
    display.set_pen(pen)
    short_list = short_list(new_list)
    for item in new_list:
        display.text(f'{item[0]}', 10, current_line, scale=scale)
        
        current_line += 1 * line_height
    display.update()
    return short_list
        
def sparkle_led():
    """ makes the LED sparkle """
    for hue in range(0,100,1):
        r,g,b = hsv_to_rgb(hue/100, 1.0, 1.0)
        led.set_rgb(r, g, b)
        sleep(0.01)

def rgb_green():
    """ sets the LED to green """
    led.set_rgb(0, 255, 0)

def flash_yellow(times):
    """ flashes the LED yellow, for the number of items specified """
    for _ in range(1, times):
        led.set_rgb(255, 255, 0)
        sleep(0.5)
        led.set_rgb(0,0,0)
        sleep(0.5)
        
def map_range(value, low1, high1, low2, high2):
    """ maps a value from one range to another """
    return low2 + (high2 - low2) * (value - low1) / (high1 - low1)

def db_to_percent(selected_item, full_list)->float:
    """ Returns the percentage, based on the signal strength """
    item = full_list[selected_item]
    signal = int(item[6])
    return map_range(signal, 0, 100, 0, -100) / 100
    
def clip(value, min_clip, max_clip)->float:
    """ Checks if the value with within the min or max and
    ensures the value stays within the min max range """
    if value < min_clip:
        return min_clip
    if value > max_clip:
        return max_clip
    return value
    

def start_up():
    # Draw logo and pause 2 seconds
    s.close_arms()
    draw_jpg(display, LOGO_FILENAME)
    value = 0.9

    s.swoop_arms(3, 0.4, 0.9)
    s.swoop_arms(3, 0.9, 0.4)
        
    flash_yellow(3)
    draw_jpg(display, SCANNING)
    new_list = scan_wifi()

    draw_table(new_list)
    draw_jpg(display, BACKGROUND)
    # ssid_list = draw_list(new_list)
    return new_list

# Draw the list of hotspots on the screen via the GUI Listbox
new_list = start_up()
ssid_list = short_list(new_list)
inset = 60
listbox = Listbox(display, ssid_list,0, inset, WIDTH, HEIGHT-inset*4)
listbox.draw()
print(ssid_list)

while True or KeyboardInterrupt:
    # Check if the user has pressed any buttons
    if button_b.read():
        machine.reset()
    
    if button_a.read():
        draw_jpg(display, LOGO_FILENAME)
        s.to_percent(0.4)
        sleep(10)
        draw_jpg(display, BACKGROUND)
        
    if button_y.read():
        listbox.down()
        
    if button_x.read():
        listbox.up()
        
    signal = clip(db_to_percent(listbox.selected, new_list), 0.4, 0.9)
    s.to_percent(signal)
    listbox.draw()

print('disarming arms')
s.close_arms()
s.disable()

    
