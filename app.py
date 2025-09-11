from flask import Flask, jsonify, render_template, Response, url_for
import cv2
import os
import time

app = Flask(__name__)

SAVE_DIR = r"C:\Users\Farrelino Rendy\Documents\web\static\upload"
os.makedirs(SAVE_DIR, exist_ok=True)

stream_camera = cv2.VideoCapture(0)  # 0 = kamera laptop
last_frame = None

def generate_frames():
    global last_frame
    while True:
        success, frame = stream_camera.read()
        if not success:
            break
        else:
            # Encode frame ke JPEG
            last_frame = frame.copy()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Gabungkan dengan boundary untuk streaming MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('kki.html')

@app.route('/halaman2')
def h2():
    return render_template('h2.html')

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    global last_frame
    if last_frame is None:
        return jsonify({"status": "error", "message": "Belum ada frame"})

    filename = f"surface_{int(time.time())}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)
    cv2.imwrite(filepath, last_frame)

    # path relatif agar bisa dipakai <img src="">
    return jsonify({
        "status": "success",
        "path": url_for('static', filename=f"upload/{filename}")
    })

@app.route('/capture2', methods=['POST'])
def capture2():
    global last_frame
    if last_frame is None:
        return jsonify({"status": "error", "message": "Belum ada frame"})

    filename = f"underwater_{int(time.time())}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)
    cv2.imwrite(filepath, last_frame)

    # path relatif agar bisa dipakai <img src="">
    return jsonify({
        "status": "success",
        "path": url_for('static', filename=f"upload/{filename}")
    })


    

if __name__ == '__main__':
    app.run(debug=True)


# Open the camera
