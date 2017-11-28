from pygame.locals import *
import pygame
import time
from random import randint
import os

from walltest import *

block = []
vertexlist=[]
map_width = 576
map_height = 576
block_size = 64
w = int(map_width/block_size)
h = int(map_height/block_size)

class Vertex: #each lattice was a vertex
	vid = [0,0] #[x,y]
	adj = []	#vertexs that were adjacent
	src = None	#use for choosing direction
	def __init__(self, vid):
		self.vid = vid
		self.adj = []
		self.src = None

def adjacency(): #to create the relationship of each vertex, adj or not
	global w, h, wall_v, wall_h, vertexlist, block

	block = []
	vertexlist=[]
	for i in range(0, w):
		for j in range(0, h):
			v = Vertex([i,j])
			vertexlist.append(v)

	for i in range(0, w):
		for j in range(0, h):

			if i!=0:
				if not ([i,j] in wall_v): #left adj
					vertexlist[i*w+j].adj.append(vertexlist[(i-1)*w+j])
			if i!=(w-1):
				if not ([i+1,j] in wall_v): #right
					vertexlist[i*w+j].adj.append(vertexlist[(i+1)*w+j])
			if j!=0:
				if not ([i,j] in wall_h): #up
					vertexlist[i*w+j].adj.append(vertexlist[i*w+(j-1)])
			if j!=(h-1):
				if not ([i,j+1] in wall_h): #down
					vertexlist[i*w+j].adj.append(vertexlist[i*w+(j+1)])

	for v in vertexlist:
		if len(v.adj) == 0: #check if block, block means player can't get there.
			block.append(v.vid)

def choose_dir(ghost,pacman):# for ghost to choosing the direction, using bfs.
	global vertexlist, block, w, h

	if ghost == pacman:# if ghost and player are in a same lattice, ghost stop.
		return -1
	if (pacman in block) or (pacman[0]<0 or pacman[1]<0 or pacman[0]>w-1 or pacman[1]>h-1 ):
					   # if player is out of map or in block, ghost stop
		return -1
	g_x = ghost[0]
	g_y = ghost[1]
	p_x = pacman[0]
	p_y = pacman[1]
	p = vertexlist[p_x*w+p_y]
	V = list(vertexlist)
	#B-F-S
	visted = [False]*(w*h) #initialize the visited list, which recorded the vertex is visited or not
	Q =[] # Q is the Queue, contented the vertice that are waiting for the end of visited
	Q.append(V[g_x*w+g_y]) #the vertex which ghost was stay, is the first visited vertex 
	visted[g_x*w+g_y] = True
	for i in block:
		visted[i[0]*w+i[1]] = True # we will never visited the block-vertex, so at first we marked they are visited 
	for i in vertexlist: # initialize the src of vertex to None
		i.src = None

	while visted.count(False): # if there is any vertex has not been visited, do while
		t = Q.pop(0) # delete one vertex form visited queue
		for i in t.adj: # visited the vertex's adj
			if not visted[i.vid[0]*w+i.vid[1]]: 
				Q.append(i)	#if not visited, add i to the Queue 
				visted[i.vid[0]*w+i.vid[1]] = True # mark visited
				i.src = t # record the visiting order

	temp = V[pacman[0]*w+pacman[1]] # the vertex which player is stay
	
	while (temp.src).src != None and temp.src != None:
	# trace back to generating the path, and we can get which vertex the ghost should go next
		temp = temp.src	

	if temp.vid[0] == g_x: # using that vertex to choose the direction
		if temp.vid[1] > g_y:
			return 3
		else :
			return 2
	elif temp.vid[0] < g_x:
		return 1
	else:
		return 0

