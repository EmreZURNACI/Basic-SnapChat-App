import cv2
import numpy as np

def apply_gozbalon_effect(image, scale=1.5):
    def magnify_region(image, center, radius, scale):
        output = image.copy()
        x0, y0 = center

        for y in range(-radius, radius):
            for x in range(-radius, radius):
                if x**2 + y**2 > radius**2:
                    continue

                src_x = int(x0 + x / scale)
                src_y = int(y0 + y / scale)
                dst_x = x0 + x
                dst_y = y0 + y

                if 0 <= src_x < image.shape[1] and 0 <= src_y < image.shape[0] and 0 <= dst_x < image.shape[1] and 0 <= dst_y < image.shape[0]:
                    output[dst_y, dst_x] = image[src_y, src_x]

        return output

    # Gri tonlamaya çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Cascade yükle
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    result = image.copy()
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            eye_center = (x + ex + ew // 2, y + ey + eh // 2)
            radius = max(ew, eh) // 2
            result = magnify_region(result, eye_center, radius=radius, scale=scale)

    return result
