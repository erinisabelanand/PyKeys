import math, copy, random, time
from cmu_112_graphics import *
#module for piano keys
import musicalbeeps
#needed to play sounds
import pygame
from pygame import mixer
player = musicalbeeps.Player(volume = 0.3, mute_output = False)

##### SPLASH SCREEN ######

# sound syntax from: https://www.py4u.net/discuss/246333 ##
mixer.init()
song = pygame.mixer.Sound('No-Copyright-Music-_-It_s-Easy-_-3-Second-Intro_Outro-Music..ogg')
song.play()
song.set_volume(0.1)

#draw home screen
def ScreenMode_redrawAll(app, canvas):
	#draw home screen button
	canvas.create_rectangle(app.width/100,app.height/26, app.width/4, app.height/55, fill = 'blue')
	(canvas.create_text(app.width/8, app.height/35,
	text = "Press 'i' for instructions", font = 'Times 10 bold', fill = 'white'))
	#game mode text
	(canvas.create_text(app.width/2,app.height/3.34,font=
	'Times 20 bold', text= "Press 'a' for the game mode", fill = 'blue'))
	#freestyle mode text
	(canvas.create_text(app.width/2,app.height/3,font=
	'Times 20 bold', text= "Press 'f' for the freestyle mode", fill = 'blue'))
	#composition mode text
	(canvas.create_text(app.width/2,app.height/3.7,font=
	'Times 20 bold', text= "Press 'c' for the composition mode", fill = 'blue'))
	(canvas.create_text(app.width/2, app.height/6, text='PyKeys', 
	font='Times 80 bold', fill = 'black'))
	#load logo
	(canvas.create_image(app.width/2, app.height*2.5/4,
	 image=ImageTk.PhotoImage(app.image2)))
	
def ScreenMode_keyPressed(app, event):
	#transition to modes
	if event.key == 'a':
		app.mode = 'intermediate'
	if event.key == 'A':
		app.mode = 'intermediate'
	if event.key == 'f':
		app.mode = 'freeStyle'
	if event.key == 'F':
		app.mode = 'freeStyle'
	if event.key == 'c':
		app.mode = 'composition'
	if event.key == 'C':
		app.mode = 'composition'
	if event.key == 'i':
		app.mode = 'instruction'
	if event.key == 'I':
		app.mode = 'instruction'


###### APP STARTED #######

def appStarted(app):
	#initalizes everything
	app.t = time.time()
	#initialize modes
	app.mode = 'playPiano'
	app.mode = 'practice'
	app.mode = 'mistakeAnalysis'
	app.mode = 'composition'
	app.mode = 'instruction'
	app.mode = 'intermediate'
	app.mode = 'gameMode'
	app.mode = 'difficulty'
	app.mode = 'ScreenMode'
	app.label = 'Piano! :P'
	app.song = ' '
	app.text = ""
	app.keys = []
	app.flatsandsharps = []
	app.image1 = app.loadImage('Snake Logo.jpg')
	app.image3 = app.loadImage('help.png')
	app.image4 = app.scaleImage(app.image3, 1/2.79)
	#saves x0,y0,x1,y1 values
	for x in range(16):
		(x0, y0, x1, y1) = getKeyBounds(app, x)
	    #creates the rectangles
		width = x1-x0
		details =(x0, y0, x1, y1)
		app.keys.append(details)
		if x!= 2 and x!=6 and x!= 9 and x!= 13:
			x0 = x0 + (3*(width)/4)
			y0 = app.height //1.5
			x1 = x1+(width//3)
			y1=  3*app.height/3.5
			details = (x0,y0,x1,y1)
			app.flatsandsharps.append(details)
	#list of letters
	#list of flatsandsharps
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4','C5','D5'])
	flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
			'D4#','F4#','G4#','A4#','C5#','D5#'])
	app.timePassed = 0
	app.selected = "My Bonnie Lies over the Ocean.txt"
	app.num = 0
	app.score = 0
	app.gameOver = False
	app.image1 = app.loadImage('Snake Logo.jpg')
	app.image2 = app.scaleImage(app.image1, 1/3)
	app.notePlayed = ""
	app.songs = []
	#create list of songs
	songlist = open('songs.txt',"r")
	songs = (songlist.read())
	app.songs = songs.splitlines()
	app.songscoordinates = []
	app.compositionnotes = []
	app.compositionname = 'NAME IT'
	for num in range(len(app.songs)):
		x0, y0 = app.width/4, app.height/3+(num*70)
		x1, y1 = app.width*3/4, app.height/2.5+(num*70)
		info = (x0,y0,x1,y1)
		app.songscoordinates.append(info)
	app.mistakesstart = 0
	app.mistakesmiddle = 0
	app.mistakesend = 0
	app.counter = 0
	app.bubbles2 = []
	app.notes2 = []
	app.slowness = +30
	app.seconds = 0
	app.highscore = 0

######### INSTRUCTION #############

def instruction_redrawAll(app,canvas):
	#draw home screen button
	canvas.create_rectangle(app.width/100,app.height/26, app.width/8, app.height/55, fill = 'blue')
	(canvas.create_text(app.width/15, app.height/35, 
	text = "Home Screen", font = 'Times 10 bold', fill = 'white'))
	(canvas.create_image(app.width/2, app.height/2,
	 image=ImageTk.PhotoImage(app.image4)))

def instruction_mousePressed(app,event):
	x = event.x
	y = event.y
	if x > app.width/100 and x < app.width/8 and y< app.height/26 and y > app.height/55:
		app.mode = 'ScreenMode'

######### INTERMEDIATE ############

def intermediate_keyPressed(app,event):
	pass
		
