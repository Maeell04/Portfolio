import subprocess, tempfile, cv2, numpy as np
import CAMERA_CONTROL as cam
from collections import Counter
from matplotlib import pyplot as plt
from time import sleep

def resize_frame():
    frame = cam.capture_frame()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )
    
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        mask = np.zeros_like(frame)
        cv2.drawContours(mask, [largest_contour], -1, (255, 255, 255), -1)
        result = cv2.bitwise_and(frame, mask)
        x, y, w, h = cv2.boundingRect(largest_contour)
    
        cropped = result[y:y+h, x:x+w]
        
        color_frame_resized = cropped.copy()
        
        gray_result = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        _, final_result = cv2.threshold(
            gray_result, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        black_frame_resized = final_result.copy()
        
        return color_frame_resized, black_frame_resized

def cut_frame_black(frame, pct_w=0.1, pct_h=0.2):
    h, w = frame.shape
    third = w // 3
    frame_mid    = frame[:,   third:2*third]
    dw = int(w * pct_w)
    dh = int(h * pct_h)
    
    x0, x1 = dw, max(w - dw, dw)
    y0, y1 = dh, max(h - dh, dh)
    return frame_mid[y0:y1, x0:x1]

def cut_frame_rgb(frame):
    h, w = frame.shape[:2]
    dx = max(1, int(round(w/3)))
    left  = frame[:, :dx]
    right = frame[:, -dx:]
    
    return left, right

def _ocr(gray_roi, tess_args):
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        if np.mean(gray_roi) > 127:
            cv2.imwrite(tmp.name, gray_roi)
        else:
            cv2.imwrite(tmp.name, cv2.bitwise_not(gray_roi))
        try:
            txt = subprocess.check_output(
                ["tesseract", tmp.name, "stdout", *tess_args],
                stderr=subprocess.DEVNULL,
                timeout=2,
            ).decode().strip()
        except subprocess.SubprocessError:
            return 0
    return txt if txt.isdigit() else 0

def detect_number(img,
                  roi_min=1000, roi_max=50000,
                  center_tol=0.2,
                  tess_args=("--oem","3","--psm","10",
                             "-c","tessedit_char_whitelist=0123456789")) -> int:

    # --- pré-traitement ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img.copy()
    _, mask = cv2.threshold(gray, 0, 255,
                            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    h, w = mask.shape
    cx, cy = w // 2, h // 2
    max_dist = center_tol * (w**2 + h**2) ** 0.5

    # --- contours ---
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

    best = None
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if not roi_min < area < roi_max:
            continue
        m = cv2.moments(cnt)
        if m["m00"] == 0:          # contour défectueux
            continue
        cen = (m["m10"] / m["m00"], m["m01"] / m["m00"])
        dist = ((cen[0] - cx)**2 + (cen[1] - cy)**2) ** 0.5
        if dist > max_dist:
            continue
        if best is None or dist < best[0]:
            best = (dist, cnt)

    if best is None:
        return 0

    # --- OCR ---
    x, y, bw, bh = cv2.boundingRect(best[1])
    roi = gray[y:y+bh, x:x+bw]
    roi = cv2.resize(roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    return _ocr(roi, tess_args)


def detect_color(frame):
    color_ranges = [
        {"name": "RED", "hue_min": 0, "hue_max": 10, "sat_min": 50, "val_min": 50, "rgb": (255, 0, 0)},
        {"name": "RED", "hue_min": 170, "hue_max": 180, "sat_min": 50, "val_min": 50, "rgb": (255, 0, 0)},
        {"name": "YELLOW", "hue_min": 11, "hue_max": 25, "sat_min": 50, "val_min": 50, "rgb": (255, 127, 0)},
        {"name": "YELLOW", "hue_min": 26, "hue_max": 40, "sat_min": 50, "val_min": 50, "rgb": (255, 255, 0)},
        {"name": "GREEN", "hue_min": 41, "hue_max": 80, "sat_min": 50, "val_min": 50, "rgb": (0, 255, 0)},
        {"name": "CYAN", "hue_min": 81, "hue_max": 100, "sat_min": 50, "val_min": 50, "rgb": (0, 255, 255)},
        {"name": "BLUE", "hue_min": 101, "hue_max": 140, "sat_min": 50, "val_min": 50, "rgb": (0, 0, 255)},
        {"name": "MAGENTA", "hue_min": 141, "hue_max": 169, "sat_min": 50, "val_min": 50, "rgb": (255, 0, 255)}
    ]

    def get_color_name(hue, sat, val):
        for color in color_ranges:
            if (color['hue_min'] <= hue <= color['hue_max']
                and color.get('sat_min', 0) <= sat <= color.get('sat_max',255)
                and color.get('val_min', 0) <= val <= color.get('val_max',255)):
                return color['name'], color['rgb']
        return "UNDEFINED", (128, 128, 128)

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    spacing = min(width, height) // 12
    offsets = [(-spacing, spacing), (0, spacing), (spacing, spacing),
               (-spacing, 0),       (0, 0),       (spacing, 0),
               (-spacing, -spacing),(0, -spacing),(spacing, -spacing)]

    colors = []
    for dx, dy in offsets:
        cx = width//2 + dx
        cy = height//2 + dy
        hue, sat, val = hsv_frame[cy, cx]
        name, rgb = get_color_name(hue, sat, val)
        colors.append((name, rgb))

    most_common_color, _ = Counter(color for color,_ in colors).most_common(1)[0]
    r, g, b = next(rgb for color,rgb in colors if color==most_common_color)

    return most_common_color
