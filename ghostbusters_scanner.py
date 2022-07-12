import network
import binascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wifi_list = wlan.scan()

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

# scan returns:
# (ssid, bssid, channel, RSSI, security, hidden, strength)

security_type = {0:'Open', 1:'WEP', 2:'WPA-PSK', 3:'WPA2-PSK', 4:'WPA/WPA2-PSK'}

new_list = []

for hotspot in wifi_list:
    ssid = str(hotspot[0].decode('utf-8'))
    bssid = str(binascii.hexlify(hotspot[1]).decode('utf-8'))
    channel = str(hotspot[2])
    strength = str(hotspot[3])
    security = str(hotspot[4])
    hidden = str(hotspot[5])
    sec_type = str(security_type.get(int(hidden)-1))
    print(f'Security: {security}, Security Type: {sec_type}')
    
    item = [ssid, bssid, channel, security  ,hidden,sec_type, strength]
    new_list.append(item)
    
#     print(f'{ssid}, bssid {bssid}, ch {channel}, strength {strength}, security {sec_type}, hidden {hidden}')

draw_table(new_list)