def intermediate_mousePressed(app, event):
	x = event.x
	y = event.y
	#if home screen button pressed
	if x > app.width/100 and x < app.width/8 and y< app.height/26 and y > app.height/55:
		app.mode = 'ScreenMode'
	#select songs
	for coordinate in app.songscoordinates:
		x0, y0, x1, y1 = coordinate
		if x>x0 and x<x1 and y>y0 and y<y1:
			index = app.songscoordinates.index(coordinate)
			song = app.songs[index]
			app.selected = f"{song}.txt"
			#transition to  mode to choose difficulty
			app.mode = 'difficulty'
			#set variables for highscore for song
			highestscore(app)
	selection = open(app.selected,"r")
	notes = (selection.read())
	notes = notes.splitlines()
	app.notes = []
	app.notes2 = []
	for tuple in notes:
		currnoteanddur = tuple.split(",")
		currnote = currnoteanddur[0]
		currdur = float(currnoteanddur[1])
		if len(currnoteanddur) > 2:
			chordnote = currnoteanddur[2]
			chorddur = float(currnoteanddur[3])
			chortnoteanddur = (chordnote,chorddur)
			app.notes2.append(chortnoteanddur)
		newcurrnoteanddur = (currnote, currdur)
		app.notes.append(newcurrnoteanddur)

	#my bonnie notes (hardcoded)
	# app.notes = ([('G3', 0.3), ("E4", 0.3),("D4", 0.3),
	# 	  ("C4", 0.3),("D4", 0.3), ("C4", 0.3),
	# 	  ("A3", 0.3), ("G3", 0.4),("E3", 0.9),
	# 	  ('G3', 0.3), ("E4", 0.3),("D4", 0.3),
	# 	  ("C4", 0.3),('C4',0.3),('B3', 0.3),
	# 	  ("C4", 0.3), ("D4", 0.8)])

	app.bubbles = []
	app.bubbles2 = []
	flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
						'D4#','F4#','G4#','A4#','C5#','D5#'])
	letters = (['C3','D3','E3','F3','G3','A3','B3',
			'C4','D4','E4','F4','G4','A4','B4','C5','D5'])
	app.bubblesy = 0
	app.bubblesy1 = app.height/10
	for item in app.notes:
		note = item[0]
		duration = item[1]
		#index into notes
		try:
			index = letters.index(note)
			x0, y0, x1, y1 = app.keys[index]
			info = note, x0, app.bubblesy, x1, app.bubblesy1
		except:
			index = flatsandsharps.index(note)
			x0, y0, x1, y1 = app.flatsandsharps[index]
			info = note, x0, app.bubblesy, x1, app.bubblesy1
			# app.bubbles2.append(info)
		app.bubbles.append(info)
	app.bubblesy0 = 0
	app.bubblesy10 = app.height/10
	#chords
	if app.notes2 != []:
		for item in app.notes2:
			note = item[0]
			duration = float(item[1])
			if note == 'xx':
				info = note, x0, app.bubblesy0, x1, app.bubblesy10
			else:
				try:
					index = letters.index(note)
					x0, y0, x1, y1 = app.keys[index]
					info = note, x0, app.bubblesy0, x1, app.bubblesy10
				except:
					index = flatsandsharps.index(note)
					x0, y0, x1, y1 = app.flatsandsharps[index]
					info = note, x0, app.bubblesy0, x1, app.bubblesy10
				
			app.bubbles2.append(info)

def intermediate_redrawAll(app, canvas):
	#draw home screen button
	canvas.create_rectangle(app.width/100,app.height/26, app.width/8, app.height/55, fill = 'yellow')
	(canvas.create_text(app.width/15, app.height/35, 
	text = "Home Screen", font = 'Times 10 bold', fill = 'blue'))
	(canvas.create_text(app.width/2, app.height/5, 
	text = "Pick a song:", font = 'Times 50 bold', fill = 'blue'))
	#draw each soong
	for num in range(len(app.songs)):
		x0, y0 = app.width/4, app.height/3+(num*70)
		x1, y1 = app.width*3/4, app.height/2.5+(num*70)
		(canvas.create_rectangle(x0, y0, x1, y1, fill = 'black'))
		(canvas.create_text(app.width/2, (y0+y1)/2, text = 
		app.songs[num], font = 'Times 20 bold', fill = 'white'))
	# (canvas.create_text(app.width/6, app.height/35, 
	# text = "Press 'r' to go back to the home screen!", font = 'Times 10 bold', fill = 'blue'))
	
def findHighestScore(app):
	#open file
	f = open("scores.txt", 'r')
	newscores = []
	#loops through file
	for line in f:
		if repr(line) == repr("\n"):
			continue
		songsandscore = line.split(',')
		song, score = songsandscore[0], int(songsandscore[1])
		selection = app.selected
		selection = selection[:len(selection)-4]
		#check if new score is greater
		if str(song) == selection and app.score > score:
			newline = song, int(app.score)
			newscores.append(newline)
		else:
			songsandscore = line.split(',')
			song, score = songsandscore[0], int(songsandscore[1])
			newline = song, score
			newscores.append(newline)
	os.remove("scores.txt")
	#creates new scores file and stores everything
	f = open("scores.txt", 'a')
	for element in newscores:
		if element == "":
			continue
		f.write(f'{element[0]}, {element[1]}\n')

########## SELECT DIFFICULTY #############

