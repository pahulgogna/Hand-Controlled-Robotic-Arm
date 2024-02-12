import serial
import cv2
import hand_finder

width = 1280
height = 720

x = 0
y = 0
claw = 1;

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

Arduino_Data = serial.Serial("com3",115200)

hands = hand_finder.findHands()
black = (0,0,0)
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame,1)

    Landmarks,HandType = hands.handloc(frame)
    if Landmarks != []:     
        for handLocation,hand in zip(Landmarks,HandType):
            if hand == 'Right':
                location = handLocation[8]
                tumb= handLocation[4]

                if location[0] <= (width//2) - width//5: # some breathing room, so that its easier to control, here 50 pixels in total
                    x = -1
                elif location[0] >= width//2 + width//5:
                    x = 1
                else:
                    x = 0
                if location[1] <= height//2 - height//5:
                    y = 1
                elif location[1] >= height//2 + height//5:
                    y = -1
                else:
                    y = 0
                print(x,y,claw)
            cv2.circle(frame,handLocation[8],20,black,3)
            cv2.circle(frame,handLocation[4],20,black,3)
    cv2.imshow('screen1', frame)
    cv2.moveWindow('screen1', 0,0)

    if cv2.waitKey(1)== ord('q'):
        break