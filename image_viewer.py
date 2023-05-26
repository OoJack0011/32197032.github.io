import cv2
from flask import Flask, render_template, Response
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    camera = cv2.VideoCapture(0)  # 0表示默认摄像头

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='172.26.30.109', port=8080, debug=True)