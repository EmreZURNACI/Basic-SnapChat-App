import cv2
import numpy as np

def apply_yansima_effect(image):
    image = cv2.resize(image, (600, 800))  # Sabit boyut
    (h, w) = image.shape[:2]
    cx = w // 2  # orta x noktası

    # 1. Sol yarıyı al ve aynala
    left_half = image[:, :cx]
    left_mirror = cv2.flip(left_half, 1)
    mirror_face = np.hstack((left_half, left_mirror))

    # 2. Gözleri büyütme fonksiyonu
    def enlarge_eyes_area(img, center, radius, scale=0.5):
        x0, y0 = center
        output = img.copy()
        for y in range(-radius, radius):
            for x in range(-radius, radius):
                if x**2 + y**2 > radius**2:
                    continue
                src_x = int(x0 + x / scale)
                src_y = int(y0 + y / scale)
                dst_x = x0 + x
                dst_y = y0 + y
                if 0 <= src_x < w and 0 <= src_y < h and 0 <= dst_x < w and 0 <= dst_y < h:
                    output[dst_y, dst_x] = img[src_y, src_x]
        return output

    # Göz konumları (tahmini)
    eye_y = int(h * 0.4)
    eye_dx = int(w * 0.15)
    eye_radius = 30

    # Sol göz büyütme
    mirror_face = enlarge_eyes_area(mirror_face, (cx - eye_dx, eye_y), eye_radius, scale=0.5)
    # Sağ göz büyütme (ayna simetrisi)
    mirror_face = enlarge_eyes_area(mirror_face, (cx + eye_dx, eye_y), eye_radius, scale=0.5)

    return mirror_face
