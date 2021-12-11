import pygame
import os
import distance as dis
# funciona en funcion del proteus
pygame.font.init()

TEXT_FONT = pygame.font.SysFont('comicsans', 10)
TITLE_FONT = pygame.font.Font("digital-7.ttf", 24)
DIGI_FONT = pygame.font.Font("digital-7.ttf", 72)
WIDTH, HEIGHT = 1300, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Distance Meter')
WHITE = (255,255,255)
BLACK = (0,0,0)
FPS = 60

IMAGE_WIDTHP = 30
IMAGE_HEIGHT = 50
IMAGE_WIDTHB = 20

BODY_IMAGE = pygame.image.load(os.path.join('image', 'ruleBody.png'))
END_IMAGE = pygame.image.load(os.path.join('image', 'ruleNib.png'))
IMG_BACK = pygame.image.load(os.path.join('image', 'background.jpg'))

BODY = pygame.transform.scale(BODY_IMAGE, (IMAGE_WIDTHB, IMAGE_HEIGHT))
END = pygame.transform.scale(END_IMAGE, (IMAGE_WIDTHP, IMAGE_HEIGHT))

POS_X = 30
POS_Y = HEIGHT/2
SCALE = 20
INICIO_X = 30
FIN_X = 1200
K = 61

def convert_to_dnumber(digit):
	if digit < 10:
		return '0'+str(digit)
	else:
		return str(digit)

def movement_left(ruler, current):
	if ruler.x - SCALE > 30:
		ruler.x -= SCALE

def movement_right(ruler):
	if ruler.x + SCALE <=1230:
		ruler.x += SCALE

def draw_window(ruler, start):
	current = dis.getDistance()
	print(current)
	#WIN.fill(WHITE)
	WIN.blit(IMG_BACK, (0,0))
	WIN.blit(TITLE_FONT.render('Distance Meter', 1, BLACK), (575, 20))
	WIN.blit(TITLE_FONT.render('Develop by:', 1, BLACK), (60, 300))
	WIN.blit(TITLE_FONT.render('Ramos Gomez Elisa', 1, WHITE), (60, 340))
	WIN.blit(TITLE_FONT.render('Sanchez Robles Andrea Selene', 1, WHITE), (60, 380))
	WIN.blit(TITLE_FONT.render('Velazquez Moreno Isaac', 1, WHITE), (60, 420))
	pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 55, WIDTH, 5))
	pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 233, WIDTH, 5))
	units_text = TEXT_FONT.render(str(), 1, BLACK)

	if current > start:
		while start*20+30 < current*20+30:
			start+=1
			ruler.x = start*20+30			
			pygame.draw.rect(WIN, (166,186,217), pygame.Rect(0, 60, ruler.x +30, 173))
			WIN.blit(END, (ruler.x, ruler.y -120))
		WIN.blit(DIGI_FONT.render(convert_to_dnumber(current), 1, WHITE), (620, 320))
	elif current < start:
		while start*20-30 > current*20-30:
			start-=1
			ruler.x = start*20-30			
			pygame.draw.rect(WIN, (166,186,217), pygame.Rect(0, 60, ruler.x +30, 173))
			WIN.blit(END, (ruler.x, ruler.y -120))
		WIN.blit(DIGI_FONT.render(convert_to_dnumber(current), 1, WHITE), (620, 320))
	else:
		while start == current:
			start=1
			ruler.x = start*30			
			pygame.draw.rect(WIN, (166,186,217), pygame.Rect(0, 60, ruler.x+30, 173))
			WIN.blit(END, (ruler.x, ruler.y -120))
		WIN.blit(DIGI_FONT.render(convert_to_dnumber(current), 1, WHITE), (620, 320))

	i = 30
	while i<ruler.x:
		WIN.blit(BODY, (i, ruler.y -120))
		i+=20

	start = current
		
	for i in range(K):
		LINE = pygame.Rect(60+(i*20), 60, 5, 20) # left, top, width, height
		pygame.draw.rect(WIN, BLACK, LINE)
		units_text = TEXT_FONT.render(str(i), 1, BLACK)
		WIN.blit(units_text, (60+(i*20), 95))
	pygame.display.update()


def main():
	start = 0
	ruler = pygame.Rect(POS_X, POS_Y, IMAGE_WIDTHP, IMAGE_HEIGHT)
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		draw_window(ruler, start)

	pygame.quit()

if __name__ == "__main__":
	main()
