import cv2
import numpy as np

# Yüz algılama modeli dosyalarını yükle (tek seferde yükleniyor)
face_net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

def detect_faces_dnn(image, confidence_threshold=0.5):
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            faces.append((x1, y1, x2 - x1, y2 - y1))  # x, y, w, h
    return faces

def overlay_mustache(image, mustache, faces):
    for (x, y, w, h) in faces:
        mustache_width = int(w * 1.2)  # Bıyık genişliği
        mustache_height = int(mustache.shape[0] * (mustache_width / mustache.shape[1]))
        resized_mustache = cv2.resize(mustache, (mustache_width, mustache_height), interpolation=cv2.INTER_AREA)

        # Bıyığın konumu (burnun biraz altı)
        mx = x + w // 2 - mustache_width // 2
        my = y + int(h * 0.55)

        for i in range(resized_mustache.shape[0]):
            for j in range(resized_mustache.shape[1]):
                if mx + j >= image.shape[1] or my + i >= image.shape[0]:
                    continue
                alpha = resized_mustache[i, j, 3] / 255.0
                if alpha > 0:
                    for c in range(3):
                        image[my + i, mx + j, c] = (
                            alpha * resized_mustache[i, j, c] +
                            (1 - alpha) * image[my + i, mx + j, c]
                        )
    return image

def add_mustache(image, mustache):
    faces = detect_faces_dnn(image)
    print(f"{len(faces)} yüz bulundu.")
    return overlay_mustache(image, mustache, faces)
