import base64

import cv2
import numpy as np
from PIL import Image
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS

from biyik import add_mustache
from gozbalon import apply_gozbalon_effect
from gozluk import overlay_glasses
from gunesgozluk import overlay_sun_glasses
from kariketur import apply_cartoon_effect
from piksel import old_film_effect
from robot import blend_robot_face_with_human
from sapka import apply_hat_effect
from spiral import apply_spiral_effect
from yansıma import apply_yansima_effect

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


def detect_faces_dnn(image):
    h, w = image.shape[:2]
    net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123])
    net.setInput(blob)
    detections = net.forward()

    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            faces.append((x1, y1, x2 - x1, y2 - y1))
    return faces


def load_image():
    if 'file' not in request.files:
        return None, jsonify({'error': 'Dosya bulunamadı'}), 400

    file = request.files['file']
    if file.filename == '':
        return None, jsonify({'error': 'Dosya seçilmedi'}), 400

    try:
        pil_image = Image.open(file.stream).convert("RGB")  # <-- convert önemli
        image = np.array(pil_image)
        image = image[:, :, ::-1].copy()  # RGB -> BGR dönüşümü (cv2 için)
        return image, None, None
    except Exception as e:
        return None, jsonify({'error': str(e)}), 500


def send_image_base64(image):
    # OpenCV görüntüsünü PNG formatında encode et
    success, buffer = cv2.imencode('.png', image)
    if not success:
        return jsonify({'error': 'Görüntü kodlanamadı'}), 500

    # Base64 formatına dönüştür
    img_bytes = buffer.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return jsonify({'image_base64': img_base64})


# çalışıyor
@app.route('/gozluk', methods=['POST'])
def gozluk():
    image, error, code = load_image()
    if error:
        return error, code

    glasses = cv2.imread('gozluk.webp', cv2.IMREAD_UNCHANGED)  # RGBA olmalı
    faces = detect_faces_dnn(image)

    if faces:
        image = overlay_glasses(image, glasses, faces)

    resized_image = cv2.resize(image, (800, 800))

    return send_image_base64(resized_image)


# çalışıyor
@app.route('/gunesgozluk', methods=['POST'])
def gunesgozluk():
    image, error, code = load_image()
    if error:
        return error, code

    glasses = cv2.imread('gunes_gozlugu.png', cv2.IMREAD_UNCHANGED)  # RGBA olmalı
    faces = detect_faces_dnn(image)

    if faces:
        image = overlay_sun_glasses(image, glasses, faces)

    resized_image = cv2.resize(image, (800, 800))

    return send_image_base64(resized_image)


# çalışıyor,zamanlama sıkıntısıı var...
@app.route('/spiral', methods=['POST'])
def spiral():
    image, error, code = load_image()
    if error:
        return error, code

    result = apply_spiral_effect(image)
    resized_image = cv2.resize(result, (800, 800))
    return send_image_base64(resized_image)


# çalışıyor
@app.route('/robot', methods=['POST'])
def robot():
    image, error, code = load_image()
    if error:
        return error, code

    robot_img = cv2.imread("robot.png", cv2.IMREAD_UNCHANGED)
    if robot_img is None:
        return "Robot resmi yüklenemedi", 500

    result = blend_robot_face_with_human(image, robot_img)
    return send_image_base64(result)


# çalışıyor
@app.route('/yansima', methods=['POST'])
def yansima():
    image, error, code = load_image()
    if error:
        return error, code

    result = apply_yansima_effect(image)
    resized_image = cv2.resize(result, (800, 800))
    return send_image_base64(resized_image)


# çalıştı
@app.route('/gozbalon', methods=['POST'])
def gozbalon():
    image, error, code = load_image()
    if error:
        return error, code

    result = apply_gozbalon_effect(image)
    resized_image = cv2.resize(result, (800, 800))
    return send_image_base64(resized_image)


# çalışıyor
@app.route('/karikatur', methods=['POST'])
def karikatur():
    image, error, code = load_image()
    if error:
        return error, code

    result = apply_cartoon_effect(image)
    resized_image = cv2.resize(result, (800, 800))
    return send_image_base64(resized_image)


# çalışıyor
@app.route('/sapka', methods=['POST'])
def sapka():
    image, error, code = load_image()
    if error:
        return error, code

    hat = cv2.imread("sapka3.png", cv2.IMREAD_UNCHANGED)
    if hat is None or hat.shape[2] < 4:
        return jsonify({'error': 'sapka3.png bulunamadı veya alfa kanalına sahip değil.'}), 500

    try:
        result = apply_hat_effect(image, hat)
        resized_image = cv2.resize(result, (800, 800))
        return send_image_base64(resized_image)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# çalışıyor
@app.route('/biyik', methods=['POST'])
def biyik():
    image, error, code = load_image()
    if error:
        return error, code

    mustache = cv2.imread("biyik.webp", cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (600, 800))  # opsiyonel

    result = add_mustache(image, mustache)

    resized_image = cv2.resize(result, (800, 800))
    return send_image_base64(resized_image)


# çalışıyor
@app.route('/piksel', methods=['POST'])
def piksel():
    image, error, code = load_image()
    if error:
        return error, code

    result = old_film_effect(image)
    resized_image = cv2.resize(result, (800, 800))
    return send_image_base64(resized_image)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
