import math, copy, random
from cmu_112_graphics import *
import musicalbeeps
import time
#needed to play sounds
player = musicalbeeps.Player(volume = 0.3, mute_output = False)

def splashScreenMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, text='PIANO GAME!', font=font)
    canvas.create_text(app.width/2, 200, text='YAZSSSS!', font=font)
    canvas.create_text(app.width/2, 250, text='Press any key for the game!', font=font)

def splashScreenMode_keyPressed(app, event):
    app.mode = 'gameMode'


def appStarted(app):
	#initalizes everything
	app.mode = 'splashScreenMode'
	app.label = 'Piano! :P'
	app.song = ' '
	app.keys = []
	app.flatsandsharps = []
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
	app.notes = ([('G3', 0.3), ("E4", 0.3),("D4", 0.3),
		  ("C4", 0.3),("D4", 0.3), ("C4", 0.3),
		  ("A3", 0.3), ("G3", 0.4),("E3", 0.9),
		  ('G3', 0.3), ("E4", 0.3),("D4", 0.3),
		  ("C4", 0.3),('C4',0.3),('B3', 0.3),
		  ("C4", 0.3), ("D4", 0.8)])
	app.bubbles = []
	app.bubblesy = 0
	app.bubblesy1 = app.height/10
	for item in app.notes:
		note = item[0]
		index = letters.index(note)
		x0, y0, x1, y1 = app.keys[index]
		info = note, x0, app.bubblesy, x1, app.bubblesy1
		app.bubbles.append(info)
	app.timePassed = 0
	app.num = 0
	app.score = 0
	app.gameOver = False

def gameMode_keyPressed(app, event):
	if event.key == 'k':
		for x in range(len(app.notes)):
			player.play_note(app.notes[x][0], app.notes[x][1])
	
def gameMode_mousePressed(app, event):
	#gets x and y coordinate from key click
	x = event.x
	y = event.y
	flag = False
	letters = ['C3','D3','E3','F3','G3','A3','B3','C4','D4','E4','F4','G4','A4','B4','C5','D5']
	for sharp in app.flatsandsharps:
		x00 = sharp[0]
		y00 = sharp[1]
		x10 = sharp[2]
		y10 = sharp[3]
		if x > x00 and x < x10 and y > y00 and y < y10:
			flatsandsharps = ['C3#','E3b','F3#','G3#','A3#','C4#','D4#','F4#','G4#','A4#','C5#','D5#']
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
	letters = ['C3','D3','E3','F3','G3','A3','B3','C4','D4','E4','F4','G4','A4','B4','C5','D5']
	for x in range(16):
		(x0, y0, x1, y1) = getKeyBounds(app, x)
	width = x1-x0
	for x in range(16):
		(x0, y0, x1, y1) = getKeyBounds(app, x)
		if x!= 2 and x!=6 and x!= 9 and x!= 13:
			canvas.create_rectangle(x0 + (3*(width)/4),app.height //1.5, x1+(width//3), 3*app.height/3.5, fill = 'black')
		canvas.create_text((x0+x1)//2,app.height*0.96,text= f'{letters[x]}', font = 'Arial 15 bold', fill = 'black')

#draws the bubble in the place of the note to be played
def drawFallingBubble(app, canvas):
	# (x0, y0, x1, y1) = getKeyBounds(app, 4)
	if app.bubblesy < app.height or app.bubblesy1 < app.height:
		note, x0, y0, x1, y1 = app.bubbles[app.num]
		canvas.create_oval(x0,app.bubblesy,x1,app.bubblesy1, fill = 'green')

# working on this
# target: to make the bubble fall down the screen in the correct order
def moveFallingBubble(app, drow):
	if app.bubblesy < app.height or app.bubblesy1 < app.height:																
		app.bubblesy += drow
		app.bubblesy1 += drow


def gameMode_timerFired(app):
	moveFallingBubble(app, +25)
	if (app.num < len(app.bubbles)-1) and (app.bubblesy > app.height or app.bubblesy1 > app.height):
		app.num += 1
		app.bubblesy = 0
		app.bubblesy1 = app.height/10
	if app.num == len(app.bubbles)-1:
		app.gameOver = True
	
# working on this- check if the bubble is still in the dimensions of the screen
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
	canvas.create_text(app.width/2, app.height/4, text = f"SCORE = {app.score}")
	if app.gameOver == True:
		canvas.create_text(app.width/2, app.height/8,text=f'Final Score = {app.score}', font = 'Arial 30 bold', fill = 'black')

#run app
def playPiano():
	runApp(width=600, height=(600))

def main():
	playPiano()

if __name__ == '__main__':
	main()