def difficulty_redrawAll(app, canvas):
	#select difficulty text
	(canvas.create_text(app.width/2, app.height/5, text='Select Difficulty', 
	font='Times 60 bold', fill = 'purple'))
	(canvas.create_rectangle(app.width/4, app.height/3+50, app.width*3/4, app.height/2.5+(50), fill = 'black'))
	(canvas.create_rectangle(app.width/4, app.height/3+(2*50), app.width*3/4, app.height/2.5+(2*50), fill = 'black'))
	(canvas.create_rectangle(app.width/4, app.height/3+(3*50), app.width*3/4, app.height/2.5+(3*50), fill = 'black'))
	(canvas.create_text(app.width/2, ((app.height/3+50)+(app.height/2.5+(50)))/2, text = 
		'Easy', font = 'Times 20 bold', fill = 'white'))
	(canvas.create_text(app.width/2, ((app.height/3+(2*50))+(app.height/2.5+(2*50)))/2, text = 
		'Moderate', font = 'Times 20 bold', fill = 'white'))
	(canvas.create_text(app.width/2, ((app.height/3+(3*50))+(app.height/2.5+(3*50)))/2, text = 
		'Difficult', font = 'Times 20 bold', fill = 'white'))

def difficulty_mousePressed(app, event):
	x = event.x
	y = event.y
	if x > app.width/4 and y > app.height/3+50 and x < app.width*3/4 and y < app.height/2.5+(50):
		app.difficulty = 'easy'
		app.mode = 'gameMode'
	elif (x > app.width/4 and y > app.height/3+(2*50) and x < app.width*3/4 and y < app.height/2.5+(2*50)):
		app.difficulty = 'moderate'
		app.mode = 'gameMode'
	elif (x > app.width/4 and y > app.height/3+(3*50) and x < app.width*3/4 and y < app.height/2.5+(3*50)):
		app.difficulty = 'difficult'
		app.mode = 'gameMode'

########## GAME MODE ###########

def gameMode_keyPressed(app, event):
	#control with keys (don't need anymore)
	# if event.key == 'k':
	# 	for x in range(len(app.notes)):
	# 		player.play_note(app.notes[x][0], app.notes[x][1])
	# flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
	# 				'D4#','F4#','G4#','A4#','C5#','D5#'])
	# letters = (['C3','D3','E3','F3','G3','A3','B3',
	# 			'C4','D4','E4','F4','G4','A4','B4',
	# 			'C5','D5'])
	# keys = (['q','w','e','r','t','y','u','i','o','p','x','c','v','b','n','m'])
	# raised = (['2','3','5','6','7','9','0','d','f','g','j','k'])
	# keypressed = event.key
	# if keypressed in keys:
	# 	index = keys.index(keypressed)
	# 	player.play_note(letters[index], 0.36)
	# 	app.notePlayed = letters[index]
	# if keypressed in raised:
	# 	index = raised.index(keypressed)
	# 	player.play_note(flatsandsharps[index], 0.36)
	# 	app.notePlayed = flatsandsharps[index]
	pass

def gameMode_mousePressed(app, event):
	#gets x and y coordinate from key click
	x = event.x
	y = event.y
	app.t = time.time()
	if x > app.width/100 and x < app.width/8 and y< app.height/26 and y > app.height/55:
		appStarted(app)
		app.mode = 'ScreenMode'
	if x > app.width/100 and y > app.height/24 and x < app.width/2.65 and y < app.height/16:
		for x in range(len(app.notes)):
			player.play_note(app.notes[x][0], app.notes[x][1])

#make each key have duration
def gameMode_mouseReleased(app,event):
	x = event.x
	y = event.y
	seconds = time.time()-app.t
	if seconds < 0.36: 
		seconds = 0.36
	flag = False
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4',
				'C5','D5'])
	for sharp in app.flatsandsharps:
		x00 = sharp[0]
		y00 = sharp[1]
		x10 = sharp[2]
		y10 = sharp[3]
		if x > x00 and x < x10 and y > y00 and y < y10:
			flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
							   'D4#','F4#','G4#','A4#','C5#','D5#'])
			index = app.flatsandsharps.index(sharp)
			player.play_note(flatsandsharps[index], seconds)
			app.seconds = seconds
			flag = True
			break

	for key in app.keys:
		x0 = key[0]
		y0 = key[1]
		x1 = key[2]
		y1 = key[3]
		for sharp in app.flatsandsharps:
			x00 = sharp[0]
			y00 = sharp[1]
			x10 = sharp[2]
			y10 = sharp[3]
			if flag != True:
				if (x > x0 and x < x1 and y > y0 and y < y1):
					index = app.keys.index(key)
					player.play_note(letters[index], seconds)
					app.seconds = seconds
					break

	if KeyClickedatRightTime(app, x,y):
		note, x0, y0, x1, y1 = app.bubbles[app.num]
		item =  app.notes[app.num]
		duration = item[1]
		if abs(duration-app.seconds) <= 0.3:
			app.score += 1
		else:
			app.score += 0.5
	else:
		total = len(app.bubbles)
		division1 = total//3
		division2 = division1*2
		if app.counter < division1:
			app.mistakesstart += 1
		elif app.counter > division1 and app.counter < division2:
			app.mistakesmiddle +=1
		elif app.counter > division2:
			app.mistakesend +=1

	if app.gameOver == True and x< app.width/1.25 and y> app.height/3.25 and x> app.width/5 and y< app.height/2.75:
		app.mode = 'mistakeAnalysis'
	
