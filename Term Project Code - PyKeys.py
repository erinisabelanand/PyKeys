import math, copy, random
from cmu_112_graphics import *
import musicalbeeps
#needed to play sounds
player = musicalbeeps.Player(volume = 0.3, mute_output = False)

def appStarted(app):
    #initalizes everything
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
          ("A3", 0.3), ("G3", 0.3),("E3", 0.3),
          ('G3', 0.3), ("E4", 0.3),("D4", 0.3),
          ("C4", 0.3),('C4',0.3),('B3', 0.3),
          ("C4", 0.3), ("D4", 0.3)])
    app.bubbles = []
    for item in app.notes:
        note = item[0]
        index = letters.index(note)
        x0, y0, x1, y1 = app.keys[index]
        info = note, x0, y0, x1, y1
        app.bubbles.append(info)
    # moveFallingBubble(app)

def keyPressed(app, event):
    pass

def mousePressed(app, event):
    #gets x and y coordinate from key click
    x = event.x
    y = event.y
    letters = ['C3','D3','E3','F3','G3','A3','B3','C4','D4','E4','F4','G4','A4','B4','C5','D5']
    for key in app.keys:
        x0 = key[0]
        y0 = key[1]
        x1 = key[2]
        y1 = key[3]
        #if its within the range of the keys, plays appropriate note
        if x > x0 and x < x1 and y > y0 and y < y1:
            index = app.keys.index(key)
            player.play_note(letters[index], 0.36)

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
    for item in (app.bubbles):
        # (x0, y0, x1, y1) = getKeyBounds(app, x)  
        note, x0, y0, x1, y1 = item
        canvas.create_oval(x0,0,x1,app.height/10, fill = 'purple')

#working on this
#target: to make the bubble fall down the screen in the correct order
def moveFallingBubble(app):
    for item in app.bubbles:
        if item[2] < app.height or item[4] < app.height:
            index = app.bubbles.index(item)
            note, x0, y0, x1, y1 = item
            app.bubbles.remove(item)
            y0 += 10
            y1 += 10
            info = (note, x0, y0, x1, y1)
            app.bubbles.insert(index, info)
    pass

#working on this- check if the bubble is still in the dimensions of the screen
#if not, remove from app.bubbles
def isBubbleonScreen(app):
    for item in app.bubbles:
        note, x0, y0, x1, y1 = item
        if y0 >= app.height or y1 >= app.height:
            app.bubbles.remove(item)
    
##############

#getting some of the logic from tetris code
'''def placeFallingPiece(app):
    #sets start row and start col
    startRow, startCol = app.fallingPieceRow, app.fallingPieceCol
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            #checks if the piece element True , and if so, sets the color
            #on the board
            if (app.fallingPiece[row][col] == True):
                app.board[startRow+row][startCol+col] = app.fallingPieceColor
    #while game is not over, adds new piece
    if not app.gameOver:
        newFallingPiece(app)
    #removes the full rows
    removeFullRows(app)
            
def moveFallingPiece(app, drow, dcol):
    #moves it in direction of drow and dcol
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    app.pieceMoved = True
    #if move is not legal, undoes the change
    if not fallingPieceisLegal(app):
        app.pieceMoved = False
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol 

def fallingPieceisLegal(app):
    #loops through falling piece
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            #checks if the fallingPiece is true
            if app.fallingPiece[row][col]:
                #if so, makes changes
                newPieceRow = app.fallingPieceRow + row
                newPieceCol = app.fallingPieceCol + col
                #checks if it is within bounds
                if ((newPieceRow < 0 ) or (newPieceRow >= app.rows) or
                    (newPieceCol) < 0 or (newPieceCol >= app.cols)):
                    return False
                #sets the cell value from board
                boardCell = app.board[newPieceRow][newPieceCol]
                #checks if the cell is empty to draw on 
                if boardCell != app.emptyColor:
                    return False
    return True'''

#############

#draws the skeleton of the piano
def drawPiano(app, canvas):
    drawKey(app, canvas)
    drawFlatsandSharps(app,canvas)
        
def redrawAll(app, canvas):
    drawPiano(app, canvas)
    #draws all the bubbles (presently)
    drawFallingBubble(app,canvas)

#run app
def playPiano():
    runApp(width=600, height=(600))

def main():
    playPiano()

if __name__ == '__main__':
    main()




''' OPEN CV SECTION
code adapted from web
https://towardsdatascience.com/mathematics-of-music-in-python-b7d838c84f72

from webcam import Webcam
from detection import Detection
import sound
import simpleaudio as sa
import numpy as np
import cv2
from threading import Thread



class Detection(object):
 
    THRESHOLD = 1500
 
    def __init__(self, image):
        self.previous_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    def get_active_cell(self, image):
        # obtain motion between previous and current image
        current_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        delta = cv2.absdiff(self.previous_gray, current_gray)
        threshold_image = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
 
        # debug
        cv2.imshow('OpenCV Detection', image)
        cv2.waitKey(10)
 
        # store current image
        self.previous_gray = current_gray
 
        # set cell width
        height, width = threshold_image.shape[:2]
        cell_width = width//7
 
        # store motion level for each cell
        cells = np.array([0, 0, 0, 0, 0, 0, 0])
        cells[0] = cv2.countNonZero(threshold_image[0:height, 0:cell_width])
        cells[1] = cv2.countNonZero(threshold_image[0:height, cell_width:cell_width*2])
        cells[2] = cv2.countNonZero(threshold_image[0:height, cell_width*2:cell_width*3])
        cells[3] = cv2.countNonZero(threshold_image[0:height, cell_width*3:cell_width*4])
        cells[4] = cv2.countNonZero(threshold_image[0:height, cell_width*4:cell_width*5])
        cells[5] = cv2.countNonZero(threshold_image[0:height, cell_width*5:cell_width*6])
        cells[6] = cv2.countNonZero(threshold_image[0:height, cell_width*6:width])
 
        # obtain the most active cell
        top_cell =  np.argmax(cells)
 
        # return the most active cell, if threshold met
        if(cells[top_cell] >= self.THRESHOLD):
            return top_cell
        else:
            return None
class Webcam:
   
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]
           
    # create thread for capturing images
    def start(self):
        Thread(target=self._update_frame, args=()).start()
   
    def _update_frame(self):
        while(True):
            self.current_frame = self.video_capture.read()[1]
                   
    # get the current frame
    def get_current_frame(self):
        return self.current_frame

def sound(x,z):
    frequency = x # Our played note will be 440 Hz
    fs = 44100  # 44100 samples per second
    seconds = z  # Note duration of 3 seconds

    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * fs, False)

    # Generate a 440 Hz sine wave
    note = np.sin(frequency * t * 2 * np.pi)

    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()

# musical notes (C, D, E, F, G, A, B)
NOTES = [494,441,393,350,330,294,262] #[262, 294, 330, 350, 393, 441, 494]
 
# initialise webcam and start thread
webcam = Webcam()
webcam.start()
 
# initialise detection with first webcam frame
image = webcam.get_current_frame()
detection = Detection(image) 
 
# initialise switch
switch = True

while True:
 
    # get current frame from webcam
    image = webcam.get_current_frame()
     
    # use motion detection to get active cell
    cell = detection.get_active_cell(image)
    if cell == None: continue
 
    # if switch on, play note
    if switch:
        sound(NOTES[cell], 1)
     
    # alternate switch    
    switch = not switch
    
    
'''