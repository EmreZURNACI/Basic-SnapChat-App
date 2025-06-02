import cv2
import numpy as np

def apply_spiral_effect(image):
    # Yükseklik ve genişlik
    (h, w) = image.shape[:2]

    # Griye çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Cascade modelleri
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    # Yüz tespiti
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return image  # Yüz bulunamadıysa orijinal resmi döndür

    (x, y, fw, fh) = faces[0]
    roi_gray = gray[y:y+fh, x:x+fw]

    # Göz tespiti
    eyes = eye_cascade.detectMultiScale(roi_gray)
    if len(eyes) < 2:
        return image  # 2 göz bulunamadıysa orijinal resmi döndür

    # İki gözün merkezini bul
    eyes = sorted(eyes, key=lambda e: e[0])  # soldan sağa sırala
    (eye1_x, eye1_y, eye1_w, eye1_h) = eyes[0]
    (eye2_x, eye2_y, eye2_w, eye2_h) = eyes[1]

    eye1_center = (x + eye1_x + eye1_w // 2, y + eye1_y + eye1_h // 2)
    eye2_center = (x + eye2_x + eye2_w // 2, y + eye2_y + eye2_h // 2)

    # Spiral merkezi = iki gözün tam ortası
    center_x = (eye1_center[0] + eye2_center[0]) // 2
    center_y = (eye1_center[1] + eye2_center[1]) // 2

    # Spiral parametreleri
    max_radius = np.sqrt(w**2 + h**2)
    strength = 10.0

    # Haritalar
    map_x = np.zeros((h, w), dtype=np.float32)
    map_y = np.zeros((h, w), dtype=np.float32)

    for y_pos in range(h):
        for x_pos in range(w):
            dx = x_pos - center_x
            dy = y_pos - center_y
            r = np.sqrt(dx*dx + dy*dy)
            if r == 0:
                angle = 0
            else:
                angle = strength * (r / max_radius)
            theta = np.arctan2(dy, dx) + angle
            new_x = center_x + r * np.cos(theta)
            new_y = center_y + r * np.sin(theta)
            map_x[y_pos, x_pos] = np.clip(new_x, 0, w - 1)
            map_y[y_pos, x_pos] = np.clip(new_y, 0, h - 1)

    # Spiral efekti uygula
    spiral_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)

    return spiral_image
