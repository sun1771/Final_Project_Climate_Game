# Climate Impact Game

# team members: Sanaz Khanali, Menna Hendawy

# 12/08/2023 - 12/13/2023

# Climate Impact Game Controls
# after pressing key 's' countdown would start
# after the countdown the player should:
# press the keys '1', '2', '3', '4' to move the people to the upper elevation (Safe zone)
# press 'Space' simultaniously to reduce the CO2 emission to buy some time to move the people above safe zone
# Win: if the player could move all the people successfully to upland 
# lose: if people drown
# in both cases by pressing's' the game would restart

# the things that went well:
# we were able to achieve all the objectives we defined in the proposal. the only thing we wanted to include extra was a button instead of kepressed for reducing the CO2 emission (slowing down the rain and sea level rise)
# And we included that in the TODO for future steps

# challenges faced:
# challenge 1 (defining sea level rise):
# initially, we initialized the sea level to rise by millis
# then realized that it starts to increase the sea level right after we hit run (starting the program)
# but we wanted the sea level to rise once the game state is in the race state
# therefore we defined a 'gameStart' variable and set it to millis after changing the game state to state race at the end of state countdown
# And calculated the sea level rise in the update method of 'seaLevel' class by calculating the seconds passed since start (subtracting millis from 'gameStart')

# challenge 2 (reset the game):
# initially, once game went to game over or success state, although we changed the game state back to state init, the game wouldn't start correctly because the millis already passed and after the game directly goes to game over 
# Therefore, we defined a reset function to set everything to their initial values, and called that resetGame function in setup and in the success and gameover state after pressing key 's'

# challenge 3 (moving the people on the angle):
# initially, I started to calculate each player's initiall location as a PVector in the list of players. and then update their location in the player class. But then it was so hard to calculate X and Y position of each player one by one so,
# so I tried to create the formula for X and Y positions that works for all the players in the calculateAbsolutePos() method of player class (since all of them would move on the same line) and only give their X position in the list of players. and that way the class would automatically calculate and update their locations  

#TODO
#1 Design a button instead of keypressed for reducing CO2 emission
#2 improve the graphics


STATE_INIT = 0
STATE_COUNTDOWN = 1
STATE_RACE = 2
STATE_GAME_OVER = 3
STATE_SUCCESS = 4
gameState = STATE_INIT
countDownStartTime = 0

players = None
rainDropList = []
gravityValue = 10.00
landStartPosition = PVector(700, 465)

gameStart = None

seaLevel = None

def setup():
    global players, seaLevel
    size(1250, 640)
    background(112, 129, 135)
    textSize(32)
    resetGame()
    
def draw():
    background(112, 129, 135)
    for player in players:
        player.render()
    
    fill(226, 202, 118  )
    noStroke()
    triangle(400, 640, 650, 640, 650, 500)
    rect(650, 500, 650, 140)
    triangle(650, 500, 1250, 500, 1250, 300)

    if gameState == STATE_INIT:
        handleStateInit()
    elif gameState == STATE_COUNTDOWN:
        handleStateCountDown()
    elif gameState == STATE_RACE:
        handleStateRace()
    elif gameState == STATE_GAME_OVER:
        handleGameOver()
    elif gameState == STATE_SUCCESS:
        handleGameSuccess()
         
def handleStateInit():
    textAlign(CENTER)
    fill(0)
    textSize(64)
    text("Press SPACE to start", width/2, height/2)

def handleStateCountDown():
    global gameState, gameStart
    countDownInSeconds = 3 - ((millis() - countDownStartTime) / 1000)
    if (countDownInSeconds > 0):
        print("countdown is: ", countDownInSeconds)
    else:
        gameState = STATE_RACE
        gameStart = millis()

    textAlign(CENTER)
    fill(0)
    textSize(64)
    text(countDownInSeconds, width / 2, height/2)
    
