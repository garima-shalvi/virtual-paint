# Virtual Paint Application
# Uses OpenCV for real-time color detection and Flask to stream the painted video feed to a web interface

from flask import Flask, render_template,Response
import cv2
import numpy as np

# Initializes webcam and configures resolution and brightness
app=Flask(__name__)
camera=cv2.VideoCapture(0)
camera.set(3,300)
camera.set(4,400)
camera.set(10,120)

myColors=[[100, 150, 50, 130, 255, 255] ,[40,80,80,75,255,255],[20,120,120,35,255,255],[5,120,80,20,255,255],[121,51,137,179,255,255]]
myCval=[(255,0,0),(0,255,0),(0,255,255),(0,165,255),(203,192,255)]
mypts= [] #[x, y, colorid]
active_color_id= None


# Detects a specific color in the camera frame, find its position, and draws a dot at that location 

def findColor(img, colorRange, drawColor, imgres): 
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # converts image to HSV for better color detection 

    lower = np.array(colorRange[0:3]) #min HSV values
    upper = np.array(colorRange[3:6]) #max HSV values

    mask = cv2.inRange(imgHSV, lower, upper) 

    kernel = np.ones((7, 7), np.uint8) #for noise cleanup
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    x, y = getContours(mask) # finds position of largest valid object with detected color

    if x != 0 and y != 0:
        cv2.circle(imgres, (x, y), 7, drawColor, cv2.FILLED) # draws a dot on detected position
        return x, y

    return None


# Finds the largest valid colored object from mask and returns it's center 

def getContours(mask):
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    ) # outline of the objects whose color is detected

    max_area = 0 # keeps track of largest valid object
    cx, cy = 0, 0

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area < 300 or area > 12000: # for filtering out irrelevant objects
            continue

        if area > max_area:
            max_area = area
            x, y, w, h = cv2.boundingRect(cnt)
            cx = x + w // 2
            cy = y + h // 2

    return cx, cy
    


# continuously read frames from webcam, do color detection, draw paint and stream those frames to browser 

def generate_frame():
    global mypts,active_color_id # Global state used to persist drawing points and selected color across frames
    while True:
        success, frame = camera.read() 
        if not success:
            break

        img = cv2.flip(frame, 1)
        imgres = img.copy()
   
        # checks if a color is selected
        if active_color_id is not None:
           color=myColors[active_color_id]
           result=findColor(img,color,myCval[active_color_id],imgres)# detects the object of selected color
           if result:
              x,y=result;
              mypts.append([x,y,active_color_id])
        for pt in mypts:
            cv2.circle(imgres, (pt[0], pt[1]), 7, myCval[pt[2]], cv2.FILLED) # redraw all previous points

        ret, buffer = cv2.imencode('.jpg', imgres)
        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        ) # stream frames to browser

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
    
@app.route('/set-color/<int:cid>',methods=['POST'])
def set_color(cid):
    global active_color_id
    if 0<=cid<len(myColors):
       active_color_id=cid
    return '',204

@app.route('/set-none',methods=['POST'])
def set_none():
    global active_color_id
    active_color_id=None
    return '',204


if __name__ == "__main__":
   app.run(debug=True,use_reloader=False)



