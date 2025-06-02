import cv2


def blend_robot_face_with_human(human_image, robot_image, output_size=(600, 800), debug=False):
    # Cascade dosyalarını yükle
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    if human_image is None or robot_image is None:
        raise ValueError("Geçerli bir insan veya robot görüntüsü girilmedi.")

    image = cv2.resize(human_image, output_size)
    robot = robot_image

    if robot.shape[2] != 4:
        raise ValueError("Robot görüntüsünün alfa (şeffaflık) kanalına sahip 4 kanallı bir PNG olması gerekir.")

    (h, w) = image.shape[:2]

    # Yüz tespiti
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        raise ValueError("Yüz bulunamadı.")

    (x, y, fw, fh) = faces[0]
    roi_gray = gray[y:y + fh, x:x + fw]

    # Göz tespiti
    eyes = eye_cascade.detectMultiScale(roi_gray)
    if len(eyes) == 0:
        raise ValueError("Göz bulunamadı.")
    (eye_x, eye_y, eye_w, eye_h) = sorted(eyes, key=lambda e: e[0])[0]
    human_eye_center = (x + eye_x + eye_w // 2, y + eye_y + eye_h // 2)

    # Robot göz merkezi
    robot_bgr = robot[:, :, :3]
    robot_alpha = robot[:, :, 3]
    robot_gray = cv2.cvtColor(robot_bgr, cv2.COLOR_BGR2GRAY)
    robot_edges = cv2.Canny(robot_gray, 50, 150)
    contours, _ = cv2.findContours(robot_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        raise ValueError("Robot göz bulunamadı.")

    largest = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest)
    if M["m00"] == 0:
        raise ValueError("Geçerli robot göz merkezi hesaplanamadı.")

    robot_eye_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # Ölçekleme
    scale_x = human_eye_center[0] / robot_eye_center[0]
    scale_y = human_eye_center[1] / robot_eye_center[1]
    scale = min(scale_x, scale_y)
    new_size = (int(robot.shape[1] * scale), int(robot.shape[0] * scale))
    robot_resized = cv2.resize(robot, new_size)

    robot_eye_scaled = (int(robot_eye_center[0] * scale), int(robot_eye_center[1] * scale))
    offset_x = human_eye_center[0] - robot_eye_scaled[0]
    offset_y = human_eye_center[1] - robot_eye_scaled[1]

    # Maske uygulama
    alpha = robot_resized[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha

    for c in range(3):
        for i in range(robot_resized.shape[0]):
            for j in range(robot_resized.shape[1]):
                yi = offset_y + i
                xi = offset_x + j
                if 0 <= xi < w and 0 <= yi < h:
                    image[yi, xi, c] = (alpha[i, j] * robot_resized[i, j, c] +
                                        alpha_inv[i, j] * image[yi, xi, c])

    return image
