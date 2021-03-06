import pygame, sys
from pygame.locals import *
from random import choice

## Clase Coordenada ##
class Coordenada:
	## Inicializador ##
	def __init__(self, x = 0, y = 0):
		self._x = x # Creacion variable x
		self._y = y	# Creacion variable y
	def set_x(self, x): # metodo set de x
		self._x = x
	def set_y(self, y): # metodo set de y
		self.y = y
	def set(self, x, y):# metodo para establecer x, y
		self.set_x(x)
		self.set_y(y)	
	def __str__(self):
		return str(self._x) + "," + str(self._y)

## Clase Nodo ##
class Neurona:
	def __str__(self):
		return self._nombre
	## Inicializador ##
	def __init__(self, nombre, status, sipnapsis, jugador_humano, coordenada):
		self._coordenada = coordenada # Creacion de una variable de tipo Coordenada (coordenada del movimiento)
		self._nombre = nombre # Creacion variable nombre (nombre del grafo)
		self._status = status # Ceacion variable status (para saber si con el ultimo mov se perdio o gano o empato)
		self._sipnapsis = sipnapsis # Creacion de la variable sipnapsis (para establecer las conexiones entre los nodos)		
		self._jugador_humano = jugador_humano # Creacion de la variable jugador_humano (para saber quien hizo el movimiento)
	def set_coordenada(self, coordenada): # metodo set de coordenada
		self._coordenada = coordenada
	def set_nombre(self, nombre): # metodo set de nombre
		self._nombre = nombre
	def set_status(self, status): # metodo set de status
		self._status = status
	def add_sipnapsis(self, new_neurona): # metodo para agregar un nuevo nodo
		self._sipnapsis[new_neurona._nombre] = new_node 
	def set_jugador_humano(self, value): # metodo set de jugador_humano
		self._jugador_humano = value

## Clase cerebro ##
class Cerebro:	
	def __init__(self):
		self._neurona_actual = None
		self._neurona_anterior = None
		self._neuronas = {}
	def add_neurona(self, neurona):
		print "Agregar neurona = " + str(neurona) ## Debug
		if self._neurona_actual == None and not self._neuronas.has_key(neurona._nombre): ## 1er movimiento sin memoria
			self._neuronas[neurona._nombre] = self._neurona_actual = neurona
		elif self._neurona_actual == None and self._neuronas.has_key(neurona._nombre): ## 1er movimiento con memoria
			self._neurona_actual = self._neuronas[neurona._nombre]
		elif not self._neurona_actual == None:
			if self._neurona_actual._sipnapsis.has_key(neurona._nombre):
				self._neurona_anterior = self._neurona_actual
				self._neurona_actual = self._neurona_actual._sipnapsis[neurona._nombre]
			else:
				self._neurona_anterior = self._neurona_actual
				self._neurona_actual._sipnapsis[neurona._nombre] = neurona
				self._neurona_actual = neurona
		else:
			print "Error in logic"

	def analizar_mov(self, matriz):
		print "Analizar Neurona = " + str(self._neurona_actual) ## debug
		print "Coord = " + str(self._neurona_actual._coordenada)
		print "Cantidad de sipnapsis(neurona actual) = " + str(len(self._neurona_actual._sipnapsis.keys())) ## debug
		for neu in self._neurona_actual._sipnapsis.keys():
			print "--> Neurona Actual sipnapsis = " + str(neu)

		if len(self._neurona_actual._sipnapsis.keys()) == 0:
			movs = []
			for i in range(3):
				for j in range(3):
					if matriz[i][j] == 0:
						movs.append([i, j]) # anexa movimientos validos
			if len(movs) > 0: # si hay movimientos disponibles							
				x, y = choice(movs) # regresa x, y				
 				return Neurona(str(x) + ":" + str(y), '', { }, False, Coordenada(x, y))				
			else:
				return False
		else:
			return False



