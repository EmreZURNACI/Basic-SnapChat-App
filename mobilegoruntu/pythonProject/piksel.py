import cv2
import numpy as np


# Eski film (retro) efekti fonksiyonu
def old_film_effect(image):
    # Görüntüyü sarımsı bir tona çevirelim (sepya etkisi)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.array(image, dtype=np.float32)

    # Sarımsı tonlama
    image[:, :, 0] *= 0.5  # Blue kanalını azaltıyoruz
    image[:, :, 1] *= 1.9  # Green kanalını artırıyoruz
    image[:, :, 2] *= 1.1  # Red kanalını artırıyoruz

    image = np.array(image, dtype=np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Kontrast ve parlaklık ayarlamaları
    alpha = 2  # Kontrast artışı
    beta = 30  # Parlaklık artışı
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Gürültü (film tanesi) ekleme
    noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
    image = cv2.add(image, noise)

    # Sonucu döndür
    return image

