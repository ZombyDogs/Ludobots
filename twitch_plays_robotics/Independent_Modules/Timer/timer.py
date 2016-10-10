import sys, pygame
import time

# -------------------- Variables ------------------

backgroundColor = 255, 255, 255

size = width, height = 800, 240

startTime = time.time()

asciiStartTime = time.asctime()

# -------------------- Functions ------------------

def Add_Text(textString,yOffset):

        label = myfont.render(textString, 1, (0,0,0))
        textrect = label.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery + yOffset*textrect.height

        screen.blit(label, textrect)

def Add_Ascii_Time(yOffset):

	textString = time.asctime()

	Add_Text(textString,yOffset)

def Add_Start_Time(yOffset):

	Add_Text(asciiStartTime,yOffset)

def Add_Time_Since_Start(yOffset):

        timeSinceStart = time.time() - startTime

        s = int(timeSinceStart)

        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
	d, h = divmod(h, 24)

        timer = ''

	timer = timer + str(d) + 'd '

        timer = timer + str(h) + 'h '

        timer = timer + str(m) + 'm '

        timer = timer + str(s) + 's '

	Add_Text(timer,yOffset)

# ---------------- Main function -----------------------

pygame.init()

screen = pygame.display.set_mode(size)

myfont = pygame.font.Font("Anonymous_Pro.ttf",26)

while 1:

        for event in pygame.event.get():

                if event.type == pygame.QUIT: sys.exit()

        screen.fill(backgroundColor)

	Add_Text('Experiment Start Time:',-3.5)

	Add_Start_Time(-2.5)

	Add_Text('Current Time:',-0.5)

	Add_Ascii_Time(0.5)

	Add_Text('Time Since Start:',2.5)

	Add_Time_Since_Start(3.5)

        pygame.display.flip()

	time.sleep(1)

