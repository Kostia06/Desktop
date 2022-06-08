import math as m
import pygame as pg 
import clipboard
import random as r
import time
font = 'fff-forward/FFFFORWA.TTF'
run = True
class Label():
    def __init__(self,screen, text, pos, color = 'Black',shade=[None,None], rotate = 0, size = 20, bg = 'White', outline='Black', side = 'center'):
        self.font = pg.font.Font(font,size)
        self.font_size = size
        self.display = self.font.render(str(text), True, color)
        self.rect_new = self.display.get_rect()
        self.side = 'self.rect_new.' + side + ' = (pos)'
        exec(self.side)
        self.rect_new.w += self.font_size
        self.rect_new.h += self.font_size
        self.display = pg.transform.rotate(self.display, rotate)
        if bg != None:
            if rotate == 90 or rotate == 270:
                if shade[1] != None:
                    pg.draw.rect(screen, (shade[1]), (self.rect_new.x - self.font_size/2+5, self.rect_new.y - self.font_size/2+5, self.rect_new.h, self.rect_new.w), 0, 10)
                pg.draw.rect(screen, (bg), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.h, self.rect_new.w), 0, 10)
                if outline != None:
                    pg.draw.rect(screen, (outline), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.h, self.rect_new.w), 3, 10)
            else:
                if shade[1] != None:
                    pg.draw.rect(screen, (shade[1]), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.w+6, self.rect_new.h+6), 0, 10)
                pg.draw.rect(screen, (bg), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.w, self.rect_new.h), 0, 10)
                if outline != None:
                    pg.draw.rect(screen, (outline), (self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.w, self.rect_new.h), 3, 10)
        if shade[0] != None:
            self.shade = self.font.render(str(text), True, shade[0])
            self.shade = pg.transform.rotate(self.shade, rotate)
            screen.blit(self.shade, (self.rect_new.x + 4, self.rect_new.y + 4))
        screen.blit(self.display, (self.rect_new))
        self.rect = pg.Rect(self.rect_new.x - self.font_size/2, self.rect_new.y - self.font_size/2, self.rect_new.w, self.rect_new.h)
class Switch():
    def __init__(self,text, pos, turn, color = 'Black', shade = [None, None], size = 20, bg = 'White', outline= 'Black', sides='center'):
        self.font_size = size 
        self.turn = turn
        self.size = size/2
        self.text = text
        self.pos = pos
        self.circle = pg.Vector2()
        self.clicked = False
        self.side = sides
        self.color = color
        self.bg = bg
        self.rect = pg.Rect(pos[0]-30, pos[1]-10, 60, 20)
        self.poses = {True: self.rect.x+self.rect.w, False:self.rect.x}
        self.circle_pos = self.poses[turn]
        self.bar_rect = None
        self.outline = outline
        self.shades = shade
    def draw(self, screen):
        text = Label(screen, self.text, self.pos, size=self.font_size, side=self.side, shade=self.shades, outline=self.outline, bg=self.bg, color = self.color)
        pg.draw.rect(screen, ('#FF6B46'), (self.rect.x, self.rect.y + text.rect.h, self.rect.w, self.rect.h), 0, 15)
        width = self.circle_pos -self.rect.x
        pg.draw.rect(screen, ('#0DEAA1'), (self.rect.x, self.rect.y + text.rect.h, width, self.rect.h), 0, 15)
        pg.draw.rect(screen, ('Black'), (self.rect.x, self.rect.y + text.rect.h, self.rect.w, self.rect.h), 3, 15)
        self.bar_rect = pg.Rect(self.rect.x, self.rect.y + text.rect.h, self.rect.w, self.rect.h)
        pg.draw.circle(screen, ('white'),[self.circle_pos, self.rect.y+text.rect.h+10], 13 )
        pg.draw.circle(screen, ('black'),[self.circle_pos,self.rect.y+text.rect.h+10], 13 , 3)
        self.animation()
    def animation(self):
        if pg.mouse.get_pressed()[0] ==1 and self.bar_rect.collidepoint(pg.mouse.get_pos()) and not self.clicked:
            self.turn = not self.turn
            self.clicked = True
        if pg.mouse.get_pressed()[0] ==0:
            self.clicked = False
        if self.circle_pos < self.poses[self.turn]:
            self.circle_pos += 2.5
        elif self.circle_pos > self.poses[self.turn]:
            self.circle_pos -= 2.5
    def choice(self):
        if self.turn:
            return True
        else:
            return False
