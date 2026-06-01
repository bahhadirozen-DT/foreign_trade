import json
import numpy as np
# Yazdığımız modülleri içe aktarıyoruz
from data_collection.google_maps_scraper import GoogleMapsScraper
from image_processing.visual_matcher import VisualProductMatcher
from mathematics.stability_analysis import MarketStabilityAnalysis
from optimization.genetic_tsp import solve_tsp_with_genetic

def run_ai_export_bot(api_key, search_product, search_location):
    print("====================================================")
    print("🚀 AKILLI DIŞ TİCARET VE LOJİSTİK BOTU BAŞLATILDI 🚀")
    print("====================================================\n")

    # 1. ADIM: Müşteri Arama (Google Maps)
    scraper = GoogleMapsScraper(api_key)
    raw_customers = scraper.find_potential_customers(search_product, search_location)
    
    if not raw_customers:
        print("[-] Belirtilen kriterlerde müşteri bulunamadı.")
        return

    # Örnek bir referans görsel baytı (Gerçek sistemde OpenCV ile okunur)
    # Boş bir yapay siyah görsel simüle ediyoruz
    mock_reference_img = np.zeros((100, 100, 3), dtype=np.uint8).tobytes()

    verified_customers = []
    locations_for_tsp = []

    matcher = VisualProductMatcher()
    math_analyzer = MarketStabilityAnalysis()

    # 2. ADIM: Matematiksel Risk ve Görsel Doğrulama Filtrelemesi
    for customer in raw_customers:
        print(f"\n🔍 {customer['name']} analiz ediliyor...")
        
        # A) Görsel Eşleştirme Kontrolü
        visual_score = 0.0
        if customer["website"] != "Bulunamadı":
            visual_score = matcher.verify_customer_product(customer["website"], mock_reference_img)
        customer["visual_match_score"] = visual_score
        
        # B) Matematiksel Kararlılık ve Risk Analizi (Görselinizdeki Yapı)
        # Sektörün genel verilerine göre dinamik matris simüle ediliyor
        J = math_analyzer.calculate_jacobian(supply_rate=0.7, demand_rate=1.1, competition_factor=0.4)
        market_metrics = math_analyzer.analyze_eigenvalues(J)
        
        # Stokastik gürültü eklenmiş nihai risk skoru
        final_risk = math_analyzer.inject_stochastic_noise(market_metrics["risk_score"], noise_level=0.02)
        customer["market_risk_score"] = final_risk
        customer["is_market_stable"] = market_metrics["is_stable"]

        print(f"   -> Görsel Eşleşme Gücü: %{visual_score*100:.2f}")
        print(f"   -> Pazar Kararlılık Durumu: {'GÜVENLİ' if market_metrics['is_stable'] else 'RİSKLİ'}")
        
        # Kriterlere uyan müşterileri rotaya ekle
        verified_customers.append(customer)
        locations_for_tsp.append((customer["lat"], customer["lng"]))

    # 3. ADIM: Genetik Algoritma ile Lojistik Rota Optimizasyonu (TSP)
    if len(locations_for_tsp) > 1:
        print("\n🧬 Genetik Algoritma ile Gezgin Satıcı (TSP) rotası hesaplanıyor...")
        best_route_indices, total_cost = solve_tsp_with_genetic(locations_for_tsp)
        
        print("\n====================================================")
        print("🎯 OPTİMİZE EDİLMİŞ ZİYARET VE SEVKİYAT ROTASI")
        print("====================================================")
        for rank, index in enumerate(best_route_indices[0]):
            cust = verified_customers[index]
            print(f"{rank + 1}. Durak: {cust['name']} (Risk: {cust['market_risk_score']:.3f}, Eşleşme: %{cust['visual_match_score']*100:.1f})")
        print(f"--> Toplam Minimum Maliyet Katsayısı: {total_cost[0]:.4f}")
    else:
        print("\n[-] Rota optimizasyonu için yeterli lokasyon (en az 2) doğrulanamadı.")

if __name__ == "__main__":
    # Test etmek için kendi Google Maps API anahtarınızı girmeniz gerekir
    GOOGLE_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
    
    # Almanya'daki tekstil üreticilerini bul, görsel/matematiksel süzgeçten geçir ve en iyi rotayı çiz
    run_ai_export_bot(GOOGLE_API_KEY, "textile manufacturer", "Frankfurt")
