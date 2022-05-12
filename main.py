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

def buildSamples():
    sampleMap = {}
    while len(sampleMap) < 100:
        entered = False
        while entered == False:
            x = randint(50, 448)
            y = randint(50, 448)
            try:
                a = sampleMap.get((x,y)).pos
                entered = False
            except:
                entered = True
                sampleMap.update({(x,y): Sample(Status.CLEAN, (x,y))})
    
    return sampleMap

#Main function
def main():
    run = True

    sampleList = buildSamples()
    sampleRect = []
    for pos in sampleList:
        sampleRect.append(pygame.Rect(sampleList[pos].pos[0], sampleList[pos].pos[1], 2, 2))

    #Game Loop
    while(run):

        #Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        

        #Drawing to screen
        WINDOW.fill(COLOR_GRAY)
        pygame.Surface.fill(WINDOW, COLOR_BLACK, simWindow)

        for rect in sampleRect:
            pygame.Surface.fill(WINDOW, COLOR_BLUE, rect)

        pygame.display.update()

#Call main function
if __name__ == "__main__":
    main()