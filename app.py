from flask import Flask, render_template,Response
import cv2
import numpy as np

app=Flask(__name__)
camera=cv2.VideoCapture(0)
camera.set(3,300)
camera.set(4,400)
camera.set(10,120)

myColors=[[115, 50, 50, 170, 255, 255],[6, 99, 172, 53, 255, 255]]
myCval=[[255,0,255],[0,255,255]]
mypts= [] #[x, y, colorid]

def findColor(img,myColor,myCval,imgres):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpts=[]
    for c in myColor:
        lower = np.array(c[0:3])
        upper = np.array(c[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        #cv2.imshow(str(c[0]), mask)
        x,y=getContours(mask)
        cv2.circle(imgres,(x,y),5,myCval[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpts.append([x,y,count])
        count+=1
    return newpts


def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgres, cnt, -1, (255, 0, 0), 3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y+h//2

def drawOnCanvas(imgres,mypts,myCval):
    for pts in mypts:
        cv2.circle(imgres, (pts[0], pts[1]), 7, myCval[pts[2]], cv2.FILLED)


def generate_frame():
   global mypts
   while True:
    #read the camera frame
    success,frame=camera.read()
    img=cv2.flip(frame,1)
    imgres=img.copy()
    newpts=findColor(img,myColors,myCval,imgres)
    if len(newpts) > 0:
        for newpt in newpts:
            mypts.append(newpt)

    if len(mypts) > 0:
        drawOnCanvas(imgres,mypts,myCval)
    
    if not success:
       break
    else:
       ret,buffer=cv2.imencode('.jpg',imgres)
       frame=buffer.tobytes()
      

    yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


@app.route('/home')
def index():
    return render_template("vp.html")

@app.route('/paint')
def paint():
    return render_template("paint.html")

@app.route('/clear')
def clear():
    global mypts
    mypts.clear()
    return('',204)

@app.route('/video')
def video():
    return Response(generate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')
    

if __name__ == "__main__":
   app.run(debug=True)