def handleStateRace():
    global gravityValue, gameState
    seaLevel.update()
    seaLevel.render()  
    fill(0, 255, 0)
    rect(0, height/2 + 40, 1250, 5)
    textSize(32 )
    text("Safe Zone", 100, height/2) 
    textAlign(CENTER)  
    fill(0)
    text("Press Space to decrease CO2 emission", width/2, 100) 
    text("Press 1, 2, 3, 4 keys to move the people to safe zone!", width/2, 150)
    #spawn rain
    for i in range(5):
        tempPos = PVector(random(-width,2*width) ,0)
        newRainDrop = RainDrop(tempPos)
        rainDropList.append(newRainDrop)
        
    # update rain drops
    for drop in rainDropList:
        drop.update()
        drop.render()
        
    for player in players:
        if player.calculateAbsolutePos().y < (height/2):
            gameState = STATE_SUCCESS 
    
    # increase the speed of rain        
    if gravityValue <= 10.00:
        gravityValue += 0.05

def handleGameOver():
    textAlign(CENTER)
    fill(0)
    textSize(64)
    text("GAME OVER", width/2, height/2)
    fill(0)
    textSize(32)
    text("Press S to start", width/2, height/2 + 50)   
    
def handleGameSuccess():
    textAlign(CENTER)
    fill(0)
    textSize(64)
    text("YOU SAVED HUMANITY!", width/2, height/2)
    textSize(32)
    text("Press S to start", width/2, height/2 + 50)
    
def resetGame():
    global seaLevel, players
    seaLevel = SeaLevel()
    
    players = (Player(0, color(150, 50, 50), 1),
               Player(20, color(50, 50, 150), 2),
               Player(40, color(150, 150,50), 3),
               Player(60, color(50, 150, 50), 4))
                        
def keyPressed():
    global gameState, countDownStartTime, earlyStart, gravityValue
    if key == ' ':
        if gameState == STATE_INIT:
            gameState = STATE_COUNTDOWN
            countDownStartTime = millis()
            
    if gameState == STATE_RACE:
        if key == "1":
            players[0].update()
        elif key == "2":
            players[1].update()
        elif key == "3":
            players[2].update()
        elif key == "4":
            players[3].update()
        elif key == ' ':
            if gravityValue > 2.00:
                gravityValue -= 1.0

    if gameState == STATE_GAME_OVER or gameState == STATE_SUCCESS:
        if key == "s" or key == "S":
            resetGame()
            gameState = STATE_INIT 

class RainDrop(object):
    def __init__(self, tempPos):
        self.pos = tempPos
        self.posList = [tempPos]
        self.MAX_LIST_LENGTH = 4
        
    def update(self):
        self.pos.y += gravityValue
        self.selfDeletion()
        self.posList.append(PVector(self.pos.x, self.pos.y))
        if len(self.posList) > self.MAX_LIST_LENGTH:
            self.posList.pop(0)
    
    def render(self):
        stroke(103, 193, 202)
        for i in range(len(self.posList) - 1):
            line(self.posList[i].x, self.posList[i].y, self.posList[i+1].x, self.posList[i+1].y)
            
    def selfDeletion(self):
        if self.posList[0].y > height and self in rainDropList:
            rainDropList.remove(self)
            
class SeaLevel(object):
    def __init__(self):
        self.h = 0
    def update(self):
        secondsSinceStart = (millis() - gameStart) / 50
        self.h = secondsSinceStart + gravityValue
    def render(self):
        fill(103, 193, 202)
        rect(0, 640, 1250, -self.h)

class Player(object):
    def __init__(self, startX, tempColor, tempNum):
        self.x = startX
        self.col = tempColor
        self.num = tempNum
        
    def update(self):
        self.x += 10
    
    def render(self):
        global gameState
        absolutePos = self.calculateAbsolutePos() 
        rectMode(CENTER)
        fill(self.col)
        noStroke()
        rect(absolutePos.x, absolutePos.y, 70, 40, 30, 30, 0, 0)
        circle(absolutePos.x, absolutePos.y - 50, 45)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(32)
        text(str(self.num), absolutePos.x, absolutePos.y - 5)
        rectMode(CORNER)
        if self.calculateAbsolutePos().y > (height - seaLevel.h):
            gameState = STATE_GAME_OVER

    def calculateAbsolutePos(self):
        absoluteX = landStartPosition.x + self.x
        absoluteY = landStartPosition.y - (self.x / 3)
        return PVector(absoluteX, absoluteY)
