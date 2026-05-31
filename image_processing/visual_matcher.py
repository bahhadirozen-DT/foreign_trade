import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class VisualProductMatcher:
    def __init__(self, reference_image_path=None):
        # Sizin satmak istediğiniz orijinal ürünün görseli (özellik çıkarımı için)
        self.orb = cv2.ORB_create(nfeatures=1000)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
    def fetch_images_from_website(self, url):
        """Müşteri web sitesindeki tüm görsel linklerini toplar"""
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            image_urls = []
            for img in soup.find_all('img'):
                img_url = img.get('src')
                if img_url:
                    image_urls.append(urljoin(url, img_url))
            return image_urls
        except Exception as e:
            print(f"[-] {url} adresinden görsel çekilemedi: {e}")
            return []

    def calculate_image_similarity(self, img1_bytes, img2_bytes):
        """İki görsel arasındaki matematiksel matris benzerliğini hesaplar"""
        try:
            # Görselleri OpenCV formatına çevir
            nparr1 = np.frombuffer(img1_bytes, np.uint8)
            nparr2 = np.frombuffer(img2_bytes, np.uint8)
            img1 = cv2.imdecode(nparr1, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imdecode(nparr2, cv2.IMREAD_GRAYSCALE)

            if img1 is None or img2 is None:
                return 0.0

            # Anahtar noktaları (Keypoints) ve Betimleyicileri (Descriptors) bul
            kp1, des1 = self.orb.detectAndCompute(img1, None)
            kp2, des2 = self.orb.detectAndCompute(img2, None)

            if des1 is None or des2 is None:
                return 0.0

            # Eşleşen noktaları hesapla
            matches = self.bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)

            # Benzerlik skoru: İyi eşleşen noktaların toplam noktalara oranı
            good_matches = [m for m in matches if m.distance < 50]
            similarity_score = len(good_matches) / max(len(kp1), len(kp2))
            return similarity_score
        except Exception:
            return 0.0

    def verify_customer_product(self, website_url, reference_img_bytes):
        """Müşteri sitesindeki görsellerle bizim ürünümüzü kıyaslar, en yüksek skoru döner"""
        img_urls = self.fetch_images_from_website(website_url)
        max_score = 0.0
        
        for url in img_urls[:5]: # İlk 5 görseli test et (performans için)
            try:
                img_res = requests.get(url, timeout=3)
                if img_res.status_code == 200:
                    score = self.calculate_image_similarity(reference_img_bytes, img_res.content)
                    if score > max_score:
                        max_score = score
            except:
                continue
                
        return max_score

# GitHub üstünde test edilmeye hazır taslak altyapı
if __name__ == "__main__":
    matcher = VisualProductMatcher()
    print("[+] Görsel eşleştirme modülü hazır.")