class Button():
    def __init__(self, text, pos,  size = 20, shade = [None,'Gray'], color='Black', bg='White', outline = 'Black', side = 'center'):
        self.clicked = False
        self.bg = bg
        self.outline = outline
        self.shade = shade
        self.side = side
        self.size = size
        self.text =text
        self.color = color
        self.pos = pos
        self.side =side
        self.offset = 0
        self.label = None
    def draw(self, screen, offset= 0):
        if self.label:
            pg.draw.rect(screen, self.shade[1], (self.label.rect.x, self.label.rect.y, self.label.rect.w+5-self.offset, self.label.rect.h+5-self.offset), 0, 10)
        self.label = Label(screen, self.text, [self.pos[0]+self.offset, self.pos[1] + self.offset+offset],color =self.color, size = self.size,shade = [self.shade[0], None], bg= self.bg, outline=self.outline,side =self.side )
        action = False
        if pg.mouse.get_pressed()[0] ==1 and self.label.rect.collidepoint(pg.mouse.get_pos()) and not self.clicked:
            self.clicked = True
            action = True
            return action
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        self.animation(self.label.rect)
    def animation(self, rect):
        if rect.collidepoint(pg.mouse.get_pos()):
            self.offset=2
        else :
            self.offset =0
class Bar():
    def __init__(self,pos, size, color=['green', 'yellow', 'red'], shade='Grey', outline='Black', time=5000):
        self.color = color
        self.color_choice = 1
        self.size = size
        self.pos = pos
        self.outline = outline
        self.shade = shade
        self.courent_time = 0
        self.press_time = 0
        self.time = time
        self.ratio = time/ self.size[0]
        self.show = False
        self.clicked = False
        self.work = True
    def draw(self,screen, item):
        self.rect = pg.Rect(item.rect.centerx-self.pos[0] -self.size[0]/2, item.rect.centery -self.pos[1] - self.size[1]/2, self.size[0],self.size[1])

        if self.show and not self.courent_time - self.press_time>self.time:
            if self.shade != None:
                pg.draw.rect(screen, self.shade, (self.rect.x, self.rect.y, self.size[0] +5, self.rect.h + 5), 0, 5)
            try:
                pg.draw.rect(screen, (self.color[self.color_choice-1]), (self.rect.x, self.rect.y, (self.courent_time - self.press_time)/self.ratio, self.rect.h), 0, 5)
            except:
                pass
            if self.outline != None:
                pg.draw.rect(screen, (self.outline), self.rect, 3, 5)

        if not item.clicked or not self.work:
            self.press_time = pg.time.get_ticks()
            self.show = False
            self.clicked = False
            self.color_choice = 1
        else:
            self.show = True
        self.courent_time = pg.time.get_ticks()
        if self.courent_time - self.press_time>self.time and not self.clicked:
            self.color_choice = 1
            self.press_time = 0
            self.courent_time = 0
            self.show = False
            self.clicked = True
        if self.courent_time - self.press_time > self.time/len(self.color) * self.color_choice:
            self.color_choice += 1
    def choice(self):
        return self.clicked
class Scale():
    def __init__(self, text, pos, scale, set, size = 20, shade = 'Gray', color = 'Black', bg = True,bg_color = 'White', shades = True, outline = 'Black'):
        self.pos = pos
        self.text = text
        self.scale = scale
        self.font = pg.font.Font(font,size)
        self.scale = scale
        self.list = (bg, bg_color, color, shade, outline, size, shades)
        self.scale_pos = pg.Vector2()
        self.rect_new = pg.Rect(pos[0], pos[1],size * 5, size/2)
        self.scale_pos.x = pos[0] + set * size/100 * 5
        self.font_size = size
        self.scale_pos.y = self.rect_new.centery + self.rect_new.h
        self.rect_new.h += self.font_size
        self.num = 50
        self.font_size = size
        self.changed = False
        self.size =size/2
    def draw(self, screen):
        pos = pg.mouse.get_pos()
        if self.rect_new.collidepoint(pos):
            self.size = self.font_size/2 + 1
        elif pg.mouse.get_pressed()[0] ==0 and not self.rect_new.collidepoint(pos):
            self.size = self.font_size/2
        if self.list[6]:
            pg.draw.rect(screen,(self.list[3]), (self.rect_new.x + 4, self.rect_new.y + 4, self.rect_new.w, self.rect_new.h), 0, 15)
        pg.draw.rect(screen,('White'), (self.rect_new), 0, 15)
        if self.list[4] != None:
            pg.draw.rect(screen,(self.list[4]), (self.rect_new), 2, 15)
        pg.draw.circle(screen, ('White'), (self.scale_pos),self.size)
        pg.draw.circle(screen, ('Black'), (self.scale_pos),self.size, 2)
        if pg.mouse.get_pressed()[0] ==1:
            if self.rect_new.collidepoint(pos):
                self.changed = True
                self.scale_pos.x = pg.mouse.get_pos()[0]
                self.num = (self.pos[0] - self.scale_pos.x)/((self.font_size * 5)/100)
                if abs(self.num) < 0:
                    self.num = 0.0
                self.size = self.font_size/2 + 2
                num_display = self.font.render(str(abs(int(self.num))), True, 'Black')
                num_rect = num_display.get_rect()
                screen.blit(num_display, (self.scale_pos +(-num_rect.w/2,self.font_size/2)))
        Label(self.text, (self.rect_new.centerx, self.rect_new.centery - self.font_size - self.rect_new.w/5), color = self.list[2],bg = self.list[0], bg_color =self.list[1], shade = self.list[3], outline=self.list[4], size = self.list[5], shades=self.list[6])
    def choice(self):
        return abs(self.num)
