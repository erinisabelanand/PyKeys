import math, copy, random
from cmu_112_graphics import *
import musicalbeeps
#needed to play sounds
player = musicalbeeps.Player(volume = 0.3, mute_output = False)


##### SPLASH SCREEN ######
def ScreenMode_redrawAll(app, canvas):
	(canvas.create_text(app.width/2,app.height/3.34,font=
	'Times 20 bold', text= "Press 'a' for the game mode", fill = 'blue'))
	(canvas.create_text(app.width/2,app.height/3,font=
	'Times 20 bold', text= "Press 'f' for the freestyle mode", fill = 'blue'))
	(canvas.create_text(app.width/2,app.height/3.7,font=
	'Times 20 bold', text= "Press 'c' for the composition mode", fill = 'blue'))
	(canvas.create_text(app.width/2, app.height/6, text='PyKeys', 
	font='Times 80 bold', fill = 'black'))
	(canvas.create_image(app.width/2, app.height*2.5/4,
	 image=ImageTk.PhotoImage(app.image2)))
	
def ScreenMode_keyPressed(app, event):
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

###### APP STARTED #######

def appStarted(app):
	#initalizes everything
	app.mode = 'composition'
	app.mode = 'intermediate'
	app.mode = 'gameMode'
	app.mode = 'ScreenMode'
	app.label = 'Piano! :P'
	app.song = ' '
	app.keys = []
	app.flatsandsharps = []
	app.image1 = app.loadImage('Snake Logo.jpg')
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
	letters = (['C3','D3','E3','F3','G3','A3','B3',
				'C4','D4','E4','F4','G4','A4','B4','C5','D5'])
	app.timePassed = 0
	app.num = 0
	app.score = 0
	app.gameOver = False
	app.image1 = app.loadImage('Snake Logo.jpg')
	app.image2 = app.scaleImage(app.image1, 1/3)
	app.notePlayed = ""
	app.songs = []
	songlist = open('songs.txt',"r")
	songs = (songlist.read())
	app.songs = songs.splitlines()
	app.songscoordinates = []
	for num in range(len(app.songs)):
		x0, y0 = app.width/4, app.height/3+(num*70)
		x1, y1 = app.width*3/4, app.height/2.5+(num*70)
		info = (x0,y0,x1,y1)
		app.songscoordinates.append(info)

######### INTERMEDIATE ############

def intermediate_keyPressed(app,event):
	pass

def intermediate_mousePressed(app, event):
	x = event.x
	y = event.y
	for coordinate in app.songscoordinates:
		x0, y0, x1, y1 = coordinate
		if x>x0 and x<x1 and y>y0 and y<y1:
			index = app.songscoordinates.index(coordinate)
			song = app.songs[index]
			app.selected = f"{song}.txt"
			app.mode = 'gameMode'
	selection = open(app.selected,"r")
	notes = (selection.read())
	notes = notes.splitlines()
	app.notes = []
	for tuple in notes:
		currnoteanddur = tuple.split(",")
		currnote = currnoteanddur[0]
		currdur = float(currnoteanddur[1])
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

def intermediate_redrawAll(app, canvas):
	(canvas.create_text(app.width/2, app.height/5, 
	text = "Pick a song:", font = 'Times 50 bold', fill = 'blue'))
	for num in range(len(app.songs)):
		x0, y0 = app.width/4, app.height/3+(num*70)
		x1, y1 = app.width*3/4, app.height/2.5+(num*70)
		(canvas.create_rectangle(x0, y0, x1, y1, fill = 'black'))
		(canvas.create_text(app.width/2, (y0+y1)/2, text = 
		app.songs[num], font = 'Times 20 bold', fill = 'white'))
	pass

########## GAME MODE ###########
def gameMode_keyPressed(app, event):
	if event.key == 'k':
		for x in range(len(app.notes)):
			player.play_note(app.notes[x][0], app.notes[x][1])
	
def gameMode_mousePressed(app, event):
	#gets x and y coordinate from key click
	x = event.x
	y = event.y
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
			player.play_note(flatsandsharps[index], 0.4)
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
					player.play_note(letters[index], 0.36)
					break

	if KeyClickedatRightTime(app, x,y):
		app.score += 1

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
		note, x0, y0, x1, y1 = app.bubbles[app.num]
		canvas.create_oval(x0,app.bubblesy,x1,app.bubblesy1, fill = 'green')

# target: to make the bubble fall down the screen in the correct order
def moveFallingBubble(app, drow):
	if app.bubblesy < app.height or app.bubblesy1 < app.height:																
		app.bubblesy += drow
		app.bubblesy1 += drow

def gameMode_timerFired(app):
	moveFallingBubble(app, +25)
	if ((app.num < len(app.bubbles)-1) and (app.bubblesy > app.height
				or app.bubblesy1 > app.height)):
		app.num += 1
		app.bubblesy = 0
		app.bubblesy1 = app.height/10
	if app.num == len(app.bubbles)-1:
		app.gameOver = True
		
# check if the bubble is still in the dimensions of the screen
# if not, remove from app.bubbles
def BubbleonScreen(app):
	for item in app.bubbles:
		note, x0, y0, x1, y1 = item
		if y0 >= app.height or y1 >= app.height:
			app.bubbles.remove(item)

def KeyClickedatRightTime(app, x, y):
	thex, they ,thex1, they1 = getKeyBounds(app, 0)
	for num in range(len(app.bubbles)):
		note, x0, y0, x1, y1 = app.bubbles[num]
		if app.bubblesy>they and app.bubblesy1 < they1 and y>they and y < they1:
			return True
		else:
			return False

#draws the skeleton of the piano
def drawPiano(app, canvas):
	drawKey(app, canvas)
	drawFlatsandSharps(app,canvas)

def gameMode_redrawAll(app, canvas):
	drawPiano(app, canvas)
	#draws all the bubbles (presently)
	drawFallingBubble(app,canvas)
	(canvas.create_text(app.width/2, app.height/4, 
	font = 'Times 20 bold', text = f"SCORE = {app.score}"))
	if app.gameOver == True:
		(canvas.create_text(app.width/2, app.height/8,text=
		f'Final Score = {app.score}', font = 'Times 50 bold', fill = 'blue'))
		(canvas.create_text(app.width/2, app.height/5.5,text=
		"Press 'k' to hear what it is supposed to sound like!", font = 'Times 20 bold', fill = 'red'))

###### FREESTYLE #######
def freeStyle_mousePressed(app, event):
	#gets x and y coordinate from key click
	x = event.x
	y = event.y
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
			player.play_note(flatsandsharps[index], 0.4)
			app.notePlayed = flatsandsharps[index]
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
					player.play_note(letters[index], 0.36)
					app.notePlayed = letters[index]
					break

def freeStyle_redrawAll(app, canvas):
	drawPiano(app, canvas)
	canvas.create_text(app.width/2, app.height/3, text= f"You just pressed: {app.notePlayed}",font = 'Times 50 bold', fill = 'blue')

##### COMPOSITION #####
def composition_mousePressed(app, event):
	pass

def composition_keyPressed(app, event):
	pass

def composition_redrawAll(app, event):
	pass

#run app
def playPiano():
	runApp(width=600, height=(600))

def main():
	playPiano()

if __name__ == '__main__':
	main()

