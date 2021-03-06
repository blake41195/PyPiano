import pygame
import os

unpressedPicList = ['key_white_Left_unpressed.png', 'key_black_unpressed.png', 'key_white_Middle_unpressed.png',
                    'key_black_unpressed.png', 'key_white_Right_unpressed.png', 'key_white_Left_unpressed.png',
                    'key_black_unpressed.png', 'key_white_Middle_unpressed.png',
                    'key_black_unpressed.png', 'key_white_Middle_unpressed.png', 'key_black_unpressed.png',
                    'key_white_Right_unpressed.png'
                    ] * 4

pressedPicList = ['key_white_Left_pressed.png', 'key_black_pressed.png', 'key_white_Middle_pressed.png',
                  'key_black_pressed.png', 'key_white_Right_pressed.png', 'key_white_Left_pressed.png',
                  'key_black_pressed.png', 'key_white_Middle_pressed.png',
                  'key_black_pressed.png', 'key_white_Middle_pressed.png', 'key_black_pressed.png',
                  'key_white_Right_pressed.png'
                  ] * 4
keyboard = [pygame.K_z, pygame.K_s, pygame.K_x, pygame.K_d, pygame.K_c, pygame.K_v, pygame.K_g, pygame.K_b, pygame.K_h,
            pygame.K_n, pygame.K_j, pygame.K_m, pygame.K_COMMA, pygame.K_l, pygame.K_PERIOD, pygame.K_COLON, pygame.K_SLASH,
            pygame.K_q, pygame.K_2, pygame.K_w, pygame.K_3, pygame.K_e, pygame.K_4, pygame.K_r, pygame.K_t, pygame.K_6,
            pygame.K_y, pygame.K_7, pygame.K_u, pygame.K_i, pygame.K_9, pygame.K_o, pygame.K_0, pygame.K_p, pygame.K_BREAK,
            pygame.K_LEFTBRACKET, pygame.K_DELETE, pygame.K_HOME, pygame.K_END, pygame.K_PAGEUP, pygame.K_PAGEDOWN,
            pygame.K_KP7, pygame.K_NUMLOCK, pygame.K_KP8, pygame.K_SLASH, pygame.K_KP9, pygame.K_ASTERISK, pygame.K_PLUS
            ]

Notes = ['c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab', 'a', 'bb', 'b']
oNotes = []
for octave in range(2, 6):
    for note in Notes:
        oNotes.append(note + str(octave))

notesPressedDict = dict(zip(oNotes, pressedPicList))
notesUnpressedDict = dict(zip(oNotes, unpressedPicList))
keyMappingDict = dict(zip(oNotes, keyboard))

KEYBOARDX = 5
KEYBAORDY = 10

# Various settings to test:
# pygame.mixer.pre_init(44100, -16, 2, 4096)  # 4096 is ++cpu
# pygame.mixer.pre_init(22050, -16, 2, 2048)
# pygame.mixer.pre_init(22050, -16, 1, 2048)
pygame.mixer.pre_init(44100, -16, 1, 2048)

pygame.init()

class Key(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.pressed = False
        self.image = pygame.image.load(os.path.join('pythonpiano_pictures', notesUnpressedDict[self.name]))
        self.imgPressed = pygame.image.load(os.path.join('pythonpiano_pictures', notesPressedDict[self.name]))
        self.imgUnpressed = pygame.image.load(os.path.join('pythonpiano_pictures', notesUnpressedDict[self.name]))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = 0
        self.rect.y = KEYBAORDY
        self._layer = 0
        self.color = 'white' if len(self.name) == 2 else 'black'
        self.mapping = 0
        try:
            self.mapping = keyMappingDict[self.name]
        except KeyError:
            self.mapping = 0

        # soundFile is changed based on what octave is set within the game.  The sound file is initialized with
        # the lowest octave
        self.soundFile = pygame.mixer.Sound(
            os.path.join('pythonpiano_sounds', f'piano-med-{self.name}.ogg'))

    def getImg(self):
        if self.pressed:
            return self.imgPressed
        else:
            return self.imgUnpressed

    def update(self):
        if self.pressed:
            self.image = self.imgPressed
        else:
            self.image = self.imgUnpressed

    def __str__(self):
        return self.name


class Game(object):
    winWidth = 850
    winHeight = 150
    win = pygame.display.set_mode([winWidth, winHeight])
    pygame.display.set_caption('PiPiano')
    background = pygame.Surface(win.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    keyboardx_position = KEYBOARDX

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.keys = pygame.sprite.LayeredUpdates()
        for note in oNotes:
            self.keys.add(Key(note))

        for key in self.keys:
            if key.color == 'white':
                key.rect.x = self.keyboardx_position
                self.keyboardx_position += key.width
            elif key.color == 'black':
                key.rect.x = self.keyboardx_position - int(key.width / 4)
                key._layer = 1

            self.background.blit(key.getImg(), key.rect)
        self.win.blit(self.background, (0, 0))

    def run(self):
        while self.running:
            self.clock.tick(100)
            self.handlerEvents()

            # Render Sprites
            for key in self.keys:
                key.update()
            self.keys.clear(self.win, self.background)
            dirty = self.keys.draw(self.win)
            pygame.display.update(dirty)

    def handlerEvents(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            for key in self.keys:
                if pressed[keyMappingDict[key.name]]:
                    key.pressed = True
                    key.soundFile.play()
            if event.type == pygame.KEYUP:
                for key in self.keys:
                    key.pressed = False
                    key.soundFile.fadeout(600)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key in self.keys:
                    if key.rect.collidepoint((mouseX, mouseY)) and mouseY + 52 - key.height > 0:
                        key.pressed = True
                        key.soundFile.play()
            if event.type == pygame.MOUSEBUTTONUP:
                for key in self.keys:
                    key.pressed = False
                    key.soundFile.fadeout(600)







if __name__ == '__main__':
    game = Game()
    game.run()