class Input():
    def __init__(self, text, pos, num, size = 20, color='Black',bg='White', shade=[None, None], type=str, sides=['center', 'center'], outline = 'Black'):
        self.num = num + 1
        self.text = text[0]
        self.output = text[1]
        self.pos = pos
        self.clicked = False
        self.type = type       
        self.offset = 0
        self.size = size
        self.shade = shade
        self.bg = bg
        self.color = color
        self.sides = sides
        self.text_label = None
        self.output_label = None
        self.outline = outline
    def draw(self,screen, event, single = False):
        pos = pg.mouse.get_pos()
        if self.clicked:
            for event in event:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.output = self.output[:-1]
                    elif event.key == pg.K_RETURN:
                        self.clicked = False
                    elif len(self.output) + 1 < self.num and not single:
                        if self.type == str:
                            self.output += event.unicode
                        elif event.key != 1073742051:
                            try:
                                send = event.unicode
                                send = int(send)
                                self.output += str(send)
                            except:
                                pass
                        if event.key == pg.K_v and pg.key.get_mods() & pg.KMOD_CTRL:
                            self.output = self.output[:-1]
                            text = clipboard.paste()
                            self.output += text
                    elif len(self.output) + 1 < self.num and single:
                        self.output = event.key
                    else:
                        self.clicked = False
        if self.text_label and self.output_label:
            if self.text_label.rect.w > self.output_label.rect.w:
                pg.draw.rect(screen, self.bg, [self.text_label.rect.x, self.text_label.rect.y,self.text_label.rect.w, self.text_label.rect.h + self.output_label.rect.h/2 ], 0, 10)
                pg.draw.rect(screen, self.outline, [self.text_label.rect.x, self.text_label.rect.y,self.text_label.rect.w, self.text_label.rect.h + self.output_label.rect.h/2 ], 3, 10)
                rect = pg.Rect(self.text_label.rect.x, self.text_label.rect.y,self.text_label.rect.w, self.text_label.rect.h + self.output_label.rect.h/2 )
            else:
                pg.draw.rect(screen, self.bg, [self.output_label.rect.x, self.text_label.rect.y,self.output_label.rect.w, self.text_label.rect.h + self.output_label.rect.h/2 ], 0, 10)
                pg.draw.rect(screen, self.outline, [self.output_label.rect.x, self.text_label.rect.y,self.output_label.rect.w, self.text_label.rect.h + self.output_label.rect.h/2 ], 3, 10)
                rect = pg.Rect(self.output_label.rect.x, self.text_label.rect.y,self.output_label.rect.w, self.text_label.rect.h + self.output_label.rect.h/2 )
            if pg.mouse.get_pressed()[0] ==1 and rect.collidepoint(pg.mouse.get_pos()) and not self.clicked:
                self.clicked = True
            if pg.mouse.get_pressed()[0] ==1 and not rect.collidepoint(pg.mouse.get_pos()):
                self.clicked = False
        if not self.clicked:
            self.text_label = Label(screen, self.text, [self.pos[0], self.pos[1]-self.size/2], color = self.color, shade = self.shade, outline=None, bg=None, size =self.size, side = self.sides[0])
            self.output_label = Label(screen, self.output, [self.pos[0], self.pos[1]+self.size/2+8],color = self.color, shade = self.shade, outline=None, bg=None, size =self.size, side = self.sides[0] )
            pg.draw.rect(screen, self.outline, [self.text_label.rect.x+5, self.output_label.rect.y+self.output_label.rect.h/1.4, self.text_label.rect.w-10, 1])
        elif self.clicked:
            self.output_label = Label(screen, self.output, [self.pos[0], self.pos[1]],color = self.color, shade = self.shade, outline=None, bg=None, size =self.size, side = self.sides[0] )
            pg.draw.rect(screen, self.outline, [self.text_label.rect.x+5, self.output_label.rect.y+self.output_label.rect.h/1.4, self.text_label.rect.w-10, 1])
        
            
    def choice(self):
        if not self.clicked:
            return self.output