#gets x0, y0, x1, y1 values
def getKeyBounds(app, col):
	#gets the values depending on the column number
	x0 = col*(app.width//16)
	x1 = x0 + (app.width//16)
	y0 = app.height //1.5
	y1 =  app.height
	return (x0, y0, x1, y1)

#draws keys
def drawKey(app,canvas):
	for x in range(16):
		(x0, y0, x1, y1) = getKeyBounds(app, x)
		canvas.create_rectangle(x0 ,y0, x1, y1,fill = 'white')

#draws flats and sharps
def drawFlatsandSharps(app,canvas):
	letters = (['C3','D3','E3','F3','G3','A3','B3','C4'
	           ,'D4','E4','F4','G4','A4','B4','C5','D5'])
	for x in range(16):
		(x0, y0, x1, y1) = getKeyBounds(app, x)
	width = x1-x0
	for x in range(16):
		(x0, y0, x1, y1) = getKeyBounds(app, x)
		if x!= 2 and x!=6 and x!= 9 and x!= 13:
			canvas.create_rectangle(x0 + (3*(width)/4),app.height //1.5, 
			x1+(width//3), 3*app.height/3.5, fill = 'black')
		(canvas.create_text((x0+x1)//2,app.height*0.96,
		text= f'{letters[x]}', font = 'Arial 15 bold', fill = 'black'))

#draws the bubble in the place of the note to be played
def drawFallingBubble(app, canvas):
	# (x0, y0, x1, y1) = getKeyBounds(app, 4)
	if app.bubblesy < app.height or app.bubblesy1 < app.height:
		letters = (['C3','D3','E3','F3','G3','A3','B3','C4'
	           ,'D4','E4','F4','G4','A4','B4','C5','D5'])
		flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
							   'D4#','F4#','G4#','A4#','C5#','D5#'])
		note, x0, y0, x1, y1 = app.bubbles[app.num]
		if note in letters: 
		# note, x00, y00, x10, y10 = app.bubbles2[app.num]
			canvas.create_oval(x0,app.bubblesy,x1,app.bubblesy1, fill = 'purple')
		else:
			canvas.create_oval(x0,app.bubblesy,x1,app.bubblesy1, fill = 'blue')
		if app.notes2 != []:
			note, x00, y00, x11, y11 = app.bubbles2[app.num]
			if note == 'xx':
				pass
			else:
				canvas.create_oval(x00,app.bubblesy0,x11,app.bubblesy10, fill = 'cyan')

# target: to make the bubble fall down the screen in the correct order
def moveFallingBubble(app, drow):
	if app.bubblesy < app.height or app.bubblesy1 < app.height:																
		app.bubblesy += drow
		app.bubblesy1 += drow
		app.bubblesy0 += drow
		app.bubblesy10 += drow

#default slowness for modes
def difficultslowness(app):
	if app.bubblesy1-app.bubblesy <= float(90):
		slowness = +35
	elif app.bubblesy1-app.bubblesy <= float(100):
		slowness = +20
	elif app.bubblesy1-app.bubblesy <= float(110):
		slowness = +15
	elif app.bubblesy1-app.bubblesy <= float(120):
		slowness = +10
	elif app.bubblesy1-app.bubblesy <= float(130):
		slowness = +8
	elif app.bubblesy1-app.bubblesy <= float(140):
		slowness = +3
	else: 
		slowness = +1
	return slowness

def moderateslowness(app):
	if app.bubblesy1-app.bubblesy <= float(90):
		slowness = +30
	elif app.bubblesy1-app.bubblesy <= float(100):
		slowness = +15
	elif app.bubblesy1-app.bubblesy <= float(110):
		slowness = +10
	elif app.bubblesy1-app.bubblesy <= float(120):
		slowness = +5
	elif app.bubblesy1-app.bubblesy <= float(130):
		slowness = +3
	elif app.bubblesy1-app.bubblesy <= float(140):
		slowness = +2
	else: 
		slowness = +1
	return slowness

def easyslowness(app):
	if app.bubblesy1-app.bubblesy <= float(90):
		slowness = +25
	elif app.bubblesy1-app.bubblesy <= float(100):
		slowness = +13
	elif app.bubblesy1-app.bubblesy <= float(110):
		slowness = +12
	elif app.bubblesy1-app.bubblesy <= float(120):
		slowness = +4
	elif app.bubblesy1-app.bubblesy <= float(130):
		slowness = +3
	elif app.bubblesy1-app.bubblesy <= float(140):
		slowness = +2
	else: 
		slowness = +1
	return slowness

def gameMode_timerFired(app):
	thex, they ,thex1, they1 = getKeyBounds(app, 0)
	if app.bubblesy > they: 
		if app.difficulty == 'easy':
			app.slowness = easyslowness(app)
		elif app.difficulty == 'moderate':
			app.slowness = moderateslowness(app)
		elif app.difficulty == 'difficult':
			app.slowness = difficultslowness(app)

	moveFallingBubble(app, app.slowness)
	if app.difficulty == 'easy':
		app.slowness = +25
	elif app.difficulty == 'moderate':
		app.slowness = +35
	elif app.difficulty == 'difficult':
		app.slowness = +40

	if ((app.num < len(app.bubbles)-1) and (app.bubblesy > app.height
				or app.bubblesy1 > app.height)):
		app.num += 1
		app.bubblesy = 0
		app.bubblesy1 = (app.height/10)+((app.notes[app.num][1])*100)
		thex, they ,thex1, they1 = getKeyBounds(app, 0)
		app.bubblesy0 = 0
		app.bubblesy10 = app.height/10
		app.counter += 1
	if app.num == len(app.bubbles)-1:
		findHighestScore(app)
		app.gameOver = True

#decide where to increment score
def KeyClickedatRightTime(app, x, y):
	thex, they ,thex1, they1 = getKeyBounds(app, 0)
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4',
				'C5','D5'])
	flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
							   'D4#','F4#','G4#','A4#','C5#','D5#'])
	note, x0, y0, x1, y1 = app.bubbles[app.num]
	if (app.bubblesy>=they or app.bubblesy1 >= they) and y>=they and y <=they1:
		try:
			index = letters.index(note)
			x00, y00, x10, y10 = app.keys[index]
		except:
			index = flatsandsharps.index(note)
			x00, y00, x10, y10 = app.flatsandsharps[index]
		if (x>x00 and x<x10):
			return True
	else:
		return False