def choose_dir2(ghost,pacman):
	# similar to choose_dir(), is also using bfs to choose dircetion, however, with different visiting order for vertice
	global vertexlist, block, w, h

	if ghost == pacman:
		return -1
	if (pacman in block) or (pacman[0]<0 or pacman[1]<0 or pacman[0]>w-1 or pacman[1]>h-1 ):
		return -1
	g_x = ghost[0]
	g_y = ghost[1]
	p_x = pacman[0]
	p_y = pacman[1]
	p = vertexlist[p_x*w+p_y]
	V = list(vertexlist)
	visted = [False]*(w*h)
	Q =[]
	Q.append(V[g_x*w+g_y])
	visted[g_x*w+g_y] = True
	for i in block:
		visted[i[0]*w+i[1]] = True
	for i in vertexlist:
		i.src = None

	while visted.count(False):
		t = Q.pop(0)
		# print(len(t.adj),"yo")
		for i in range(0,len(t.adj)):

			j = len(t.adj)-1 - i
			# print(j)
			if not visted[t.adj[j].vid[0]*w+t.adj[j].vid[1]]:
				Q.append(t.adj[j])
				visted[t.adj[j].vid[0]*w+t.adj[j].vid[1]] = True
				t.adj[j].src = t

	temp = V[pacman[0]*w+pacman[1]]
	
	while (temp.src).src != None and temp.src != None:
		temp = temp.src	
	if temp.vid[0] == g_x:
		if temp.vid[1] > g_y:
			return 3
		else :
			return 2
	elif temp.vid[0] < g_x:
		return 1
	else:
		return 0
def choose_dir_power_mode(ghost,pacman):
	""" PowerMode means player has eat the Pellet, and ghost need to get away from player.
		Same idea of choose_dir(), by using bfs, we can get the farthest vertex for player,
		and use the farthest vertex as the destination, do bfs again to choose direction.
	"""
	global vertexlist, block, w, h
	if (pacman in block) or (pacman[0]<0 or pacman[1]<0 or pacman[0]>w-1 or pacman[1]>h-1 ):
		return -1
	g_x = ghost[0]
	g_y = ghost[1]
	p_x = pacman[0]
	p_y = pacman[1]
	p = vertexlist[p_x*w+p_y]
	V = list(vertexlist)
	visted = [False]*(w*h)
	Q =[]
	Q.append(V[p_x*w+p_y])
	visted[p_x*w+p_y] = True
	for i in block:
		visted[i[0]*w+i[1]] = True
	for i in vertexlist:
		i.src = None

	while visted.count(False):
		t = Q.pop(0)
		for i in t.adj:
			if not visted[i.vid[0]*w+i.vid[1]]:
				Q.append(i)
				visted[i.vid[0]*w+i.vid[1]] = True
				i.src = t
	# t is now the latest visited vertex, which means it is the farthest vertex for player
	f_x = t.vid[0]
	f_y = t.vid[1]
	# if ghost is already in the farthest vertex, randly choose direction 
	if g_x == f_x and g_y == f_y:
		for v in vertexlist:
			if [g_x, g_y] == v.vid:
				i = randint(0,len(v.adj)-1)
				print(i)
				if v.adj[i].vid[0] == g_x:
					if v.adj[i].vid[1] > g_y:
						return 3
					else :
						return 2
				elif v.adj[i].vid[0] < g_x:
					return 1
				else:
					return 0
	# Second time of bfs
	V = list(vertexlist)
	visted = [False]*(w*h)
	Q =[]
	Q.append(V[g_x*w+g_y])
	visted[g_x*w+g_y] = True
	for i in block:
		visted[i[0]*w+i[1]] = True
	for i in vertexlist:
		i.src = None

	while visted.count(False):
		t = Q.pop(0)
		for i in t.adj:
			if not visted[i.vid[0]*w+i.vid[1]]:
				Q.append(i)
				visted[i.vid[0]*w+i.vid[1]] = True
				i.src = t

	temp = V[f_x*w+f_y]
	while (temp.src).src != None and temp.src != None:
		temp = temp.src	
	if temp.vid[0] == g_x:
		if temp.vid[1] > g_y:
			return 3
		else :
			return 2
	elif temp.vid[0] < g_x:
		return 1
	else:
		return 0

def eraseBG(image): # set background opacity
	w, h = image.get_size()
	for x in range(w):
		for y in range(h):
			if image.get_at((x, y))[0] == 0 and image.get_at((x, y))[1] == 0 and image.get_at((x, y))[2] == 0:
				image.set_at((x, y), pygame.Color(0, 0, 0, 0))
	image.set_colorkey( (0,0,0), RLEACCEL )

class Dot:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def draw(self, surface):
		pygame.draw.circle(surface, [200, 200, 25], (self.x, self.y), 5, 0)

class Pellet:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.draw_count = 0 # for blinking animation
	def draw(self, surface):
		if self.draw_count < 4: 
			pygame.draw.circle(surface, [200, 200, 25], (self.x, self.y), 10, 0)
		self.draw_count = (self.draw_count + 1) % 8

