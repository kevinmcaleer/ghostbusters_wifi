class Listbox():
    highlight = {
        'red': 255,
        'green':0,
        'blue':0,}
    
    default = {
        'red': 255,
        'green':255,
        'blue':255,}
    
    selected = 0
    item_height = 20
    
    def __init__(self, display, items, x, y, width, height):
        self.data = items
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        print(f'len of data: {len(self.data)}')
    
    def __post_init__(self):
        self.draw()
    
    def draw(self):
        # Clear area
        white = self.display.create_pen(255,255,255)
        self.display.set_pen(white)
        self.display.set_clip(self.x, self.y,self.width, self.height)
        self.display.clear()
        self.display.remove_clip()
        # Draw border
        
        # Draw items
        
        # setup pens
        highlight = self.display.create_pen(self.highlight['red'],self.highlight['green'], self.highlight['blue'])
        default = self.display.create_pen(self.default['red'],self.default['green'], self.default['blue'])
        no_of_items = len(self.data)
        for line in range(0, no_of_items):
            if line == self.selected:
                self.display.set_pen(highlight)
                self.display.rectangle(self.x, self.y + (line * self.item_height), self.width, self.item_height)
                self.display.set_pen(default)
            else:
                self.display.set_pen(default)
                self.display.rectangle(self.x, self.y + (line * self.item_height), self.width, self.item_height)
                self.display.set_pen(highlight)
                
            self.display.text(self.data[line], self.x + 10, self.y + line * self.item_height)
        self.display.update()
        
    def select(self, item):
        self.selected = item

    def down(self):
        
        if self.selected == len(self.data)-1:
            self.draw()
            return
        if self.selected < len(self.data)-1:
            self.selected += 1
        self.draw()
        print(f'down button pressed, selected item = {self.selected}')
    def up(self):
        
        if self.selected == 0:
            self.draw()
            return
    
        if self.selected > 0:
            self.selected -= 1 
        self.draw()
        print(f'up button pressed, selected item = {self.selected}')

def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q