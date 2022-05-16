from cmath import sqrt, log
from random import randint, random
import pygame

pygame.init()

#Window dimensions
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#Sim Window
simWindow = pygame.Rect(50, 50, 400, 400)

#Constants
SAMPLE_COUNT = 500
IMMUNITY = 250
INFECT_TIME = 4
COOL_DOWN_TIME = 6
DEATH_RATE = 3
SPREAD_RATE = 40
CLOCK = pygame.time.Clock()
FPS = 50
MULTI_REPS = 100
FONT = pygame.font.Font('Roboto-Black.ttf', 24)
SMALL_FONT = pygame.font.Font('Roboto-Black.ttf', 20)
SIM_NUM = 0
INFECTIONS = 1

#INPUT TEXT
TEXT_SELECT = 0
IM_TEXT = ""
INT_TEXT = ""
CDT_TEXT = ""
DR_TEXT = ""
SR_TEXT = ""

#Color constants
COLOR_GRAY = (125, 125, 125)
COLOR_BLACK = (0,0,0)
COLOR_CYAN = (60, 223, 223)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_PURPLE = (200, 0, 200)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)

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
        self.immunity = 0
    
    def changeStat(self, newStat):
        self.stat = newStat
    
    def move(self, newPOS):
        self.pos = newPOS
    
    def updateSample(self):
        if self.stat == Status.NEW_INFECT:
            self.stat =  Status.INFECTED
            self.coolDown = INFECT_TIME
        elif self.stat == Status.INFECTED:
            self.coolDown -= 1
            if self.coolDown == 0:
                self.immunity += 1
                if COOL_DOWN_TIME == 0:
                    self.stat = Status.CLEAN
                else:
                    self.stat = Status.COOL_DOWN
        elif self.stat == Status.COOL_DOWN:
            if self.coolDown == -1 * COOL_DOWN_TIME + 1:
                self.stat = Status.CLEAN
            else:
                self.coolDown -= 1

def distance(infectedPos, infecteePos):
    return (sqrt((infectedPos[0]-infecteePos[0]) ** 2 +(infectedPos[1]-infecteePos[1]) ** 2)).real

def infect(sampleList):
    global INFECTIONS
    for infector in sampleList:
        if infector.stat == Status.INFECTED:
            for infectee in sampleList:
                if infectee.stat == Status.CLEAN:
                    infectChance = (randint(0, 99) * log(infectee.immunity + 4, 4)).real
                    dist = distance(infector.pos, infectee.pos)
                    if (dist < 5 and infectChance < SPREAD_RATE) or (dist < 15 and infectChance < SPREAD_RATE/2) or (dist < 30 and infectChance < SPREAD_RATE/4):
                        infectee.changeStat(Status.NEW_INFECT)
                        INFECTIONS += 1

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


def reset():
    global SIM_NUM, INFECTIONS
    SIM_NUM = 0
    INFECTIONS = 1
    return buildSamples()

def singleSim(samples):
    global SIM_NUM
    SIM_NUM += 1
    for sample in samples:
        sample.updateSample()
        if sample.stat == Status.INFECTED:
            rng = randint(0, 999)
            deathChance = DEATH_RATE/(INFECT_TIME - sample.coolDown + 1)
            if rng < deathChance:
                samples.remove(sample)
    for sample in samples:
        moveSample(sample)
    infect(samples)
    return samples

