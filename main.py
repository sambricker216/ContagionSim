from asyncio.windows_events import NULL
from random import randint, random
import pygame

#Window dimensions
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

 #Sim Window
simWindow = pygame.Rect(50, 50, 400, 400)

#Color constants
COLOR_GRAY = (125, 125, 125)
COLOR_BLACK = (0,0,0)
COLOR_CYAN = (60, 223, 223)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

pygame.display.set_caption("Contagion Sim")

class Status:
    CLEAN = 0
    INFECTED = 1
    IMMUNIZED = 2
    COOL_DOWN = 3

class Sample:
    def __init__(self, stat, pos):
        self.stat = stat
        self.pos = pos
    
    def changeStat(self, newStat):
        self.stat = newStat
    
    def move(self, newPOS):
        self.pos = newPOS

def buildSamples(immunized):
    sampleMap = []
    usedLocs = {}
    while len(sampleMap) < 100:
        entered = False
        while entered == False:
            x = randint(50, 448)
            y = randint(50, 448)
            try:
                a = usedLocs[(x,y)]
            except:
                entered = True
                if len(sampleMap) == 0:
                    usedLocs.update({(x,y): True})
                    sampleMap.append(Sample(Status.INFECTED, (x,y)))
                elif len(sampleMap) <= immunized:
                    usedLocs.update({(x,y): True})
                    sampleMap.append(Sample(Status.IMMUNIZED, (x,y)))
                else:
                    usedLocs.update({(x,y): True})
                    sampleMap.append(Sample(Status.CLEAN, (x,y)))
    
    return sampleMap

#Main function
def main():
    run = True

    samples = buildSamples(60)

    #Game Loop
    while(run):

        #Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        sampleRect = []
        for num in range(100):
            sampleRect.append(pygame.Rect(samples[num].pos[0], samples[num].pos[1], 2, 2))

        #Drawing to screen
        WINDOW.fill(COLOR_GRAY)
        pygame.Surface.fill(WINDOW, COLOR_BLACK, simWindow)

        for num in range(100):
            if samples[num].stat == Status.INFECTED:
               pygame.Surface.fill(WINDOW, COLOR_RED, sampleRect[num])
            elif samples[num].stat == Status.IMMUNIZED:
               pygame.Surface.fill(WINDOW, COLOR_CYAN, sampleRect[num])
            elif samples[num].stat == Status.COOL_DOWN:
               pygame.Surface.fill(WINDOW, COLOR_GREEN, sampleRect[num])
            else:
               pygame.Surface.fill(WINDOW, COLOR_BLUE, sampleRect[num]) 

        pygame.display.update()
    
#Call main function
if __name__ == "__main__":
    main()