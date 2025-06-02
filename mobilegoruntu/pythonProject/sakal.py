import cv2
import numpy as np

def overlay_beard(image, beard, faces):
    """
    Sakalı, yüz konumuna göre görüntüye ekler.
    """
    for (x, y, w, h) in faces:
        # Sakal boyutunu yüz boyutuna göre ayarla
        beard_width = w
        beard_height = int(h * 0.6)  # Sakalın yüksekliğini biraz küçült
        resized_beard = cv2.resize(beard, (beard_width, beard_height), interpolation=cv2.INTER_AREA)

        # Sakalın konumunu çene bölgesine yerleştir
        bx = x  # Yüzün x koordinatına göre
        by = y + int(h * 0.54)  # Yüzün alt kısmına (çene) doğru yerleştir

        # Alfa kanalı kontrolü ve gerekiyorsa ekleme
        if resized_beard.shape[2] == 3:
            alpha_channel = np.ones(resized_beard.shape[:2], dtype=resized_beard.dtype) * 255
            resized_beard = np.dstack((resized_beard, alpha_channel))

        # Sakalı yüzün üzerine yerleştir
        for i in range(resized_beard.shape[0]):
            for j in range(resized_beard.shape[1]):
                if by + i >= image.shape[0] or bx + j >= image.shape[1]:
                    continue
                alpha = resized_beard[i, j, 3] / 255.0
                if alpha > 0:
                    image[by + i, bx + j] = (
                        alpha * resized_beard[i, j, :3] + (1 - alpha) * image[by + i, bx + j]
                    ).astype(np.uint8)
    return image


def apply_beard(image_path, beard_path):
    """
    Yüz algılamayı yaparak sakal ekler.
    """
    # Resmi oku
    image = cv2.imread(image_path)

    # Sakal dosyasını oku
    beard = cv2.imread(beard_path, cv2.IMREAD_UNCHANGED)

    # Alfa kanalı yoksa ekle
    if beard.shape[2] == 3:
        alpha_channel = np.ones(beard.shape[:2], dtype=beard.dtype) * 255
        beard = np.dstack((beard, alpha_channel))

    # DNN tabanlı yüz algılayıcıyı yükle
    net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')

    # Yüz algılaması için resmi BGR'den RGB'ye çevir
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, crop=False)

    # Yüzleri tespit et
    net.setInput(blob)
    detections = net.forward()

    # Yüzlerin koordinatlarını al
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Yüksek güvene sahip yüzleri al
            x1 = int(detections[0, 0, i, 3] * w)
            y1 = int(detections[0, 0, i, 4] * h)
            x2 = int(detections[0, 0, i, 5] * w)
            y2 = int(detections[0, 0, i, 6] * h)
            faces.append((x1, y1, x2 - x1, y2 - y1))

    # Sakalı yüzlere ekle
    image_with_beard = overlay_beard(image, beard, faces)

    return image_with_beard
