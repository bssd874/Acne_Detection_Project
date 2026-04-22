import cv2
import numpy as np

class SkinValidatorSimple:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.skin_lower = np.array([0, 20, 70], dtype=np.uint8)
        self.skin_upper = np.array([20, 255, 255], dtype=np.uint8)
    
    def is_human_face_present(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return len(faces) > 0
    
    def has_skin_tone(self, img, min_skin_percentage=15):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        skin_mask = cv2.inRange(hsv, self.skin_lower, self.skin_upper)
        skin_percentage = (np.sum(skin_mask > 0) / skin_mask.size) * 100
        return skin_percentage >= min_skin_percentage
    
    def validate_image(self, img):
        if img is None:
            return False, "Gambar tidak bisa dibaca"
        
        has_face = self.is_human_face_present(img)
        has_skin = self.has_skin_tone(img)
        
        if has_face:
            return True, "Wajah manusia terdeteksi"
        elif has_skin:
            return True, "Kulit manusia terdeteksi"
        else:
            return False, "Bukan gambar kulit/wajah manusia. Silakan upload foto wajah atau kulit manusia yang jelas."