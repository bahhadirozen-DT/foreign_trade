import os
import json
import numpy as np
from data_collection.global_scraper import FreeMapScraper
from image_processing.visual_matcher import VisualProductMatcher
from mathematics.stability_analysis import MarketStabilityAnalysis
from optimization.genetic_tsp import solve_tsp_with_genetic

def run_ai_export_bot(search_product, search_location):
    print("====================================================")
    print(f"🚀 KÜRESEL BOT BAŞLATILDI: {search_product} / {search_location} 🚀")
    print("====================================================\n")

    # Küresel arama motorunu tetikliyoruz
    scraper = FreeMapScraper()
    raw_customers = scraper.find_potential_customers(search_product, search_location)
    
    if not raw_customers:
        print("[-] Belirtilen kriterlerde dünya üzerinde müşteri bulunamadı.")
        return

    mock_reference_img = np.zeros((100, 100, 3), dtype=np.uint8).tobytes()
    verified_customers = []
    locations_for_tsp = []

    matcher = VisualProductMatcher()
    math_analyzer = MarketStabilityAnalysis()

    for customer in raw_customers:
        print(f"\n🔍 {customer['name']} analiz ediliyor...")
        
        # OpenCV Görsel Doğrulama
        visual_score = 0.0
        if customer["website"] != "Bulunamadı":
            visual_score = matcher.verify_customer_product(customer["website"], mock_reference_img)
        customer["visual_match_score"] = visual_score
        
        # İleri Düzey Matematiksel Risk Analizi (Jacobian ve Eigenvalue)
        J = math_analyzer.calculate_jacobian(supply_rate=0.7, demand_rate=1.1, competition_factor=0.4)
        market_metrics = math_analyzer.analyze_eigenvalues(J)
        final_risk = math_analyzer.inject_stochastic_noise(market_metrics["risk_score"], noise_level=0.02)
        
        customer["market_risk_score"] = final_risk
        customer["is_market_stable"] = market_metrics["is_stable"]

        print(f"   -> Görsel Eşleşme Gücü: %{visual_score*100:.2f}")
        
        verified_customers.append(customer)
        locations_for_tsp.append((customer["lat"], customer["lng"]))

    # Genetik Algoritma (TSP) ile Rota Optimizasyonu
    if len(locations_for_tsp) > 1:
        print("\n🧬 Genetik Algoritma ile Gezgin Satıcı (TSP) rotası hesaplanıyor...")
        best_route_indices, total_cost = solve_tsp_with_genetic(locations_for_tsp)
        
        print("\n====================================================")
        print("🎯 OPTİMİZE EDİLMİŞ KÜRESEL ZIYARET VE LOJISTIK ROTASI")
        print("====================================================")
        # Genetik algoritmanın ürettiği indeks listesini düzgünce açıyoruz
        actual_route = list(best_route_indices[0]) if isinstance(best_route_indices[0], (list, tuple)) else list(best_route_indices)
        
        for rank, index in enumerate(actual_route):
            if index < len(verified_customers):
                cust = verified_customers[index]
                print(f"{rank + 1}. Durak: {cust['name']} (Risk Skoru: {cust['market_risk_score']:.3f})")
        print(f"--> Toplam Minimum Maliyet Katsayısı: {total_cost[0] if isinstance(total_cost, tuple) else total_cost:.4f}")
    else:
        print("\n[-] Rota optimizasyonu için yeterli lokasyon doğrulanamadı.")

if __name__ == "__main__":
    # GitHub arayüzündeki formdan girilen değerleri okur, boşsa varsayılanı kullanır
    search_product = os.getenv("SEARCH_PRODUCT", "valves flaps fittings")
    search_location = os.getenv("SEARCH_LOCATION", "Italy")
    
    run_ai_export_bot(search_product, search_location)

