import cv2


def overlay_glasses(image, glasses, face_coords):
    for (x, y, w, h) in face_coords:
        gw = w
        gh = int(h * 0.4)
        glasses_resized = cv2.resize(glasses, (gw, gh))

        # Gözlük resminin alfa kanalını kontrol et
        if glasses_resized.shape[2] == 4:  # Alfa kanalı var
            for i in range(gh):
                for j in range(gw):
                    if glasses_resized[i, j][3] != 0:  # Alfa kanalı (şeffaflık)
                        y_offset = y + int(h / 4) + i
                        x_offset = x + j
                        if y_offset < image.shape[0] and x_offset < image.shape[1]:
                            # Alfa kanalı işleme
                            alpha = glasses_resized[i, j][3] / 255.0
                            for c in range(3):  # BGR kanalları
                                image[y_offset, x_offset, c] = (1.0 - alpha) * image[y_offset, x_offset, c] + alpha * \
                                                               glasses_resized[i, j][c]
        else:  # Eğer gözlük resmi alfa kanalı içermiyorsa (BGR)
            for i in range(gh):
                for j in range(gw):
                    y_offset = y + int(h / 4) + i
                    x_offset = x + j
                    if y_offset < image.shape[0] and x_offset < image.shape[1]:
                        image[y_offset, x_offset] = glasses_resized[i, j]

    return image
