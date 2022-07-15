import network
import binascii
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
import jpegdec
from time import sleep

display = PicoGraphics(DISPLAY_PICO_DISPLAY)
WIDTH, HEIGHT = display.get_bounds()

LOGO_FILENAME = 'splash.jpg'
BACKGROUND = 'background.jpg'
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
# scan returns:
# (ssid, bssid, channel, RSSI, security, hidden, strength)



def scan_wifi():

    security_type = {0:'Open', 1:'WEP', 2:'WPA-PSK', 3:'WPA2-PSK', 4:'WPA/WPA2-PSK'}

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wifi_list = wlan.scan()

    new_list = []
    print('scanning')
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

    return new_list
    
#     print(f'{ssid}, bssid {bssid}, ch {channel}, strength {strength}, security {sec_type}, hidden {hidden}')

def draw_list(new_list):
    print('drawing list')
    scale = 2
    current_line = 0
    line_height = 10 * scale
    display.set_font("bitmap8")
    pen = display.create_pen(black['red'], black['green'], black['blue'])
    display.set_pen(pen)
    for item in new_list:
        display.text(f'{item[0]}', 0, current_line, scale=scale)
        
        current_line += 1 * line_height

    display.update()
# Draw logo and pause 2 seconds
sleep(3)
draw_jpg(display, LOGO_FILENAME)
sleep(2)
draw_jpg(display, SCANNING)
new_list = scan_wifi()
draw_table(new_list)
draw_jpg(display, BACKGROUND)
draw_list(new_list)