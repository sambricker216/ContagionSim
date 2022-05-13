from cmath import sqrt
from random import randint, random
import pygame

#Window dimensions
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

 #Sim Window
simWindow = pygame.Rect(50, 50, 400, 400)

#Constants
SAMPLE_COUNT = 500
IMMUNITY = 100
INFECT_TIME = 7
COOL_DOWN_TIME = 5
DEATH_RATE = 4
SPREAD_RATE = 70

#Color constants
COLOR_GRAY = (125, 125, 125)
COLOR_BLACK = (0,0,0)
COLOR_CYAN = (60, 223, 223)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_PURPLE = (200, 0, 200)

pygame.display.set_caption("Contagion Sim")

class Status:
    CLEAN = 0
    INFECTED = 1
    IMMUNIZED = 2
    COOL_DOWN = 3
    NEW_INFECT = 4

class Sample:
    def __init__(self, stat, pos):
        self.stat = stat
        self.pos = pos
        self.coolDown = 0
    
    def changeStat(self, newStat):
        self.stat = newStat
    
    def move(self, newPOS):
        self.pos = newPOS
    
    def updateSample(self):
        if self.stat == Status.NEW_INFECT:
            self.stat =  Status.INFECTED
            self.coolDown = INFECT_TIME
        elif self.stat == Status.INFECTED or self.stat == Status.COOL_DOWN:
            self.coolDown -= 1
            if self.coolDown == 0:
                self.stat = Status.COOL_DOWN
            elif self.coolDown == COOL_DOWN_TIME * -1:
                self.stat = Status.CLEAN

def distance(infectedPos, infecteePos):
    return (sqrt((infectedPos[0]-infecteePos[0]) ** 2 +(infectedPos[1]-infecteePos[1]) ** 2)).real

def infect(sampleList):
    for infector in sampleList:
        if infector.stat == Status.INFECTED:
            for infectee in sampleList:
                if infectee.stat == Status.CLEAN:
                    infectChance = randint(0, 99)
                    dist = distance(infector.pos, infectee.pos)
                    if dist < 5 and infectChance < SPREAD_RATE:
                        infectee.changeStat(Status.NEW_INFECT)
                    elif dist < 15 and infectChance < SPREAD_RATE/2:
                        infectee.changeStat(Status.NEW_INFECT)
                    elif dist < 30 and infectChance < SPREAD_RATE/4:
                        infectee.changeStat(Status.NEW_INFECT)

def moveSample(sample):
    range = randint(0,3)
    if range == 0 and sample.pos[0] < 445: #Right
        sample.move((sample.pos[0] + 3, sample.pos[1]))
    elif range == 1 and sample.pos[0] > 54: #Left
        sample.move((sample.pos[0] - 3, sample.pos[1]))
    elif range == 2 and sample.pos[1] > 54: #Up
        sample.move((sample.pos[0], sample.pos[1] - 2))
    elif range == 3 and sample.pos[1] < 445: #Down
        sample.move((sample.pos[0], sample.pos[1] + 2))

def buildSamples():
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
                    sampleMap[0].coolDown = INFECT_TIME
                elif len(sampleMap) <= IMMUNITY:
                    usedLocs.update({(x,y): True})
                    sampleMap.append(Sample(Status.IMMUNIZED, (x,y)))
                else:
                    usedLocs.update({(x,y): True})
                    sampleMap.append(Sample(Status.CLEAN, (x,y)))
    
    return sampleMap

#Main function
def main():
    run = True

    samples = buildSamples()
    mouse = [-1,-1]

    #Game Loop
    while(run):

        #Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                if 600 <= mousePos[0] <= 700 and 100 <= mousePos[1] <= 150:
                    for sample in samples:
                        sample.updateSample()
                        if sample.stat == Status.INFECTED:
                            rng = randint(0, 99)
                            deathChance = DEATH_RATE/(sample.coolDown)
                            if rng < deathChance:
                                samples.remove(sample)
                    for sample in samples:
                        moveSample(sample)
                    infect(samples)
        
        sampleRect = []
        for num in range(len(samples)):
            sampleRect.append(pygame.Rect(samples[num].pos[0], samples[num].pos[1], 2, 2))

        #Drawing to screen
        WINDOW.fill(COLOR_GRAY)
        pygame.Surface.fill(WINDOW, COLOR_BLACK, simWindow)

        for num in range(len(samples)):
            if samples[num].stat == Status.INFECTED:
               pygame.Surface.fill(WINDOW, COLOR_RED, sampleRect[num])
            elif samples[num].stat == Status.IMMUNIZED:
               pygame.Surface.fill(WINDOW, COLOR_CYAN, sampleRect[num])
            elif samples[num].stat == Status.COOL_DOWN:
               pygame.Surface.fill(WINDOW, COLOR_GREEN, sampleRect[num])
            elif samples[num].stat == Status.NEW_INFECT:
               pygame.Surface.fill(WINDOW, COLOR_PURPLE, sampleRect[num])  
            else:
               pygame.Surface.fill(WINDOW, COLOR_BLUE, sampleRect[num])
        
        #Move button
        moveButton = pygame.Rect(600,100,100,50)
        pygame.Surface.fill(WINDOW, COLOR_BLACK, moveButton)

        pygame.display.update()

        if run is False:
            print(len(samples))
    
#Call main function
if __name__ == "__main__":
    main()