#draws the skeleton of the piano
def drawPiano(app, canvas):
	drawKey(app, canvas)
	drawFlatsandSharps(app,canvas)

#set app.highscore
def highestscore(app):
	f = open("scores.txt", 'r')
	for line in f:
		if repr(line) == repr('\n'):
			continue
		song, score = line.split(',')
		if f"{song}.txt" == app.selected:
			app.highscore = int(score)
	
def gameMode_redrawAll(app, canvas):
	#draw the listen to song button
	canvas.create_rectangle(app.width/100, app.height/24, app.width/2.65, app.height/16, fill = 'yellow')
	(canvas.create_text(app.width/5.23, app.height/19, 
	text = "Press to listen to how it's supposed to sound!", font = 'Times 10 bold', fill = 'blue'))
	#draw home screen button
	canvas.create_rectangle(app.width/100,app.height/26, app.width/8, app.height/55, fill = 'yellow')
	(canvas.create_text(app.width/15, app.height/35, 
	text = "Home Screen", font = 'Times 10 bold', fill = 'blue'))
	drawPiano(app, canvas)
	#draws all the bubbles (presently)
	drawFallingBubble(app,canvas)
	(canvas.create_text(app.width/12, app.height/13, 
	text = f"Highest Score = {app.highscore}", font = 'Times 10 bold', fill = 'blue'))
	if app.gameOver == True:
		(canvas.create_text(app.width/2, app.height/4,text=
		f'Final Score = {app.score}', font = 'Times 50 bold', fill = 'blue'))
		canvas.create_rectangle(app.width/1.25, app.height/3.25, app.width/5, app.height/2.75, fill = 'black')
		(canvas.create_text(app.width/2, app.height/3, 
			font = 'Times 20 bold', text = "Press here to improve your score!", fill = 'white'))
	else:
		(canvas.create_text(app.width/2, app.height/4, 
	font = 'Times 20 bold', text = f"SCORE = {app.score}"))

###### FREESTYLE #######

def freeStyle_mousePressed(app, event):
	#gets x and y coordinate from key click
	x = event.x
	y = event.y
	app.t = time.time()

def freeStyle_redrawAll(app, canvas):

	drawPiano(app, canvas)
	#draw home screen button
	canvas.create_rectangle(app.width/100,app.height/26, app.width/8, app.height/55, fill = 'yellow')
	(canvas.create_text(app.width/15, app.height/35, 
	text = "Home Screen", font = 'Times 10 bold', fill = 'blue'))
	(canvas.create_text(app.width/2, app.height/3, 
	text= f"You just pressed: {app.notePlayed}",font = 'Times 50 bold', fill = 'blue'))
	# (canvas.create_text(app.width/6, app.height/35, 
	# text = "Press 'r' to go back to the home screen!", font = 'Times 10 bold', fill = 'blue'))

#duration of keys with mouse press
def freeStyle_mouseReleased(app, event):
	seconds = time.time()-app.t
	if seconds < 0.36: 
		seconds = 0.36
	x = event.x
	y = event.y
	if x > app.width/100 and x < app.width/8 and y< app.height/26 and y > app.height/55:
		appStarted(app)
		app.mode = 'ScreenMode'
	flag = False
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4',
				'C5','D5'])
	for sharp in app.flatsandsharps:
		x00 = sharp[0]
		y00 = sharp[1]
		x10 = sharp[2]
		y10 = sharp[3]
		if x > x00 and x < x10 and y > y00 and y < y10:
			flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
							   'D4#','F4#','G4#','A4#','C5#','D5#'])
			index = app.flatsandsharps.index(sharp)
			player.play_note(flatsandsharps[index], seconds)
			app.notePlayed = flatsandsharps[index]
			app.t = 0
			flag = True
			break

	for key in app.keys:
		x0 = key[0]
		y0 = key[1]
		x1 = key[2]
		y1 = key[3]
		for sharp in app.flatsandsharps:
			x00 = sharp[0]
			y00 = sharp[1]
			x10 = sharp[2]
			y10 = sharp[3]
			if flag != True:
				if (x > x0 and x < x1 and y > y0 and y < y1):
					index = app.keys.index(key)
					player.play_note(letters[index], seconds)
					app.t = 0
					app.notePlayed = letters[index]
					break

###control piano with keys###
###not doing this because keyreleased does not work###
'''def freeStyle_keyPressed(app,event):
	app.t = time.time()
	if event.key == 'r':
		app.mode = 'ScreenMode'
	flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
					'D4#','F4#','G4#','A4#','C5#','D5#'])
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4',
				'C5','D5'])
	keys = (['q','w','e','r','t','y','u','i','o','p','x','c','v','b','n','m'])
	raised = (['2','3','5','6','7','9','0','d','f','g','j','k'])
	keypressed = event.key
	if keypressed in keys:
		index = keys.index(keypressed)
		player.play_note(letters[index], 0.36)
		app.notePlayed = letters[index]
	if keypressed in raised:
		index = raised.index(keypressed)
		player.play_note(flatsandsharps[index], 0.36)
		app.notePlayed = flatsandsharps[index]'''
	
'''def freeStyle_keyReleased(app,event):
	seconds = time.time()-app.t
	if seconds < 0.40: 
		seconds = 0.40
	flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
					'D4#','F4#','G4#','A4#','C5#','D5#'])
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4',
				'C5','D5'])
	keys = (['q','w','e','r','t','y','u','i','o','p','x','c','v','b','n','m'])
	raised = (['2','3','5','6','7','9','0','d','f','g','j','k'])
	keypressed = event.key
	if keypressed in keys:
		index = keys.index(keypressed)
		player.play_note(letters[index], seconds)
		app.notePlayed = letters[index]
	if keypressed in raised:
		index = raised.index(keypressed)
		player.play_note(flatsandsharps[index], seconds)
		app.notePlayed = flatsandsharps[index]'''

