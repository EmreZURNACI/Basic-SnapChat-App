import cv2

# 1. Resmi yükle
image = cv2.imread("resim4.jpeg")

if image is None:
    print("Resim bulunamadı!")
    exit()

# Orijinal boyut
h, w = image.shape[:2]
print(f"Orijinal Boyut: {w}x{h}")

# 2. Boyutlandırma
resize_input = input("Yeni boyutu girin (genişlik,yükseklik) ya da geçmek için Enter: ")
if resize_input:
    try:
        new_w, new_h = map(int, resize_input.split(","))
        image = cv2.resize(image, (new_w, new_h))
    except:
        print("Boyutlandırma hatalı, geçildi.")

# 3. Döndürme (derece cinsinden)
rotate_input = input("Döndürme derecesi girin (örnek: 90 ya da -45) ya da geçmek için Enter: ")
if rotate_input:
    try:
        angle = float(rotate_input)
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        image = cv2.warpAffine(image, matrix, (w, h))
    except:
        print("Döndürme hatalı, geçildi.")

# 4. Çevirme
print("Çevirme seçenekleri:\n 0 = Dikey (üst-alt)\n 1 = Yatay (sağ-sol)\n -1 = Her ikisi")
flip_input = input("Çevirme tipi (0,1,-1) girin ya da geçmek için Enter: ")
if flip_input:
    try:
        flip_code = int(flip_input)
        image = cv2.flip(image, flip_code)
    except:
        print("Çevirme hatalı, geçildi.")

# 5. Kırpma (x,y,genişlik,yükseklik)
crop_input = input("Kırpma alanı girin (x,y,genişlik,yükseklik) ya da geçmek için Enter: ")
if crop_input:
    try:
        x, y, cw, ch = map(int, crop_input.split(","))
        image = image[y:y+ch, x:x+cw]
    except:
        print("Kırpma hatalı, geçildi.")

# Son görüntüyü göster
cv2.imshow("Düzenlenmiş Görsel", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
