import cv2

class findHands:
    import mediapipe as mp
    def __init__(self,maxHands=1,con1=0.5,con2=.5,height = 720,width = 1280):
        self.hands = self.mp.solutions.hands.Hands(False,maxHands,1,con1,con2,)
        self.height = height
        self.width = width

    def handloc(self,frame):
        MyHands = []
        handsType = []
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = self.hands.process(frameRGB)
        if result.multi_hand_landmarks != None:
            
            for handLandmarks, hand in zip(result.multi_hand_landmarks,result.multi_handedness):
                handType = hand.classification[0].label
                # print(handType)
                handsType.append(handType)
                myhand = []
                for landmarks in handLandmarks.landmark:
                    myhand.append((int(landmarks.x*self.width),int(landmarks.y*self.height),int(landmarks.z*1000)))

                MyHands.append(myhand)
        return MyHands, handsType