import cv2
import numpy as np

def apply_cartoon_effect(image):
    # 1. Gürültüyü azaltmak için bilateral filtre uygula (yüz yumuşar ama kenarlar kalır)
    filtered = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

    # 2. Griye çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Kenar tespiti için median blur
    gray_blur = cv2.medianBlur(gray, 9)

    # 4. Kenarları bul (adaptive threshold ile)
    edges = cv2.adaptiveThreshold(
        gray_blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=9,
        C=2
    )

    # 5. Kenarları BGR’ye çevir (3 kanala çıkar)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # 6. Renkli görüntü ile kenarları bitwise AND ile birleştir (karikatürleştirme)
    cartoon = cv2.bitwise_and(filtered, edges_colored)

    return cartoon
