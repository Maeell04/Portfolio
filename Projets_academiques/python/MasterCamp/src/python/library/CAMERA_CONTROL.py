from picamera2 import Picamera2, Preview
from time import sleep
import cv2

_cam = Picamera2()
_cam_cfg = _cam.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
_cam.configure(_cam_cfg)
_cam.start()
sleep(1)  # allow auto‑exposure to settle

def capture_frame():
    """Grab a frame from Picamera2 and return BGR image for OpenCV."""
    rgb = _cam.capture_array()
    return rgb


def kill_all():
    _cam.close()


def window():
    print("→ Capturing preview window – press ESC to quit…")
    while True:
        frame = capture_frame()
        cv2.imshow("HEAD_CONTROL camera test", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break


def generate_mjpeg_stream():
    import io
    from flask import Response
    from threading import Lock

    stream_lock = Lock()

    def generate():
        while True:
            with stream_lock:
                frame = capture_frame()
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_last_frame_jpeg():
    frame = capture_frame()  # BGR
    _, buffer = cv2.imencode('.jpg', frame)
    return io.BytesIO(buffer)

# === Self‑test ===
if __name__ == "__main__":
    try:
        window()
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        print("Cleaning up...")
        kill_cam()
        print("Test complete.")
