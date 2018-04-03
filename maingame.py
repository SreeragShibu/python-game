import pygame
import sys
from pygame.locals import DOUBLEBUF,KEYDOWN,K_ESCAPE,FULLSCREEN,K_s,K_z
import random

screen = pygame.display.set_mode((1000,1000), DOUBLEBUF|FULLSCREEN)

clock=pygame.time.Clock()
k=0
health=100
enemyhealth=2000
class Enemylaser(pygame.sprite.Sprite):
	def __init__(self,x,y,group):
		super(Enemylaser,self).__init__()
		self.add(group)
		sheet=pygame.image.load("laser.png").convert_alpha()
		self.image=pygame.Surface((128,32),pygame.SRCALPHA).convert_alpha()
		self.image.blit(sheet,dest = (0,0),area=(0,0,128,32))

		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		
	def update(self):
		x,y=self.rect.center
		x-=40
		self.rect.center=x,y

class Mylaser(pygame.sprite.Sprite):
	def __init__(self,x,y,group):
		super(Mylaser,self).__init__()
		self.add(group)
		sheet=pygame.image.load("bullets.png").convert_alpha()
		self.image=pygame.Surface((300,162),pygame.SRCALPHA).convert_alpha()
		self.image.blit(sheet,dest = (0,0),area=(0,0,300,162))
		self.image=pygame.transform.scale(self.image,(100,100))
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)

	def update(self):
		
		x,y=self.rect.center
		x+=10
		self.rect.center=x,y

class Enemy(pygame.sprite.Sprite):
	def __init__(self,x,y,fighter,group,fire_group):
		super(Enemy,self).__init__()
		self.image=pygame.image.load("boss.png").convert_alpha()
		self.image=pygame.transform.scale(self.image,(300,300))
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		self.add(group)
		self.fighter=fighter
		self.velocity=0
		self.main_laser_counter=0
		self.fire_group=fire_group
	def update(self):
		f_x,f_y=self.fighter.rect.center
		s_x,s_y=self.rect.center
		if s_y>f_y:
			self.velocity= -1
		elif s_y<f_y:
			self.velocity=1
		else:
			self.velocity= 0
			if self.main_laser_counter !=10:
				self.main_laser_counter+=1
		if self.main_laser_counter==10:
			Enemylaser(s_x,s_y,[self.fire_group,all_sprites])
			
		s_y+=self.velocity
		self.rect.center=s_x,s_y

class ship(pygame.sprite.Sprite):
	def __init__(self,x,y,group,Myfire_group):
		super(ship,self).__init__()
		self.image=pygame.image.load("plane.png").convert_alpha()
		self.image=pygame.transform.scale(self.image,(100,100))
		self.rect = self.image.get_rect()
		self.rect.center=(x,y)
		self.add(group)
		self.Myfire_group=Myfire_group
	def update(self):
		x,y=pygame.mouse.get_pos()
		self.rect.center=(x,y)
		if k==1:
			Mylaser(x,y,[self.Myfire_group,all_sprites])
					
	

class MySprite(pygame.sprite.Sprite):
	def __init__(self,x,y,vel,group):
		super(MySprite, self).__init__()
		self.image = pygame.Surface((3,3))
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.center=(x,y)
		self.add(group)
		self.vel=vel
		self.col=0
		
	def update(self):
		self.col+= 20
		self.col%= 255
		x,y = self.rect.center
		
		if x>960:
			x=0
		
		x += self.vel	
		self.rect.center = x,y

all_sprites=pygame.sprite.Group()
fire_group=pygame.sprite.Group()
Myfire_group=pygame.sprite.Group()
background =pygame.Surface((1000,1000))

for i in range(100):
	x= random.randint(0,1000)
	y=random.randint(0,1000)
	MySprite(x,y,5,all_sprites)
for i in range(50):
	x= random.randint(0,1000)
	y=random.randint(0,1000)
	MySprite(x,y,15,all_sprites)
for i in range(25):
	x= random.randint(0,1000)
	y=random.randint(0,1000)
	MySprite(x,y,25,all_sprites)
	
#ship(320,240,all_sprites)
fighter=ship(320,240,all_sprites,Myfire_group)
enemyship=Enemy(800,240,fighter,all_sprites,fire_group)

while True :
    
		clock.tick(20)
		k=0
		for event in pygame.event.get():
			if event.type == KEYDOWN: #pressing_key
				if event.key == K_ESCAPE:
					print ("thanks for playing")
					sys.exit(0)
				if event.key == K_z:
					k=1
		
		collided=pygame.sprite.spritecollideany(fighter,fire_group)
		collided2=pygame.sprite.spritecollideany(enemyship,Myfire_group)
		if collided:
			collided.kill()
			health-=10
		if collided2:
			collided2.kill()
			enemyhealth-=20
		if health<0:
			print "game over!!"
			pygame.quit()
			sys.exit(0)
		if enemyhealth<0:
			print "game won!!"
			pygame.quit()
			sys.exit(0)
				 				
		all_sprites.clear(screen,background)
		all_sprites.update()
		all_sprites.draw(screen)		       
	

		pygame.display.flip()
	
raw_input()
