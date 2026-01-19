# 🎨 Virtual Paint Application

A computer vision–based virtual painting application that allows users to draw on a virtual canvas using real-time color tracking via a webcam.

Built with **OpenCV** for vision processing and **Flask** for streaming the video feed to a web interface.

---

## 🚀 Features
- Real-time color-based object tracking
- Draw virtually using colored markers or objects
- Multiple color selection with active state
- Reset canvas functionality
- Clean, animated web UI
- Live video stream using Flask

---

## 🛠️ Tech Stack
- Python
- OpenCV
- Flask
- HTML
- CSS
- JavaScript

---

## 📸 Screenshots

### Home Page
![Home Page](static/assets/screenshots/home-page.png)

### Paint Interface
![Paint Page](static/assets/screenshots/paint-page.png)

### Color Drawing Example
![Drawing Example (Blue)](static/assets/screenshots/drawing-blue.png)
![Drawing Example (Green)](static/assets/screenshots/drawing-green.png)
![Drawing Example (Yellow)](static/assets/screenshots/drawing-yellow.png)
![Drawing Example (Orange)](static/assets/screenshots/drawing-orange.png)
![Drawing Example (Light Pink)](static/assets/screenshots/drawing-pink.png)

### Reset and Back Home buttons
![Reset](static/assets/screenshots/reset.png)
![Back Home](static/assets/screenshots/back-home.png)

---

## 🎥 Demo Video
[Click here to watch demo](static/assets/demo.mp4)

---

## ⚙️ How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/garima-shalvi/virtual-paint.git
cd virtual-paint
```
2. Install dependencies
```bash
pip install opencv-python flask numpy
```
3. Run the application
```bash
python app.py
```
4. Open your browser and visit: 
```
http://127.0.0.1:5000/home
```