def visuals(samples):
    global SIM_NUM, INFECTIONS

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
            pygame.Surface.fill(WINDOW, COLOR_YELLOW, sampleRect[num])
        elif samples[num].stat == Status.NEW_INFECT:
            pygame.Surface.fill(WINDOW, COLOR_PURPLE, sampleRect[num])  
        else:
            sampleColor = COLOR_BLUE
            if(20 * samples[num].immunity < 255):
                sampleColor = (0, COLOR_BLUE[1] + 20 * samples[num].immunity, COLOR_BLUE[2] - 20 * samples[num].immunity)
            else:
                sampleColor = COLOR_GREEN
            pygame.Surface.fill(WINDOW, sampleColor, sampleRect[num])

    #Text Displays
    moveButton = pygame.Rect(490,50,170,50)
    moveButtonText = FONT.render('Single Sim', True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, moveButton)
    WINDOW.blit(moveButtonText, moveButton.topleft)

    resetButton = pygame.Rect(490,120,170,50)
    resetButtonText = FONT.render('Reset', True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, resetButton)
    WINDOW.blit(resetButtonText, resetButton.topleft)
    
    multiButton = pygame.Rect(490,190,170,50)
    multiButtonText = FONT.render('Multi Sim', True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, multiButton)
    WINDOW.blit(multiButtonText, multiButton.topleft)

    popButton = pygame.Rect(490,260,170,50)
    popButtonText = FONT.render('Pop size = ' + str(len(samples)), True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, popButton)
    WINDOW.blit(popButtonText, popButton.topleft)

    simButton = pygame.Rect(490,330,170,50)
    simButtonText = SMALL_FONT.render('Sim num = ', True, COLOR_WHITE, COLOR_BLACK)
    simButtonNum = SMALL_FONT.render(str(SIM_NUM), True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, simButton)
    WINDOW.blit(simButtonText, simButton.topleft)
    WINDOW.blit(simButtonNum, (simButton.bottomleft[0], simButton.bottomleft[1] - 25))

    infButton = pygame.Rect(490,400,170,50)
    infButtonText = FONT.render('Infections = ', True, COLOR_WHITE, COLOR_BLACK)
    infButtonNum = SMALL_FONT.render(str(INFECTIONS), True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, infButton)
    WINDOW.blit(infButtonText, infButton.topleft)
    WINDOW.blit(infButtonNum, (infButton.bottomleft[0], infButton.bottomleft[1] - 25))

    drButton = pygame.Rect(690,50,170,50)
    drButtonText = SMALL_FONT.render('DRate/Infection = ', True, COLOR_WHITE, COLOR_BLACK)
    drButtonNum = SMALL_FONT.render(str( round(100 * (SAMPLE_COUNT - len(samples))/INFECTIONS, 2)  ), True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, drButton)
    WINDOW.blit(drButtonText, drButton.topleft)
    WINDOW.blit(drButtonNum, (drButton.bottomleft[0], drButton.bottomleft[1] - 25))

    global IM_TEXT, INT_TEXT, CDT_TEXT, DR_TEXT, SR_TEXT

    im_text_button = pygame.Rect(690,120,170,50)
    im_text_button_text = SMALL_FONT.render('Immune Count = ', True, COLOR_WHITE, COLOR_BLACK)
    im_text_button_val = SMALL_FONT.render( IM_TEXT , True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, im_text_button)
    WINDOW.blit(im_text_button_text, im_text_button.topleft)
    WINDOW.blit(im_text_button_val, (im_text_button.bottomleft[0], im_text_button.bottomleft[1] - 25))

    int_text_button = pygame.Rect(690,190,170,50)
    int_text_button_text = SMALL_FONT.render('Infect Time = ', True, COLOR_WHITE, COLOR_BLACK)
    int_text_button_val = SMALL_FONT.render( INT_TEXT , True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, int_text_button)
    WINDOW.blit(int_text_button_text, int_text_button.topleft)
    WINDOW.blit(int_text_button_val, (int_text_button.bottomleft[0], int_text_button.bottomleft[1] - 25))

    cd_text_button = pygame.Rect(690,260,170,50)
    cd_text_button_text = SMALL_FONT.render('Cool Down = ', True, COLOR_WHITE, COLOR_BLACK)
    cd_text_button_val = SMALL_FONT.render( CDT_TEXT , True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, cd_text_button)
    WINDOW.blit(cd_text_button_text, cd_text_button.topleft)
    WINDOW.blit(cd_text_button_val, (cd_text_button.bottomleft[0], cd_text_button.bottomleft[1] - 25))

    dr_text_button = pygame.Rect(690,330,170,50)
    dr_text_button_text = SMALL_FONT.render('Mortality = ', True, COLOR_WHITE, COLOR_BLACK)
    dr_text_button_val = SMALL_FONT.render( DR_TEXT , True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, dr_text_button)
    WINDOW.blit(dr_text_button_text, dr_text_button.topleft)
    WINDOW.blit(dr_text_button_val, (dr_text_button.bottomleft[0], dr_text_button.bottomleft[1] - 25))

    sr_text_button = pygame.Rect(690,400,170,50)
    sr_text_button_text = SMALL_FONT.render('Spread Rate = ', True, COLOR_WHITE, COLOR_BLACK)
    sr_text_button_val = SMALL_FONT.render( SR_TEXT , True, COLOR_WHITE, COLOR_BLACK)
    pygame.Surface.fill(WINDOW, COLOR_BLACK, sr_text_button)
    WINDOW.blit(sr_text_button_text, sr_text_button.topleft)
    WINDOW.blit(sr_text_button_val, (sr_text_button.bottomleft[0], sr_text_button.bottomleft[1] - 25))

    pygame.display.update()

