import threading as th
from gui import *
import os,json, pygame as pg
import random as r
from desktop import Desktop, json_dir
from clip import Clip_Board
from mouse import Mouse
import sys 
import pathlib


with open(json_dir, 'r') as f:
    data = json.load(f)

WIDTH, HEIGHT = 700, 600
wave = [Water([0,40], [WIDTH, -80]), Water([0, HEIGHT-40], [WIDTH, 80])]
desktop = Button('Desktop', [WIDTH//2, 240], color='#17667C', size=30, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
clip = Button('ClipBoard', [WIDTH//2, 320], color='#17667C', size=30, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
credits = Button('Credits', [WIDTH//2,400], color='#17667C', size=30, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
back = Button('Back', [WIDTH//2,520], color='#17667C', size=30, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
desktop_dir = Input(['Desktop Folders Dir', str(pathlib.Path.home() / 'Desktop')], [150,180],50, color='#17667C', size=15, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
folder = Input(['Folder Name', ''], [150,240],50, color='#17667C', size=15, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
file = Input(['File Types', ''], [150,300],50, color='#17667C', size=15, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
downloads = Switch('Check in Downloads', [150, 350],data['downloads'], color='#17667C', size=15, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
add = Button('Add', [150,420], color='#17667C', size=15, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
desktop_work = Switch('Work', [150, 460],data['work'], color='#17667C', size=15, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858')
class Main():
    def __init__(self):
        self.page = 1
        self.dots = [Dots([r.randrange(0, WIDTH), r.randrange(0, HEIGHT)]) for i in range(20)]
        self.work = False
        if len(data['dir']) == 0:
            self.desktop_dir = pathlib.Path.home() / 'Desktop'
        else:
            self.desktop_dir = data['dir']
            self.work = True
        self.build()
        self.run = True
        self.desktop = Desktop()
        self.clipboard =  Clip_Board()
        self.copys = {'text':[], 'buttons':[]}
        self.mouse = Mouse()
        self.offset = 0
        self.desktop_folders_files = data['types']
        self.desktop_text = []
        self.space = 0
    def build(self):
        self.run = True
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        pg.display.set_caption("BEST DESKTOP")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        if self.work:
            pg.display.iconify()
    def update(self):

        while 1:
            if self.run:
                self.clock.tick(60)
                self.event = pg.event.get()
                for i in self.event:
                    if i.type == pg.QUIT:
                        with open(json_dir, "r+") as jsonFile:
                            data = json.load(jsonFile)
                            data['work'] = desktop_work.choice()
                            data['downloads'] = downloads.choice()
                            jsonFile.seek(0)  # rewind
                            json.dump(data, jsonFile)
                            jsonFile.truncate()
                        pg.quit()
                        sys.exit(0)
                self.draw(self.screen)
                self.clipboard.update()
                if self.clipboard.new:
                    self.copys['text'].clear()
                    self.copys['buttons'].clear()
                if self.page != 4 and desktop_work.choice():
                    self.desktop.update()
                for i in range(len(self.clipboard.clip_list)):
                    text = self.clipboard.clip_list[i]
                    pos = [WIDTH//2, 200+(i*30)]
                    if not  text in self.copys['text']:
                        self.copys['text'].append(text)
                        self.copys['buttons'].append(Button(text,pos,color='#17667C', size=10, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858'))
            else:
                pg.display.iconify()



    
    def draw(self, screen):
        self.pages= {1: self.page_1, 2:self.page_2, 3:self.page_3, 4:self.page_4}
        screen.fill(('#0086BC'))
        for i in wave:
            i.draw(screen)
        for i in self.dots:
            if i.top == -1:
                i.draw(screen)
        self.pages[self.page](screen)
        for i in self.dots:
            if i.top == 1:
                i.draw(screen)
        pg.display.update()
    
    def page_4(self, screen):
        Label(screen, 'Desktop',[WIDTH//2,120 ], color='#17667C', size=30, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858' )
        desktop_dir.draw(screen, self.event)
        folder.draw(screen, self.event)
        file.draw(screen, self.event)
        downloads.draw(screen)
        if not os.path.exists(f'{desktop_dir.output}/{folder.output}') and len(folder.output) > 0 and not folder.clicked:
            folder.bg = '#FF6B46'
        else:
            folder.bg = '#0DEAA1'
        if len(file.output) > 0 and not file.clicked:
            if not [i for i in file.output.split(',') if i[0] == '.']:
                file.bg = '#FF6B46'
            else:
                file.bg =  '#0DEAA1'
        for key, value in self.desktop_folders_files.items():
            text = f'{key}: {value}'
            if not text in self.desktop_text:
                self.desktop_text.append(f'{key}: {value}')
        for i in range(len(self.desktop_text)):
            text = self.desktop_text[i]
            Label(screen, text,[400,200 +(i*30) ], color='#17667C', size=10, bg='#0DEAA1',shade=[None,None], outline='#2F4858', side='topleft')
        self.desktop_text.clear()
        if add.draw(screen) and file.bg =='#0DEAA1' and folder.bg =='#0DEAA1':
            if folder.output != '' and file.output != '':
                if folder.output in self.desktop_folders_files.keys():
                    self.desktop_folders_files[folder.output] = self.desktop_folders_files[folder.output] + file.output.split(',')
                else:
                    self.desktop_folders_files[folder.output] = file.output.split(',')
                folder.output = ''
                file.output = ''
                add.bg = '#0DEAA1'
            else:
                add.bg = '#FF6B46'

            if downloads.choice():
                self.desktop.build(f'{desktop_dir.output},{pathlib.Path.home()}/Downloads' ,self.desktop_folders_files)
            else:
                self.desktop.build(desktop_dir.output ,self.desktop_folders_files)
        if desktop_work.draw(screen):
            pass
        if back.draw(screen):
            self.page = 1

    def page_3(self,screen):
        Label(screen, 'Click to Copy',[WIDTH//2,120 ], color='#17667C', size=30, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858' )
        for i in range(len(self.copys['buttons'])):
            button = self.copys['buttons'][i]
            text = self.copys['text'][i]
            if button.draw(screen):
                self.clipboard.copy(text)
        if back.draw(screen):
            self.page = 1

    def page_2(self,screen):
        Label(screen, 'By: Kostia :)',[WIDTH//2, HEIGHT//2-50 ], color='#17667C', size=30, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858' )
        if back.draw(screen):
            self.page = 1

    def page_1(self, screen):
        Label(screen, 'Best Desktop',[WIDTH//2,160 ], color='#17667C', size=30, bg='#0DEAA1',shade=[None,'#2F4858'], outline='#2F4858' )
        if desktop.draw(screen):
            self.page = 4
        if clip.draw(screen):
            self.page = 3
        if credits.draw(screen):
            self.page = 2


def run_window():
    a = Main()
    a.update()



run_window()