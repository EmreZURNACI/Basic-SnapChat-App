import cv2
import numpy as np

def apply_hat_effect(image, hat, proto_path="deploy.prototxt", model_path="res10_300x300_ssd_iter_140000.caffemodel", conf_threshold=0.5):
    # Modeli yükle
    net = cv2.dnn.readNetFromCaffe(proto_path, model_path)

    (h, w) = image.shape[:2]

    # Blob oluştur
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            face_w = x2 - x1
            face_h = y2 - y1

            # Şapka boyutu (daha büyük yap)
            hat_width = int(face_w * 2)
            hat_height = int(face_h * 1)
            resized_hat = cv2.resize(hat, (hat_width, hat_height), interpolation=cv2.INTER_AREA)

            # Şapkayı yüzün üstüne ortala
            hx = x1 - int((hat_width - face_w) / 2)
            hy = y1 - int(hat_height * 0.5)
            hy = max(0, hy)

            # Alfa kanalı kontrolü
            if resized_hat.shape[2] == 3:
                alpha_channel = np.ones(resized_hat.shape[:2], dtype=resized_hat.dtype) * 255
                resized_hat = np.dstack((resized_hat, alpha_channel))

            # Şapkayı yerleştir (alpha blending)
            for i_hat in range(resized_hat.shape[0]):
                for j_hat in range(resized_hat.shape[1]):
                    y_img = hy + i_hat
                    x_img = hx + j_hat
                    if 0 <= x_img < w and 0 <= y_img < h:
                        alpha = resized_hat[i_hat, j_hat, 3] / 255.0
                        if alpha > 0:
                            image[y_img, x_img] = (
                                alpha * resized_hat[i_hat, j_hat, :3] + (1 - alpha) * image[y_img, x_img]
                            ).astype(np.uint8)

    return image