## Clase Gato ##
class Gato:
	def __init__(self, cerebro):
		## Inicializacion de las librerias ##
		pygame.init()
		## cerebro ##
		self._cerebro = cerebro
		## Tamanioo de la ventana
		self._height = 600
		self._width  = 600
		self._bloque_largo = self._height / 3 ## Ancho ##
		self._bloque_ancho = self._width / 3 ## largo ##
		self._size = self._height, self._width
		## Colores ##
		self._blanco = pygame.Color(255, 255, 255)
		self._negro  =   pygame.Color(0, 0, 0)
		## Preparar la ventana ##
		self._ventana = pygame.display.set_mode(self._size)
		## Inicializar el turno ## 
		self._turno_humano = True
		## Preparar Matriz ##
		self._matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] ## -0 vacio, 1 computadora, 2 jugador
		## FPS del programa ##
		self._fps = pygame.time.Clock()
	
	def dibujar_tablero(self):
		## Fondo de Ventana ##
		self._ventana.fill(self._blanco)
		###########################################################
		###########################################################
		##########  										#######
		##########         DIBUJO DE LOS ELEMENTOS 			#######  
		##########											#######
		###########################################################
		###########################################################
		stroke = 5 ## grosor ##
		## Lineas Verticales ##	
		pygame.draw.line(self._ventana, self._negro, (self._bloque_largo, 0), (self._bloque_largo, self._width), stroke) ## 1ra linea ##
		pygame.draw.line(self._ventana, self._negro, (self._bloque_largo * 2, 0), (self._bloque_largo * 2, self._width), stroke) ## 2da linea ##
		## Lineas Horizontales ##	
		pygame.draw.line(self._ventana, self._negro, (0, self._bloque_ancho), (self._height, self._bloque_ancho), stroke) ## 3ra linea
		pygame.draw.line(self._ventana, self._negro, (0, self._bloque_ancho * 2), (self._height, self._bloque_ancho * 2), stroke) ## 4ta linea
	
	def dibujar_jugadores(self):
		###########################
		##### Dibujar X o O #######
		###########################
		for fila in range(3):
			for columna in range(3):
				if self._matriz[fila][columna] != 0:
					#x = 0
					#y = 0				
					###########################
					if fila == 0:
						y = 0
						y_fin = self._bloque_largo - 1
					elif fila == 1:
						y = self._bloque_largo
						y_fin = self._bloque_largo * 2 - 1
					elif fila == 2:
						y = self._bloque_largo * 2
						y_fin = self._width
					###########################
					if columna == 0:
						x = 0
						x_fin = self._bloque_ancho - 1
					elif columna == 1:
						x = self._bloque_ancho
						x_fin = self._bloque_ancho * 2 - 1
					elif columna == 2:
						x = self._bloque_ancho * 2
						x_fin = self._height
					###########################
					imagen = ''

					if self._matriz[fila][columna] == 2:
						imagen = pygame.image.load('firefox_mod.png')
					else:
						imagen = pygame.image.load('google_mod.png')

					x = ((x + x_fin) - imagen.get_height()) / 2
					y = ((y + y_fin) - imagen.get_width()) / 2

					self._ventana.blit(imagen, (x, y))

	def movimiento_CPU(self):
		neurona = self._cerebro.analizar_mov(self._matriz)
		if not neurona == False:			
			self._matriz[neurona._coordenada._x][neurona._coordenada._y] = 1
			self._cerebro.add_neurona(neurona)
			if(self.check_move(1, self._matriz)):
				print "Perdiste"
				self._matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]	
			self._turno_humano = True
		else:
			self._matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]			
			self._turno_humano = True
			print "empate"

	def check_move(self, num, mat):

		diagonal1 = [[0, 2], [1, 1], [2, 0]]
		diagonal2 = [[0, 0], [1, 1], [2, 2]]

		horiz1    = [[0, 0], [0, 1], [0, 2]] 
		horiz2 	  = [[1, 0], [1, 1], [1, 2]]
		horiz3 	  = [[2, 0], [2, 1], [2, 2]]

		verti1    = [[0, 0], [1, 0], [2, 0]]
		verti2 	  = [[0, 1], [1, 1], [2, 1]]
		verti3 	  = [[0, 2], [1, 2], [2, 2]]

		if mat[diagonal1[0][0]][diagonal1[0][1]] == num and mat[diagonal1[1][0]][diagonal1[1][1]] == num and mat[diagonal1[2][0]][diagonal1[2][1]] == num:
			return True
		elif mat[diagonal2[0][0]][diagonal2[0][1]] == num and mat[diagonal2[1][0]][diagonal2[1][1]] == num and mat[diagonal2[2][0]][diagonal2[2][1]] == num:
			return True
		elif mat[horiz1[0][0]][horiz1[0][1]] == num and mat[horiz1[1][0]][horiz1[1][1]] == num and mat[horiz1[2][0]][horiz1[2][1]] == num:
			return True
		elif mat[horiz2[0][0]][horiz2[0][1]] == num and mat[horiz2[1][0]][horiz2[1][1]] == num and mat[horiz2[2][0]][horiz2[2][1]] == num:
			return True
		elif mat[horiz3[0][0]][horiz3[0][1]] == num and mat[horiz3[1][0]][horiz3[1][1]] == num and mat[horiz3[2][0]][horiz3[2][1]] == num:
			return True
		elif mat[verti1[0][0]][verti1[0][1]] == num and mat[verti1[1][0]][verti1[1][1]] == num and mat[verti1[2][0]][verti1[2][1]] == num:
			return True
		elif mat[verti2[0][0]][verti2[0][1]] == num and mat[verti2[1][0]][verti2[1][1]] == num and mat[verti2[2][0]][verti2[2][1]] == num:
			return True
		elif mat[verti3[0][0]][verti3[0][1]] == num and mat[verti3[1][0]][verti3[1][1]] == num and mat[verti3[2][0]][verti3[2][1]] == num:
			return True
		else:
			return False

	def check_event(self):
		############################################################
		############################################################
		#############             EVENTOS           ################
		############################################################
		############################################################
		for event in pygame.event.get():
			if event.type == QUIT: ## Evento de salida ##
				pygame.quit() ## Cerrar librerias ##
				sys.exit()	  ## Cerrar aplicacion 	
			elif event.type == MOUSEBUTTONUP: ## Presion de un boton del mouse ##
				if event.button in (1, 3) and self._turno_humano == True: ## Presion del boton izquierdo o derecho del mouse ##
					mouse_x, mouse_y = event.pos ## Coordenadas del mouse ##					
					## Coordennadas en X ##
					if mouse_y in range(0, self._bloque_largo):
						vector_x = 0
					elif mouse_y in range(self._bloque_largo, self._bloque_largo * 2):
						vector_x = 1
					elif mouse_y in range(self._bloque_largo * 2, self._width + 1):
						vector_x = 2
					## Coordenadas en Y ##
					if mouse_x in range(0, self._bloque_ancho):
						vector_y = 0
					elif mouse_x in range(self._bloque_ancho, self._bloque_ancho * 2):
						vector_y = 1
					elif mouse_x in range(self._bloque_ancho * 2, self._height + 1):
						vector_y = 2
					if  self._matriz[vector_x][vector_y] == 0:
						self._cerebro.add_neurona(Neurona(str(vector_x)+":"+str(vector_y), '', {}, self._turno_humano, Coordenada(vector_x, vector_y)))
						self._matriz[vector_x][vector_y] = 2 ## se crea el movimiento
						if(self.check_move(2, self._matriz)):
							self._matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]			
							self._turno_humano = True
							print "Ganaste";
						else:
							self._turno_humano = False
						#print matriz ## Depuracion
						#print self._cerebro._neurona_actual ## Depuracion

			elif event.type == KEYDOWN: ## Envento de tecla presionada ##
				if event.key == K_ESCAPE: ## Tecla ESC presionada ##
					pygame.event.post(pygame.event.Event(QUIT)) ## Salir ##

	def play(self):
		while(True):
			self.dibujar_tablero()
			self.dibujar_jugadores()
			if(not self._turno_humano):
				self.movimiento_CPU()
			self.check_event()
			##### Actualizacion del panel ######
			pygame.display.update() ## Actualiza la ventana ##
			self._fps.tick(30) ## Espera, para que corra a 30 fps ##
cerebro = Cerebro()
mi_gato = Gato(cerebro) # se crea el gato
mi_gato.play() # se inicializa el gato

	