##### COMPOSITION #####

def composition_mousePressed(app, event):
	#gets x and y coordinate from key click
	x = event.x
	y = event.y
	flag = False
	app.t = time.time()
	#home screen press
	if x > app.width/100 and x < app.width/8 and y< app.height/26 and y > app.height/55:
		appStarted(app)
		app.mode = 'ScreenMode'
	#file name press
	if x > app.width/100 and x < app.width/7 and y> app.height/24 and y < app.height/16:
		app.compositionname = getUserInput(app, "Name your composition: ")
	#listen to composition
	if x> app.width/100 and x < app.width/4.25 and y > app.height/15 and y < app.height/11.25:
		playComposition(app)
	if x>app.width/100 and x < app.width/4.8 and y > app.height/11 and y < app.height/9:
		if app.compositionnotes != []:
			convertComptoFile(app)
			app.text = "File Saved!"

def composition_mouseReleased(app,event):
	x = event.x
	y = event.y
	seconds = time.time() - app.t
	seconds = round(seconds,2)
	if seconds < 0.36: 
		seconds = 0.36
	flag = False
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4',
				'C5','D5'])
	for sharp in app.flatsandsharps:
		x00 = sharp[0]
		y00 = sharp[1]
		x10 = sharp[2]
		y10 = sharp[3]
		if x > x00 and x < x10 and y > y00 and y < y10:
			flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
							   'D4#','F4#','G4#','A4#','C5#','D5#'])
			index = app.flatsandsharps.index(sharp)
			player.play_note(flatsandsharps[index], seconds)
			app.compositionnotes.append((flatsandsharps[index],seconds))
			flag = True
			app.t = 0
			break

	for key in app.keys:
		x0 = key[0]
		y0 = key[1]
		x1 = key[2]
		y1 = key[3]
		for sharp in app.flatsandsharps:
			x00 = sharp[0]
			y00 = sharp[1]
			x10 = sharp[2]
			y10 = sharp[3]
			if flag != True:
				if (x > x0 and x < x1 and y > y0 and y < y1):
					index = app.keys.index(key)
					player.play_note(letters[index], seconds)
					app.notePlayed = letters[index]
					app.compositionnotes.append((letters[index],seconds))
					app.t = 0
					break

def composition_keyPressed(app, event):
	#control piano with keys
	#not using because does not work with keyReleased
	'''
	flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
					'D4#','F4#','G4#','A4#','C5#','D5#'])
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4',
				'C5','D5'])
	keys = (['q','w','e','r','t','y','u','i','o','p','x','c','v','b','n','m'])
	raised = (['2','3','5','6','7','9','0','d','f','g','j','k'])
	keypressed = event.key
	if keypressed in keys:
		index = keys.index(keypressed)
		player.play_note(letters[index], 0.36)
		app.compositionnotes.append(letters[index])
	if keypressed in raised:
		index = raised.index(keypressed)
		player.play_note(flatsandsharps[index], 0.36)
		app.compositionnotes.append(flatsandsharps[index])'''
	pass

#create file
def convertComptoFile(app):
	f = open(f"{app.compositionname}.txt", "a")
	notes = []
	for item in app.compositionnotes:
		new = (item[0], item[1])
		notes.append(new)
	for element in notes:
		note, dur = element 
		f.write(f'{note}, {dur}\n')
	s = open("songs.txt", "a")
	s.write(f"\n{app.compositionname}")
	s = open("scores.txt", "a")
	s.write(f"\n{app.compositionname}, 0")

#loop through app.compositionnnotes and play note
def playComposition(app):
	for x in range(len(app.compositionnotes)):
			player.play_note(app.compositionnotes[x][0],app.compositionnotes[x][1])

def getUserInput(app, prompt):
	return simpledialog.askstring('Input Name', prompt)

def composition_redrawAll(app, canvas):
	drawPiano(app, canvas)
	#draw home screen button
	canvas.create_rectangle(app.width/100,app.height/26, app.width/8, app.height/55, fill = 'yellow')
	(canvas.create_text(app.width/15, app.height/35, 
	text = "Home Screen", font = 'Times 10 bold', fill = 'blue'))
	#name your file button
	canvas.create_rectangle(app.width/100, app.height/24, app.width/7, app.height/16, fill = 'yellow')
	(canvas.create_text(app.width/13, app.height/19, 
	text = "Name your file!", font = 'Times 10 bold', fill = 'blue'))
	#listen to composition
	canvas.create_rectangle(app.width/100, app.height/15, app.width/4.25, app.height/11.25, fill = 'yellow')
	(canvas.create_text(app.width/8, app.height/12.75, 
	text = "Listen to your composition!", font = 'Times 10 bold', fill = 'blue'))
	#s to save composition
	canvas.create_rectangle(app.width/100, app.height/11, app.width/4.8, app.height/9, fill = 'yellow')
	(canvas.create_text(app.width/9.25, app.height/9.9, 
	text = "Save your composition!", font = 'Times 10 bold', fill = 'blue'))
	canvas.create_text(app.width/2,app.height/2, text=f"{app.compositionnotes}")
	(canvas.create_text(app.width/2, app.height/6,text=
		f'{app.compositionname}', font = 'Times 50 bold', fill = 'red'))
	canvas.create_text(app.width/16.5, app.height/8, text = f"{app.text}", font = 'Times 10 bold', fill = 'purple')

######## MISTAKE ANALYSIS ###########

def mistakeAnalysis_keyPressed(app, event):
	pass	

