import keyboard  # using module keyboard
import sys
import win32api, win32con #mouse
import time
from PIL import ImageGrab,Image
import pygetwindow
from termcolor import cprint
from desktopmagic.screengrab_win32 import getRectAsImage
import cv2
import numpy as np


def kill():
    if keyboard.is_pressed('esc') == True:
        sys.exit()
        
def displayTime(time):
    mins = 0
    while time > 59:
        mins = mins + 1
        time = time - 60
    string = ""
    if mins > 0:
        string = (str(mins) + " minutes and " + str(time) + " seconds")
    else:
        string = (str(time) + " seconds")
    return string        

def initWindow():
    all = pygetwindow.getWindowsWithTitle("ApowerMirror")
    if len(all) != 0:
        #androidWindow.resizeTo(400, 400)
        for i in range(len(all)):
            if all[i].title == "ApowerMirror":
                all[i].moveTo(1930, 50)
        return True
    return False

def click(x,y,RorL='L'):
    kill()
    win32api.SetCursorPos((x,y))
    if RorL == 'L':
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    elif RorL == 'R':
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)


def compareImage(xoffset, yoffset, w, h, imageName):
    imgFromFile = cv2.imread(imageName)
    imTemp = getRectAsImage((gameX + xoffset, gameY + yoffset, gameX + xoffset + w, gameY + yoffset + h))
    b, g, r = imTemp.split()
    imTemp = Image.merge("RGB", (r, g, b))
    imgToCheck = np.array(imTemp)
    
#    if gameState == "predict":
#        cv2.imshow(imageName,imgToCheck)
#        cv2.resizeWindow(imageName, 400,100)
    
    difference = cv2.subtract(imgFromFile, imgToCheck)

    b, g, r = cv2.split(difference)
    bad = 0
    for value in np.ndenumerate(difference):
        if value[1] > 20:
            bad = bad + 1
    return bad




lastState = ""
gameCycles = 0

def predictGameState(desiredCourse):
    global lastState
    global gameCycles
    kill()
    bad_Menu = compareImage(menuInfo[0], menuInfo[1], menuInfo[2], menuInfo[3], menuInfo[4])
    bad_Battle = compareImage(battleInfo[0], battleInfo[1], battleInfo[2], battleInfo[3], battleInfo[4])
    bad_Xp = compareImage(xpInfo[0], xpInfo[1], xpInfo[2], xpInfo[3], xpInfo[4])
    bad_Ok = compareImage(okInfo[0], okInfo[1], okInfo[2], okInfo[3], okInfo[4])
    
    bad_Menu = bad_Menu / (menuInfo[2]*menuInfo[3]*3) * 100
    bad_Battle = bad_Battle / (battleInfo[2]*battleInfo[3]*3) * 100
    bad_Xp = bad_Xp / (xpInfo[2]*xpInfo[3]*3) * 100
    bad_Ok = bad_Ok / (okInfo[2]*okInfo[3]*3) * 100
    
    listOfBad = [bad_Menu, bad_Battle, bad_Xp, bad_Ok]
    for i in range(len(listOfBad)):
        if listOfBad[i] == 0:
            listOfBad[i] = 100.0
    #print(listOfBad)
    
    timeToSleep = 15
    small = listOfBad.index(min(listOfBad))
    if listOfBad[small] < 20:
        if small == 0:
            print("I think its the level select")
            click(desiredCourse[0], desiredCourse[1])
            timeToSleep = 3
            lastState = "menu"
        elif small == 1:
            print("I think its a battle")
            lastState = "battle"
        elif small == 2:
            print("I think its the XP screen")
            click(bottomContinueButton[0], bottomContinueButton[1])
            timeToSleep = 3
            lastState = "xp"
        elif small == 3:
            print("I think its an OK button screen")
            click(bottomContinueButton[0], bottomContinueButton[1])
            timeToSleep = 6
            if lastState == "menu":
                gameCycles = gameCycles + 1
                cprint("Round: " + str(gameCycles), "green")
                lastState = "ok"
    else:
        print("I cannot predict")
        timeToSleep = 6
    
    return timeToSleep
    


#===================================================================#vars
courseTop = (2138, 350)
courseMid = (2143, 470)
courseBot = (2138, 590)
## Go - continuing on XP screen - ok(coin screen)
bottomContinueButton = (2137, 919)

#  [xOffset, yOffset, widthOfImage, heightOfImage, filenameToCompare]
menuInfo = [4, 43, 33, 32, "training.png"]
battleInfo = [274, 51, 32, 15, "speedup.png"]
xpInfo = [17, 130, 23, 19, "xp.png"]
okInfo = [122, 801, 144, 17, "ok.png"]

gameState = "predict"
#===================================================================#vars



gameX = 1950
gameY = 122




setup = initWindow()
if not setup:
    cprint("---Error. Window not found---", "red")
time.sleep(1)        


while gameState == "predict":
    kill()
    
    """
    lag = 6000
    while True:
        lag = lag -1
        if lag == 0:
            print(win32api.GetCursorPos())
            lag = 6000
    """   

#    im = getRectAsImage((gameX, gameY, 2339, 949))
#    im.save("shot.png")

#=========================================================================================================
    if gameState == "predict":
        timeToSleep = predictGameState(courseTop)

#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        time.sleep(timeToSleep)