def multiSim(samples, visual):
    
    for num in range(MULTI_REPS):
        samples = singleSim(samples)
        
        if(visual == True):
            CLOCK.tick(FPS)
            visuals(samples)
    
    return samples

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
                global TEXT_SELECT
                if 490 <= mousePos[0] <= 660 and 50 <= mousePos[1] <= 100:
                   samples = singleSim(samples)
                elif 490 <= mousePos[0] <= 660 and 120 <= mousePos[1] <= 170:
                    samples = reset()
                elif 490 <= mousePos[0] <= 660 and 190 <= mousePos[1] <= 240:
                    samples = multiSim(samples, True)
                elif 690 <= mousePos[0] <= 860 and 120 <= mousePos[1] <= 170:
                    TEXT_SELECT = 0
                elif 690 <= mousePos[0] <= 860 and 190 <= mousePos[1] <= 240:
                    TEXT_SELECT = 1
                elif 690 <= mousePos[0] <= 860 and 260 <= mousePos[1] <= 310:
                    TEXT_SELECT = 2
                elif 690 <= mousePos[0] <= 860 and 330 <= mousePos[1] <= 380:
                    TEXT_SELECT = 3
                elif 690 <= mousePos[0] <= 860 and 400 <= mousePos[1] <= 450:
                    TEXT_SELECT = 4
                
            elif event.type == pygame.KEYUP and (pygame.K_0 <= event.key <= pygame.K_9 or event.key == pygame.K_BACKSPACE):
                global IM_TEXT, INT_TEXT, CDT_TEXT, DR_TEXT, SR_TEXT, IMMUNITY, INFECT_TIME, COOL_DOWN_TIME, SPREAD_RATE, DEATH_RATE
                if(TEXT_SELECT == 0):
                    if event.key == pygame.K_BACKSPACE:
                        IM_TEXT = IM_TEXT[:-1]
                    else:
                        IM_TEXT += event.unicode
                    
                    if(len(IM_TEXT) == 0):
                        IMMUNITY = 0
                    else:
                        IMMUNITY = int(IM_TEXT)

                elif(TEXT_SELECT == 1):
                    if event.key == pygame.K_BACKSPACE:
                        INT_TEXT = INT_TEXT[:-1]
                    else:
                        INT_TEXT += event.unicode

                    if(len(INT_TEXT) == 0):
                        INFECT_TIME = 0
                    else:
                        INFECT_TIME = int(INT_TEXT)
                    
                elif(TEXT_SELECT == 2):
                    if event.key == pygame.K_BACKSPACE:
                        CDT_TEXT = CDT_TEXT[:-1]
                    else:
                        CDT_TEXT += event.unicode

                    if(len(CDT_TEXT) == 0):
                        COOL_DOWN_TIME = 0
                    else:
                        COOL_DOWN_TIME = int(CDT_TEXT)

                elif(TEXT_SELECT == 3):
                    if event.key == pygame.K_BACKSPACE:
                        DR_TEXT = DR_TEXT[:-1]
                    else:
                        DR_TEXT += event.unicode
                    
                    if(len(DR_TEXT) == 0):
                        DEATH_RATE = 0
                    else:
                        DEATH_RATE = int(DR_TEXT)

                elif(TEXT_SELECT == 4):
                    if event.key == pygame.K_BACKSPACE:
                        SR_TEXT = SR_TEXT[:-1]
                    else:
                        SR_TEXT += event.unicode

                    if(len(SR_TEXT) == 0):
                        SPREAD_RATE = 0
                    else:
                        SPREAD_RATE = int(SR_TEXT)

        visuals(samples)
    
#Call main function
if __name__ == "__main__":
    main()