class Wall:
	x = 0
	y = 0
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def draw_v(self, surface): # draw walls that are vertical
		pygame.draw.rect(surface, [0, 0, 255], (self.x-2.5, self.y-32, 5, 64))
	def draw_h(self, surface): # draw walls that are horizontal
		pygame.draw.rect(surface, [0, 0, 255], (self.x-32, self.y-2.5, 64, 5))

class Ghost:
	x = 320-32
	y = 320-32
	last_x = 320-32
	last_y = 320-32
	step = 4
	direction = 0
	move_c = 0
	pause_c = 0
	map_width = 576
	map_height = 576
	picwidth =32


	color = [255,0,0]
	block_size = 64
	_image_src = "img/Blinky.png"
	power_mode_image_count = 0
	_image_poewr_mode1 = pygame.image.load("img/ghost_powermode1.png")
	_image_poewr_mode1 = pygame.transform.scale(_image_poewr_mode1,(picwidth, picwidth))
	eraseBG(_image_poewr_mode1)
	_image_poewr_mode2 = pygame.image.load("img/ghost_powermode2.png")
	_image_poewr_mode2 = pygame.transform.scale(_image_poewr_mode2,(picwidth, picwidth))
	eraseBG(_image_poewr_mode2)

	def __init__(self):
		self._image = pygame.image.load(self._image_src)
		self._image = pygame.transform.scale(self._image,(self.picwidth, self.picwidth))
		eraseBG(self._image)
		self.image = self._image
		self.power_mode = False
		

	def on_init(self):
		self.x = 320-32
		self.y = 320-32
		self.last_x = 320-32
		self.last_y = 320-32
		self.direction = 0
		self.move_c = 0
		self.pause_c = 16	
		self.__init__()

	def update(self):
		""" to refresh the position of ghost """

		if self.pause_c !=0: # when game being start, ghost need to pause for a second, then can start to move.
			self.pause_c -= 1
			
		else:
			if self.direction == 0:
				self.x += self.step

			if self.direction == 1:
				self.x -= self.step

			if self.direction == 2:
				self.y -= self.step

			if self.direction == 3:
				self.y += self.step
			
			# check if out of map or not
			if self.x > self.map_width-self.picwidth:
				self.x = self.map_width-self.picwidth
			if self.x < 0:
				self.x = 0
			if self.y > self.map_height-self.picwidth:
				self.y = self.map_height-self.picwidth
			if self.y < 0:
				self.y = 0

		if self.power_mode: # for power_mode animation
			if self.power_mode_image_count < 2:
				self.image = self._image_poewr_mode1
			else:
				self.image = self._image_poewr_mode2

	def show_x(self):
		"""for displaying image at correct place """
		return self.x - self.picwidth/2
	def show_y(self):
		"""for displaying image at correct place """
		return self.y - self.picwidth/2
	def map_x(self):
		"""return which vertex was it in"""
		return int(self.x/self.block_size)
	def map_y(self):
		"""return which vertex was it in"""
		return int(self.y/self.block_size)
	def draw(self, surface):
		surface.blit(self.image, (self.show_x(), self.show_y()))


class Game:
	"""providing game logic"""
	picwidth = 32
	def isCollision_ghost(self, x1, y1, x2, y2, bsize):
		
		if x1 >= x2 and x1 <= x2+bsize:
			if y1 >= y2 and y1 <= y2+bsize:
				return True
		return False

	def isCollision_dot(self, x1, y1, x2, y2, bsize):
		
		if x1 >= x2 and x1 <= x2+bsize:
			if y1 >= y2 and y1 <= y2+bsize:
				return True
		return False

