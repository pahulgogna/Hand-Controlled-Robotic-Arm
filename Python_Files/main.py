import serial
import cv2
import hand_finder
import math

width = 1280
height = 720

x = 0
y = 0
claw = 1

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

Arduino_Data = serial.Serial("com9",115200)

hands = hand_finder.findHands()
black = (0,0,0)

def proximity(loc1,loc2):  # checks if the two coordinates are closer than a minimum value
    radius = 80
    if math.copysign(loc1[0] - loc2[0],1) <= radius:
        if math.copysign(loc1[1] - loc2[1],1) <= radius:
            return True
        return False
    return False

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame,1)

    Landmarks,HandType = hands.handloc(frame)
    if Landmarks != []:     
        for handLocation,hand in zip(Landmarks,HandType):
            if hand == 'Right':
                IndexTip = handLocation[8]
                tumb= handLocation[4]
                bottom = handLocation[0]
                
                #for LR motor ____________
                if IndexTip[0] <= (width//2) - width//5: # some breathing room, so that its easier to control
                    x = 2
                elif IndexTip[0] >= width//2 + width//5:
                    x = 1
                else:
                    x = 0
                #_________________________
                # for Pan motor __________
                if IndexTip[1] <= height//2 - height//5: # same logic as the LR motor
                    y = 1
                elif IndexTip[1] >= height//2 + height//5:
                    y = 2
                else:
                    y = 0
                #_________________________
                # for the Claw motor
                if proximity(IndexTip, tumb):
                    claw = 0
                else:
                    claw = 1
                
                # perpendicular = math.copysign((bottom[1]-IndexTip[1]),1)
                # base = math.copysign(bottom[2]-IndexTip[2],1)
                
                data = f"{x}:{y}:{claw}\r"

                print(data)

                Arduino_Data.write(data.encode())  # uncomment when arduino is connected.

            # cv2.circle(frame,handLocation[8],20,black,3)
            # cv2.circle(frame,handLocation[4],20,black,3)
                
    cv2.imshow('screen1', frame)
    cv2.moveWindow('screen1', 0,0)


    if cv2.waitKey(1)== ord('q'):
        break