class Water(pg.sprite.Sprite):
    def __init__(self,pos,size,amplitude=10,period=5):
        self.amplitude = amplitude
        self.period = period
        self.list = []
        self.x = [pos[0],size[0]]
        self.clicked = False
        self.y = [pos[1]+size[1], size[1]]
        self.points = []
        self.water_heights = []
        self.dy = []
        self.spacing = 10
        self.sea_level = size[1]
        self.friction = 0.01
        self.surface_tension = 0.5
        self.oscillator = 0
        for i in range(0,self.x[1]+self.spacing,self.spacing):
            self.water_heights.append(self.y[0]-self.sea_level )
            self.dy.append(0)
        for i in range(len(self.water_heights)):
            self.points.append(((self.spacing*i) + self.x[0],self.water_heights[i]))
        self.points.append((self.x[0]+self.x[1],self.y[0]))
        self.points.append((self.x[0],self.y[0]))
    def shiftWaterHeight(self, mouse_pos, water_heights):
        x,y = mouse_pos[0], self.y[0] - self.y[1] *1.25
        x = x - self.x[0]
        index = 0
        for i in range(len(water_heights)):
            if self.spacing*i <= x and x <= self.spacing*(i+1):
                index = i
                break
        water_heights[index] = y
    def draw(self, screen):
        screens  = pg.Surface((screen.get_size()), pg.SRCALPHA)
        mouse = pg.mouse.get_pressed(), pg.mouse.get_pos()
        if mouse[0][0] ==1 and not self.clicked:
            self.shiftWaterHeight(mouse[1], self.water_heights)
            self.clicked = True
        elif mouse[0][0] == 0:
            self.clicked = False
        for i in range(len(self.dy)):
            neighbor_heights = 0
            neighbor_count = 0
            if i>0:
                neighbor_heights += self.water_heights[i-1]
                neighbor_count += 1
            if i<len(self.dy)-1:
                neighbor_heights += self.water_heights[i+1]
                neighbor_count += 1
            self.dy[i] += self.surface_tension*(neighbor_heights - neighbor_count*self.water_heights[i])
            self.dy[i] = (1-self.friction)*self.dy[i]
        for i in range(len(self.water_heights)):
            self.water_heights[i] += self.dy[i]
        self.water_heights[-1] = self.y[0]-self.sea_level-self.amplitude*m.sin(self.oscillator/self.period)
        self.oscillator += 1
        for i in range(len(self.water_heights)):
            self.points[i] = ((self.spacing*i) +self.x[0],self.water_heights[i])
        pg.draw.polygon(screens, ('#0DEAA1'), self.points)
        screen.blit(screens, (0,0))
class Gradient():
    def __init__(self, screen, colors, rect ):
        colour_rect = pg.Surface( ( len(colors), len(colors) ) )     
        for i in range(len(colors)):                            
            pg.draw.line( colour_rect, colors[i],  ( i,0 ), ( i,i+1 ) )                    
        colour_rect = pg.transform.smoothscale( colour_rect, ( rect.width, rect.height ) )  
        screen.blit( colour_rect, rect )      
class Dots():
    def __init__(self, pos):
        self.pos = pos
        self.size = r.randint(5,10)
        self.x = r.choice((-1,1)) * 2
        self.y = r.choice((-1,1)) * 2
        self.prev_time = time.perf_counter()
        self.top = r.choice([-1,1])
    def draw(self, screen):
        self.transparent = pg.Surface((screen.get_size()), pg.SRCALPHA)
        WIDTH, HEIGHT = screen.get_size()
        now = time.perf_counter()
        dt = now - self.prev_time
        self.prev_time = now
        pg.draw.circle(screen, ('#0DEAA1'), (self.pos),self.size)
        pg.draw.circle(self.transparent, (13,234,161, 50), (self.pos), self.size+5)
        if r.randint(1,1000) == 1:
            self.x = r.choice((-1,1))
            self.y = r.choice((-1,1))
        self.pos[0] += self.x * dt * 30
        self.pos[1] += self.y * dt * 30 
        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.x *= -1
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.y *= -1
        screen.blit(self.transparent, (0,0))