class App:

	GameWidth = 576
	GameHeight = 576
	textsurfHeight = 30
	windowHeigh = GameHeight + textsurfHeight
	windowWidth =576
	ghost = []
	dot = []
	pellet = []
	wall_v = []
	wall_h = []
	ghost_num = 0
	point = 0

	def __init__(self,Con):
		self._running = True
		self._display_surf = None
		self._image_surf = None
		self._text_surf = None
		self._msg_box_surf = None
		self.Con = Con
		self.GameHeight = self.Con.border_H * self.Con.block_size
		self.GameWidth = self.Con.border_W * self.Con.block_size
		self.windowHeigh = self.GameHeight + self.textsurfHeight
		self.windowWidth = self.GameWidth
		for i in list(self.Con.player):
			if type(self.Con.player[i]) != type('a'):
				self.sock = i
		self.game = Game()
		
	def on_init(self):
		pygame.font.init() # you have to call this at the start, if you want to use this module.
		pygame.mixer.music.load('music/pacman_siren.wav')
		self.effect_beginning = pygame.mixer.Sound('music/pacman_beginning.wav')
		self.effect_chomp = pygame.mixer.Sound('music/pacman_chomp.wav')
		self.effect_eatpill = pygame.mixer.Sound('music/pacman_eatpill.wav')
		self.effect_death = pygame.mixer.Sound('music/pacman_death.wav')
		self.effect_eatghost = pygame.mixer.Sound('music/pacman_eatghost.wav')
		self.effect_waza = pygame.mixer.Sound('music/pacman_waza.wav')
		self.scorefont = pygame.font.SysFont('Comic Sans MS', 18)

		adjacency()
		self.init_wall()
		self.init_dot()
		self.init_pellet()
		# Check if dot initail correctly or not
		del_c = 0
		for i in range(0, len(self.dot)):
			for j in range(0, len(self.wall_v)):
				if self.game.isCollision_wall_v(self.wall_v[j].x, self.wall_v[j].y, \
					self.dot[i-del_c].x, self.dot[i-del_c].y, 1):
					del self.dot[i-del_c]
					del_c += 1
					break
			for j in range(0, len(self.wall_h)):
				if self.game.isCollision_wall_h(self.wall_h[j].x, self.wall_h[j].y, \
					self.dot[i-del_c].x, self.dot[i-del_c].y, 1):
					del self.dot[i-del_c]
					del_c += 1
					break
		
		self.add_ghost([255,0,0], 320-32, 320-32)
		self.add_ghost([127,0,0], 256-32, 320-32)
		self.ghost[1]._image_src = "img/Inky.png"
		self.ghost[1].__init__()
		self.ghost[1].pause_c = 64

		self._running = True
		self.start_ticks = pygame.time.get_ticks()
		self.game_time_sec = int((pygame.time.get_ticks() - self.start_ticks)/1000) # milliseconds to seconds
		self.game_time_sec10 = int(self.game_time_sec/10)
		self.game_time_sec = int(self.game_time_sec%10)
		self.game_time_min = int(self.game_time_sec10/6)
		self.game_time_sec10 = int(self.game_time_sec10%6)

		self.life_image = pygame.image.load("img/pacman.png") # for displaying number of player's life
		self.life_image = pygame.transform.scale(self.life_image, (25, 25))

		self.on_loop()
		self.on_render()
		self.effect_beginning.play()
		time.sleep(4500.0 / 1000.0)
		pygame.mixer.music.play(-1, 0.0)

	def init_dot(self):
		global wall_v, wall_h, block
		for i in range(0, int(self.GameWidth/32)):
			for j in range(0, int(self.GameHeight/32)):
				if not([i/2,j/2] in block or [i, j] in [[6, 8], [7, 8], [8, 8], \
					[9, 8], [10, 8], [8, 7], [0, 0], [0, 16], [16, 0], [16, 16], [8, 12]]):
					self.dot.append(Dot((i+1)*32,(j+1)*32))

	def init_pellet(self):
		self.pellet.append(Pellet(0+32, 0+32))
		self.pellet.append(Pellet(0+32, 512+32))
		self.pellet.append(Pellet(512+32, 0+32))
		self.pellet.append(Pellet(512+32, 512+32))

	def init_wall(self):
		global wall_v, wall_h
		for i in range(0, len(wall_v)):
			self.wall_v.append(Wall(wall_v[i][0]*64, wall_v[i][1]*64+32))
		for i in range(0, len(wall_h)):
			self.wall_h.append(Wall(wall_h[i][0]*64+32, wall_h[i][1]*64))
		
	def add_ghost(self,color,x,y):
		self.ghost.append(Ghost()) 
		self.ghost[self.ghost_num].x = x
		self.ghost[self.ghost_num].y = y
		self.ghost[self.ghost_num].color = color
		self.ghost_num += 1

	def show_msg_box(self, color, msg):
		pygame.draw.rect(self._display_surf, color, (self.GameWidth/2-100, self.GameHeight/2-50, 200, 100))
		self._msg_box_surf = self.scorefont.render(msg, False, [0,0,0])
		self._display_surf.blit(self._msg_box_surf, (self.GameWidth/2-70, self.GameHeight/2-15))
		
		pygame.display.flip()

	def on_event(self, event):
		if event.type == QUIT:
			self._running = False

	def on_loop(self):
		"""each time we call on_loop(), we refresh the condition of game."""
		if len(self.dot) == 0 and len(self.pellet) == 0:
			# Finish game!
			pygame.mixer.music.stop()
			self.show_msg_box([125,125,0],"Completed!(ESC to End)")
			pygame.mixer.music.load('music/pacman_beginning.wav')
			pygame.mixer.music.play(-1, 0.0)
			while self._running:
				pygame.event.pump()
				keys = pygame.key.get_pressed()
				if (keys[pygame.K_ESCAPE]):
					self._running = False

		if self.Con.player[self.sock].life == 0:
			# Game Over!
			pygame.mixer.music.stop()
			self.show_msg_box([125,255,125],"GameOver!(ESC to End)")
			pygame.mixer.music.load('music/pacman_beginning.wav')
			pygame.mixer.music.play(-1, 0.0)
			while self._running:
				pygame.event.pump()
				keys = pygame.key.get_pressed()
				if (keys[pygame.K_ESCAPE]):
					self._running = False

		self.Con.player[self.sock].update()	# refresh player's position
		self.Con.player[self.sock].last_x = self.Con.player[self.sock].x
		self.Con.player[self.sock].last_y = self.Con.player[self.sock].y
		# for player's animation
		self.Con.player[self.sock].image_count = (self.Con.player[self.sock].image_count + 1) % 4 

		# refresh ghost's positon, each 16-times moves choosing direction once.
		g_c = 0 
		for g in self.ghost:
			if g.move_c == 0:
				if g.power_mode:
					g.direction = choose_dir_power_mode([g.map_x(),g.map_y()],\
						[self.Con.player[self.sock].map_x(),self.Con.player[self.sock].map_y()])
				else:
					if g_c ==0:
						g.direction = choose_dir([g.map_x(),g.map_y()],\
							[self.Con.player[self.sock].map_x(),self.Con.player[self.sock].map_y()])
					else:
						g.direction = choose_dir2([g.map_x(),g.map_y()],\
							[self.Con.player[self.sock].map_x(),self.Con.player[self.sock].map_y()])
					
			g_c += 1
			g.move_c = (g.move_c + 1)%16
			g.update()
			g.last_x = g.x
			g.last_y = g.y

		# Check if ghost has catch player or not
		for g in self.ghost:
			if self.game.isCollision_ghost(g.x, g.y, \
				self.Con.player[self.sock].show_x(), self.Con.player[self.sock].show_y(), 32):
				if g.power_mode:
					# in power_mode ghost was eaten.
					self.effect_eatghost.play()
					time.sleep(300.0 / 1000.0)
					self.point = self.point + 400
					g.on_init()
				else:
					# otherwise, player lose one life, and each ghost goes to starting position.
					self.effect_death.play()
					time.sleep(300.0 / 1000.0)
					for i in self.ghost:
						i.on_init()
					self.ghost[1].x = 256-32
					self.ghost[1].y = 320-32
					self.ghost[1].pause_c = 64
					self.Con.player[self.sock].life -= 1
					break
		# Check if player has catch dot or not
		for j in range(0, len(self.dot)):
			if self.game.isCollision_dot(self.dot[j].x, self.dot[j].y, \
				self.Con.player[self.sock].show_x(), self.Con.player[self.sock].show_y(), 32):
				del self.dot[j]	
				self.effect_chomp.play()
				self.point = self.point + 10
				break
		# Check if player has catch pellet or not
		for j in range(0, len(self.pellet)):
			if self.game.isCollision_dot(self.pellet[j].x, self.pellet[j].y, \
				self.Con.player[self.sock].show_x(), self.Con.player[self.sock].show_y(), 32):
				# if yes, power_mode on
				del self.pellet[j]
				self.effect_eatpill.play()
				pygame.mixer.music.stop()
				pygame.mixer.music.load('music/pacman_waza.wav')
				pygame.mixer.music.play(-1, 0.0)
				self.point = self.point + 100
				for g in self.ghost:
					g.power_mode =True
					g.power_mode_image_count = 0
				self.power_mode_start_time = pygame.time.get_ticks() # for clock of power_mode
				break	
		# Check if power_mode on or not	
		power_mode_off_c = 0
		for g in self.ghost:
			if g.power_mode == True:
				if (pygame.time.get_ticks() - self.power_mode_start_time)/1000 >= 10:
					power_mode_off_c += 1
					g.__init__()
					if power_mode_off_c == len(self.ghost):
						# every ghosts is out of power_mode, turn off the pwer mode
						pygame.mixer.music.stop()
						pygame.mixer.music.load('music/pacman_siren.wav')
						pygame.mixer.music.play(-1, 0.0)
				else:
					if (pygame.time.get_ticks() - self.power_mode_start_time)/1000 >= 7:
						# for power_mode off warning animation
						g.power_mode_image_count = (g.power_mode_image_count + 1) % 4
			else:
				power_mode_off_c += 1
		
		# for game time displaying
		self.game_time_sec = int((pygame.time.get_ticks() - self.start_ticks)/1000) # milliseconds to seconds
		self.game_time_sec10 = int(self.game_time_sec/10)
		self.game_time_sec = int(self.game_time_sec%10)
		self.game_time_min = int(self.game_time_sec10/6)
		self.game_time_sec10 = int(self.game_time_sec10%6)
		self._text_surf = self.scorefont.render("Time : "+str(self.game_time_min)+": "+str(self.game_time_sec10)\
			+str(self.game_time_sec)+"    Score : "+str(self.point), False, (255, 255, 255))
		
		pass

	def on_render(self):
		"""draw game screen in this function"""
		self._display_surf.fill((0,0,0))
		for i in range(0,len(self.wall_v)):
			self.wall_v[i].draw_v(self._display_surf)
		for i in range(0,len(self.wall_h)):
			self.wall_h[i].draw_h(self._display_surf)
		for i in range(0, len(self.dot)):
			self.dot[i].draw(self._display_surf)
		for i in range(0, len(self.pellet)):
			self.pellet[i].draw(self._display_surf)
		self.Con.player[self.sock].draw(self._display_surf)
		for i in range(0,len(self.ghost)):
			self.ghost[i].draw(self._display_surf)

		self._display_surf.blit(self._text_surf,(0,self.GameHeight))
		
		for i in range(0,self.Con.player[self.sock].life):
			self._display_surf.blit(self.life_image,(self.GameWidth/2 + i*27.5, self.GameHeight))

		pygame.display.flip()
		
	def on_cleanup(self):
		"""at the end of game, do initialization."""
		pygame.quit()
		for i in range(0, len(self.wall_v)):
			del self.wall_v[0]
		for i in range(0, len(self.wall_h)):
			del self.wall_h[0]
		for i in range(0, len(self.dot)):
			del self.dot[0]
		for i in range(0, len(self.pellet)):
			del self.pellet[0]
		for i in range(0, len(self.ghost)):
			del self.ghost[0]

	def on_execute(self):
		"""main function of App"""
		if self.on_init() == False:
			self._running = False
		pause = False
		while(self._running):
			pygame.event.pump()
			keys = pygame.key.get_pressed()
			if (keys[pygame.K_ESCAPE]):
				# enter "esc" to quit the game
				self._running = False

			if (keys[pygame.K_p]):
				# enter "p" to pause the game
				pause = True
				print("Pause")
				pygame.mixer.music.pause()
				self.show_msg_box([125,255,125],"Pause (p to Resume)")
				time.sleep(250.0 / 1000.0)

			while pause:
				# waiting for entering "p" to resume, or "esc" to quit
				pygame.event.pump()
				keys = pygame.key.get_pressed()
				if (keys[pygame.K_p]):
					pause = False
					print("Resume")
					pygame.mixer.music.unpause()
					time.sleep(250.0 / 1000.0)
				if (keys[pygame.K_ESCAPE]):
					pause = False
					self._running = False
					time.sleep(250.0 / 1000.0)

			self.on_loop()
			self.on_render()
			
			time.sleep(100.0 / 1000.0)
		self.on_cleanup()

if __name__ == "__main__" :
	theApp = App()
	theApp.on_execute()