def mistakes(app):
	#find where most mistakes were made
	maxmistakes = max(app.mistakesstart, app.mistakesmiddle, app.mistakesend)
	if app.mistakesstart == maxmistakes:
		analyze = 'start'
	elif app.mistakesmiddle == maxmistakes:
		analyze = 'middle'
	else:
		analyze = 'end'
	return analyze

def mistakeAnalysis_mousePressed(app, event):
	x = event.x
	y = event.y
	#go back home
	if x > app.width/100 and x < app.width/8 and y< app.height/26 and y > app.height/55:
		appStarted(app)
		app.mode = 'ScreenMode'
	if len(app.bubbles)<10:
		if x > app.width/3 and y > app.height/2.1 and x < app.width/1.5 and y < app.height/1.9:
			refresh(app)
			highestscore(app)
			app.mode = 'gameMode'
		elif x>app.width/3 and y > app.height/1.82 and x< app.width/1.5 and y < app.height/1.66:
			appStarted(app)
			app.mode = 'intermediate'
	else:
		if x > app.width/3 and y > app.height/1.82 and x< app.width/1.5 and y < app.height/1.66:
			appStarted(app)
			app.mode = 'intermediate'
		elif x > app.width/3 and y> app.height/2.1 and x < app.width/1.5 and y < app.height/1.9:
			lookat = whichSection(app)
			app.notes = app.notes[lookat[0]:lookat[1]]
			app.bubbles = []
			flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
								'D4#','F4#','G4#','A4#','C5#','D5#'])
			letters = (['C3','D3','E3','F3','G3','A3','B3',
					'C4','D4','E4','F4','G4','A4','B4','C5','D5'])
			app.bubblesy = 0
			app.bubblesy1 = app.height/10
			for item in app.notes:
				note = item[0]
				try:
					index = letters.index(note)
					x0, y0, x1, y1 = app.keys[index]
					info = note, x0, app.bubblesy, x1, app.bubblesy1
				except:
					index = flatsandsharps.index(note)
					x0, y0, x1, y1 = app.flatsandsharps[index]
					info = note, x0, app.bubblesy, x1, app.bubblesy1
				app.bubbles.append(info)
			app.num = 0
			app.score = 0
			app.gameOver = False
			app.mode = 'practice'


def mistakeAnalysis_redrawAll(app, canvas):
	(canvas.create_text(app.width/2, app.height/8, 
	font = 'Times 30 bold', fill = 'red', text = "Mistake Analysis"))
	#draw home screen button
	canvas.create_rectangle(app.width/100,app.height/26, app.width/8, app.height/55, fill = 'yellow')
	(canvas.create_text(app.width/15, app.height/35, 
	text = "Home Screen", font = 'Times 10 bold', fill = 'blue'))
	(canvas.create_text(app.width/2, app.height/6,
	text = f"Here's how many mistakes you made: {round(len(app.bubbles) - app.score)} ", font = 'Times 15 bold', fill = 'blue'))
	if len(app.bubbles) < 10:
		canvas.create_rectangle(app.width/3, app.height/2.1, app.width/1.5, app.height/1.9,fill = 'pink')
		(canvas.create_text(app.width/2, app.height/3,
	text = "Suggestion: Practice the entire song!", font = 'Times 28 bold', fill = 'purple'))
		(canvas.create_text(app.width/2, app.height/2,
		text = "Practice", font = 'Times 28 bold', fill = 'purple'))
		canvas.create_rectangle(app.width/3, app.height/1.82, app.width/1.5, app.height/1.66,fill = 'pink')
		(canvas.create_text(app.width/2, app.height/1.75,
	text = "Try a new song", font = 'Times 28 bold', fill = 'purple'))
	else:
		analyze = mistakes(app)
		if analyze == 'start':
			(canvas.create_text(app.width/2, app.height/3.5,
	text = "You made the most mistakes at the start of the piece!", font = 'Times 20 bold', fill = 'purple'))
			canvas.create_text(app.width/2, app.height/3, text = f' {app.mistakesstart} in particular!',font = 'Times 20 bold', fill = 'purple')
		elif analyze == 'middle':
			(canvas.create_text(app.width/2, app.height/3.5,
	text = "You made the most mistakes at the middle of the piece! ", font = 'Times 20 bold', fill = 'purple'))
			canvas.create_text(app.width/2, app.height/3, text = f' {app.mistakesmiddle} in particular!',font = 'Times 20 bold', fill = 'purple')
		else:
			(canvas.create_text(app.width/2, app.height/3.5,
	text = "You made the most mistakes at the end of the piece!", font = 'Times 20 bold', fill = 'purple'))
			canvas.create_text(app.width/2, app.height/3, text = f' {app.mistakesend} in particular!',font = 'Times 20 bold', fill = 'purple')

		canvas.create_rectangle(app.width/3, app.height/2.1, app.width/1.5, app.height/1.9,fill = 'pink')
		(canvas.create_text(app.width/2, app.height/2,
		text = "Practice", font = 'Times 28 bold', fill = 'purple'))
		(canvas.create_text(app.width/2, app.height/2.5,
		text = "Suggestion: Practice that section!", font = 'Times 28 bold', fill = 'purple'))
		canvas.create_rectangle(app.width/3, app.height/1.82, app.width/1.5, app.height/1.66,fill = 'pink')
		(canvas.create_text(app.width/2, app.height/1.75,
	text = "Try a new song", font = 'Times 28 bold', fill = 'purple'))

