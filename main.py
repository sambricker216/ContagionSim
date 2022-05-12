from asyncio.windows_events import NULL
from random import randint, random
import pygame

#Window dimensions
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

 #Sim Window
simWindow = pygame.Rect(50, 50, 400, 400)

#Sample count
SAMPLE_COUNT = 500

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

def moveSample(sample):
    range = randint(0,3)
    if range == 0 and sample.pos[0] < 446: #Right
        sample.move((sample.pos[0] + 2, sample.pos[1]))
    elif range == 1 and sample.pos[0] > 53: #Left
        sample.move((sample.pos[0] - 2, sample.pos[1]))
    elif range == 2 and sample.pos[1] > 53: #Up
        sample.move((sample.pos[0], sample.pos[1] - 2))
    elif range == 3 and sample.pos[1] < 446: #Down
        sample.move((sample.pos[0], sample.pos[1] + 2))

def buildSamples(immunized):
    sampleMap = []
    usedLocs = {}
    while len(sampleMap) < SAMPLE_COUNT:
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
    mouse = [-1,-1]

    #Game Loop
    while(run):

        #Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                print(mousePos)
                if 600 <= mousePos[0] <= 700 and 100 <= mousePos[1] <= 150:
                    print("move")
                    for sample in samples:
                        moveSample(sample)
        
        sampleRect = []
        for num in range(SAMPLE_COUNT):
            sampleRect.append(pygame.Rect(samples[num].pos[0], samples[num].pos[1], 2, 2))

        #Drawing to screen
        WINDOW.fill(COLOR_GRAY)
        pygame.Surface.fill(WINDOW, COLOR_BLACK, simWindow)

        for num in range(SAMPLE_COUNT):
            if samples[num].stat == Status.INFECTED:
               pygame.Surface.fill(WINDOW, COLOR_RED, sampleRect[num])
            elif samples[num].stat == Status.IMMUNIZED:
               pygame.Surface.fill(WINDOW, COLOR_CYAN, sampleRect[num])
            elif samples[num].stat == Status.COOL_DOWN:
               pygame.Surface.fill(WINDOW, COLOR_GREEN, sampleRect[num])
            else:
               pygame.Surface.fill(WINDOW, COLOR_BLUE, sampleRect[num])
        
        #Move button
        moveButton = pygame.Rect(600,100,100,50)
        pygame.Surface.fill(WINDOW, COLOR_BLACK, moveButton)

        pygame.display.update()
    
#Call main function
if __name__ == "__main__":
    main()