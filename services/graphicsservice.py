import pygame

class GraphicsService:
    def __init__(self):
        pygame.font.init()
        self.size = (1024, 500)
        self.middle = (self.size[0]/2, self.size[1]/2)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("OMAGAD IT WORKS !!")
        self.font = pygame.font.SysFont("monospace", 15)
        self.taps = []
    
    def draw_text(self, text, pos=(0, 0), color=(0, 0, 0)):
        label = self.font.render(text, 1, color)
        self.screen.blit(label, pos)
        
    def begin_draw(self):
        self.screen.fill((255, 255, 255))
        
    def draw_rect(self, x, y, w, h):
        pygame.draw.rect(self.screen, (0, 0, 0), [x, y, w, h])
    
    def end_draw(self):
        pygame.display.flip()
        
    def draw_taps(self):
        TAPS_COUNT = 100
        Y_BASE = self.size[1] * 3 / 4
        taps_size = self.size[0]/TAPS_COUNT
        tap_id = len(self.taps) - 1
        count = 0
        while tap_id >= 0 and count < TAPS_COUNT:
            tap = self.taps[tap_id]
            color = (0, 0, 255) if tap else (0, 0, 0)
            y = Y_BASE if tap else Y_BASE + 10
            w = self.size[0] / TAPS_COUNT
            x = count * w
            pygame.draw.rect(self.screen, color, [x, y, w, 2])
            tap_id -= 1
            count += 1
        
    def refresh(self, data):    
        ps = 4 # chunk division
        pw = 4 # pixel width
        
        chunk = data[0]
        bpm = data[1]
        tap = data[2]
        
        chunk_size = len(chunk)
        self.begin_draw()
        for i in range(0, len(chunk)/(ps)):
            d = chunk[i*ps]
            self.draw_rect(i*pw, self.size[1]/2, pw, d*self.size[1]/(2**16))
        
        if tap:
            pygame.draw.rect(self.screen, (255, 0, 0), [self.size[0]/2-25, self.size[1]/2-25, 50, 50])
            self.taps.append(True)
        else:
            self.taps.append(False)
            
        self.draw_taps()
        self.draw_text("BPM : " + str(int(bpm)))
        self.end_draw()
       