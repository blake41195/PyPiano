import pygame
import os

unpressedPicList = ['key_white_Left_unpressed.png', 'key_black_unpressed.png', 'key_white_Middle_unpressed.png',
                    'key_black_unpressed.png', 'key_white_Right_unpressed.png', 'key_white_Left_unpressed.png',
                    'key_black_unpressed.png', 'key_white_Middle_unpressed.png',
                    'key_black_unpressed.png', 'key_white_Middle_unpressed.png', 'key_black_unpressed.png',
                    'key_white_Right_unpressed.png'
                    ]

pressedPicList = ['key_white_Left_pressed.png', 'key_black_pressed.png', 'key_white_Middle_pressed.png',
                  'key_black_pressed.png', 'key_white_Right_pressed.png', 'key_white_Left_pressed.png',
                  'key_black_pressed.png', 'key_white_Middle_pressed.png',
                  'key_black_pressed.png', 'key_white_Middle_pressed.png', 'key_black_pressed.png',
                  'key_white_Right_pressed.png'
                  ]

Notes = ['c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab', 'a', 'bb', 'b']

notesPressedDict = dict(zip(Notes, pressedPicList))
notesUnpressedDict = dict(zip(Notes, unpressedPicList))

KEYBOARDX = 5
KEYBAORDY = 10


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
        self.color = 'white' if len(self.name) == 1 else 'black'

        # soundFile is changed based on what octave is set within the game.  The sound file is initialized with
        # the lowest octave
        self.soundFile = None

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


class Game(object):
    winWidth = 500
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
        self.octave = 2
        self.keys = pygame.sprite.LayeredUpdates()
        for note in Notes:
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

    def updateOctave(self):
        for key in self.keys:
            key.soundFile = pygame.mixer.Sound(
                os.path.join('pythonpiano_sounds', f'piano-med-{key.name}{self.octave}.ogg'))

    def run(self):
        # Various settings to test:
        # pygame.mixer.pre_init(44100, -16, 2, 4096)  # 4096 is ++cpu
        # pygame.mixer.pre_init(22050, -16, 2, 2048)
        # pygame.mixer.pre_init(22050, -16, 1, 2048)
        pygame.mixer.pre_init(44100, -16, 1, 2048)

        pygame.init()
        self.updateOctave()

        while self.running:
            self.clock.tick()
            self.handlerEvents()

            # Render Sprites
            for key in self.keys:
                key.update()
            self.keys.clear(self.win, self.background)
            dirty = self.keys.draw(self.win)
            pygame.display.update(dirty)

    def handlerEvents(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.octave < 5:
                self.octave += 1
                self.updateOctave()
        elif keys[pygame.K_DOWN]:
            if self.octave > 2:
                self.octave -= 1
                self.updateOctave()
        for event in pygame.event.get():
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
