# foreign_trade
maps&amp;others
# 🚀 Akıllı Dış Ticaret İstihbarat ve Lojistik Optimizasyon Botu

Bu proje; hedef pazarlardaki müşterileri bulan, web sitelerindeki ürün görsellerini yapay zeka ile doğrulayan, pazar risklerini diferansiyel denklemlerle analiz eden ve lojistik süreçleri Genetik Algoritma ile optimize eden uçtan uca bir dış ticaret otomasyonudur.

## 🛠️ Teknik Mimari ve Kullanılan Matematikler

1. **Veri Toplama (`data_collection/`):** Google Places API kullanarak ürün anahtar kelimesine göre hedef lokasyondaki ithalatçı/toptancı şirket verilerini (Ad, Web sitesi, Koordinat) çeker.
2. **Bilgisayarlı Görü (`image_processing/`):** Web sitelerinden çekilen ürün görsellerini OpenCV ORB (Oriented FAST and Rotated BRIEF) algoritması ile özellik matrislerine ayırıp benzerlik doğrulaması yapar.
3. **Dinamik Sistemler ve Kararlılık (`mathematics/`):** Pazarın arz-talep ve risk yapısını Diferansiyel Denklemler üzerinden modelleyerek **Jacobian Matrisi** çıkarır. **Eigenvalue (Özdeğer)** taramasıyla pazarın kararlılık (stability) durumunu analiz eder ve **Stokastik Gürültü** ekleyerek kriz simülasyonları yapar.
4. **Rota Optimizasyonu (`optimization/`):** Doğrulanan müşterilerin koordinatlarını alarak **Gezgin Satıcı Problemini (TSP)** evrimsel bir **Genetik Algoritma** (`DEAP` kütüphanesi) ile en kısa sürede ve en az maliyetle çözer.

## 📦 Kurulum

Projeyi yerel bilgisayarınızda çalıştırmak isterseniz:

```bash
git clone <repo-linkiniz>
cd <repo-adi>
pip install -r requirements.txt
python main.py
```