###### PRACTICE ########
#refresh key variables
def refresh(app):
	app.bubbles = []
	flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
						'D4#','F4#','G4#','A4#','C5#','D5#'])
	letters = (['C3','D3','E3','F3','G3','A3','B3',
			'C4','D4','E4','F4','G4','A4','B4','C5','D5'])
	app.bubblesy = 0
	app.bubblesy1 = app.height/10
	for item in app.notes:
		note = item[0]
		try:
			index = letters.index(note)
			x0, y0, x1, y1 = app.keys[index]
			info = note, x0, app.bubblesy, x1, app.bubblesy1
		except:
			index = flatsandsharps.index(note)
			x0, y0, x1, y1 = app.flatsandsharps[index]
			info = note, x0, app.bubblesy, x1, app.bubblesy1
		app.bubbles.append(info)
	app.num = 0
	app.score = 0
	app.gameOver = False
	app.mode = 'practice'

def practice_keyPressed(app, event):
	pass
	
#figure out which section of song has most mistakes
def whichSection(app):
	analyzed = mistakes(app)
	total = len(app.bubbles)
	division1 = total//3
	division2 = division1*2
	if analyzed == 'start':
		lookat = (0, division1)
	elif analyzed == 'middle':
		lookat = (division1, division2)
	else:
		lookat = (division2, len(app.bubbles))
	return lookat

def practice_mousePressed(app, event):
	x = event.x
	y = event.y
	app.t = time.time()
	if x > app.width/100 and x < app.width/8 and y< app.height/26 and y > app.height/55:
		appStarted(app)
		app.mode = 'ScreenMode'
	if x > app.width/100 and y > app.height/24 and x < app.width/2.65 and y < app.height/16:
		for x in range(len(app.notes)):
			player.play_note(app.notes[x][0], app.notes[x][1])
	if app.gameOver == True:
		if x < app.width/1.25 and y > app.height/3.25 and x > app.width/5 and y < app.height/2.75:
			appStarted(app)
			refresh(app)
			app.mode = 'practice'
	
def practice_mouseReleased(app,event):
	x = event.x
	y = event.y
	seconds = time.time()-app.t
	if seconds < 0.36: 
		seconds = 0.36
	flag = False
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4',
				'C5','D5'])
	for sharp in app.flatsandsharps:
		x00 = sharp[0]
		y00 = sharp[1]
		x10 = sharp[2]
		y10 = sharp[3]
		if x > x00 and x < x10 and y > y00 and y < y10:
			flatsandsharps = (['C3#','E3b','F3#','G3#','A3#','C4#',
							   'D4#','F4#','G4#','A4#','C5#','D5#'])
			index = app.flatsandsharps.index(sharp)
			player.play_note(flatsandsharps[index], seconds)
			flag = True
			break

	for key in app.keys:
		x0 = key[0]
		y0 = key[1]
		x1 = key[2]
		y1 = key[3]
		for sharp in app.flatsandsharps:
			x00 = sharp[0]
			y00 = sharp[1]
			x10 = sharp[2]
			y10 = sharp[3]
			if flag != True:
				if (x > x0 and x < x1 and y > y0 and y < y1):
					index = app.keys.index(key)
					player.play_note(letters[index], seconds)
					break

	if KeyClickedatRightTime(app, x,y):
		note, x0, y0, x1, y1 = app.bubbles[app.num]
		item =  app.notes[app.num]
		duration = item[1]
		if abs(duration-app.seconds) <= 0.3:
			app.score += 1
		else:
			app.score += 0.5

def practice_timerFired(app):
	thex, they ,thex1, they1 = getKeyBounds(app, 0)
	if app.bubblesy > they: 
		if app.difficulty == 'easy':
			app.slowness = easyslowness(app)
		elif app.difficulty == 'moderate':
			app.slowness = moderateslowness(app)
		elif app.difficulty == 'difficult':
			app.slowness = difficultslowness(app)

	moveFallingBubble(app, app.slowness)
	if app.difficulty == 'easy':
		app.slowness = +25
	elif app.difficulty == 'moderate':
		app.slowness = +35
	elif app.difficulty == 'difficult':
		app.slowness = +40
	
	if ((app.num < len(app.bubbles)-1) and (app.bubblesy > app.height
				or app.bubblesy1 > app.height)):
		app.num += 1
		app.bubblesy = 0
		app.bubblesy1 = (app.height/10)+((app.notes[app.num][1])*100)
		app.counter += 1	
	if app.num == len(app.bubbles)-1:
		app.gameOver = True

def practice_redrawAll(app, canvas):
	canvas.create_rectangle(app.width/100, app.height/24, app.width/2.65, app.height/16, fill = 'yellow')
	(canvas.create_text(app.width/5.23, app.height/19, 
	text = "Press to listen to how it's supposed to sound!", font = 'Times 10 bold', fill = 'blue'))
	#draw home screen button
	canvas.create_rectangle(app.width/100,app.height/26, app.width/8, app.height/55, fill = 'yellow')
	(canvas.create_text(app.width/15, app.height/35, 
	text = "Home Screen", font = 'Times 10 bold', fill = 'blue'))
	drawPiano(app, canvas)
	#draws all the bubbles (presently)
	drawFallingBubble(app,canvas)
	if app.gameOver == True:
		(canvas.create_text(app.width/2, app.height/4,text=
		f'Final Score = {app.score}', font = 'Times 50 bold', fill = 'blue'))
		canvas.create_rectangle(app.width/1.25, app.height/3.25, app.width/5, app.height/2.75, fill = 'black')
		(canvas.create_text(app.width/2, app.height/3, 
			font = 'Times 20 bold', text = "Practice until you have 0 mistakes!", fill = 'white'))
	else:
		(canvas.create_text(app.width/2, app.height/4, 
	font = 'Times 20 bold', text = f"SCORE = {app.score}"))

#run app
def playPiano():
	runApp(width=600, height=(600))

def main():
	playPiano()

if __name__ == '__main__':
	main()

#ENJOY