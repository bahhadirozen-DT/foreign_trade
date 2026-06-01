import os
import json
import requests
import numpy as np
from data_collection.global_scraper import FreeMapScraper
from image_processing.visual_matcher import VisualProductMatcher
from mathematics.stability_analysis import MarketStabilityAnalysis
from optimization.genetic_tsp import solve_tsp_with_genetic

def add_to_github_project(token, project_number, username, company_name, risk_score, visual_score, website, route_rank):
    """Bulunan firmayı ve analiz sonuçlarını doğrudan GitHub CRM tablosuna satır olarak ekler."""
    if not token or token == "YOUR_GITHUB_PAT":
        return
        
    headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
    
    # 1. Aşama: Kullanıcının Proje ID'sini GraphQL ile çekiyoruz
    user_project_query = """
    query($login: String!, $number: Int!) {
      user(login: $login) {
        projectV2(number: $number) {
          id
        }
      }
    }
    """
    
    try:
        proj_res = requests.post(
            "https://github.com",
            json={"query": user_project_query, "variables": {"login": username, "number": int(project_number)}},
            headers=headers
        )
        project_id = proj_res.json()['data']['user']['projectV2']['id']
        
        # 2. Aşama: Tabloya yeni satır (Item) ekliyoruz
        add_item_query = """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
            item { id }
          }
        }
        """
        # Şirket detaylarını içeren taslak metni başlık olarak kaydediyoruz
        summary_title = f"{company_name} | Rota: {route_rank} | Risk: {risk_score:.2f} | Web: {website}"
        
        # GitHub Issue mekanizması üzerinden tabloya bağlama (Standart API Yöntemi)
        issue_res = requests.post(
            f"https://github.com{username}/foreign_trade/issues",
            json={"title": summary_title, "body": f"Risk Skoru: {risk_score}\nGörsel Eşleşme: {visual_score}\nWeb: {website}"},
            headers=headers
        )
        
        if issue_res.status_code == 201:
            content_id = issue_res.json()['node_id']
            requests.post(
                "https://github.com",
                json={"query": add_item_query, "variables": {"projectId": project_id, "contentId": content_id}},
                headers=headers
            )
            print(f"   [✓] {company_name} başarıyla GitHub CRM tablonuza eklendi.")
    except Exception as e:
        print(f"   [-] Tabloya eklenirken API hatası oluştu: {e}")

def run_ai_export_bot(search_product, search_location):
    print("====================================================")
    print(f"🚀 KÜRESEL CRM ENTEGRELİ BOT BAŞLATILDI: {search_product} / {search_location} 🚀")
    print("====================================================\n")

    # Çevresel değişkenlerden GitHub kimlik bilgilerini alıyoruz
    gh_token = os.getenv("GITHUB_TOKEN", "")
    gh_project_num = os.getenv("PROJECT_NUMBER", "1") # Varsayılan olarak 1. proje
    gh_username = "bahhadirozen-DT"

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
        
        visual_score = 0.0
        if customer["website"] != "Bulunamadı":
            visual_score = matcher.verify_customer_product(customer["website"], mock_reference_img)
        customer["visual_match_score"] = visual_score
        
        J = math_analyzer.calculate_jacobian(supply_rate=0.7, demand_rate=1.1, competition_factor=0.4)
        market_metrics = math_analyzer.analyze_eigenvalues(J)
        final_risk = math_analyzer.inject_stochastic_noise(market_metrics["risk_score"], noise_level=0.02)
        
        customer["market_risk_score"] = final_risk
        customer["is_market_stable"] = market_metrics["is_stable"]
        
        verified_customers.append(customer)
        locations_for_tsp.append((customer["lat"], customer["lng"]))

    if len(locations_for_tsp) > 1:
        print("\n🧬 Genetik Algoritma ile Rota hesaplanıyor...")
        best_route_indices, total_cost = solve_tsp_with_genetic(locations_for_tsp)
        
        # Rota sırasını düzgünce indekslemek için bir harita oluşturuyoruz
        actual_route = list(best_route_indices)
        route_mapping = {city_idx: rank + 1 for rank, city_idx in enumerate(actual_route)}
        
        print("\n====================================================")
        print("🎯 TABLOYA YAZMA VE ROTA PLANLAMA AŞAMASI")
        print("====================================================")
        for idx, cust in enumerate(verified_customers):
            rank = route_mapping.get(idx, 99)
            # Veriyi terminale basarken aynı anda GitHub CRM tablosuna gönderiyoruz
            print(f"{rank}. Durak: {cust['name']} Verileri İşleniyor...")
            add_to_github_project(
                token=gh_token,
                project_number=gh_project_num,
                username=gh_username,
                company_name=cust['name'],
                risk_score=cust['market_risk_score'],
                visual_score=cust['visual_match_score'],
                website=cust['website'],
                route_rank=rank
            )
        print(f"\n[✓] Tüm süreç tamamlandı. Toplam Maliyet Katsayısı: {total_cost:.4f}")
    else:
        print("\n[-] Rota optimizasyonu için yeterli lokasyon doğrulanamadı.")

if __name__ == "__main__":
    search_product = os.getenv("SEARCH_PRODUCT", "valves flaps fittings")
    search_location = os.getenv("SEARCH_LOCATION", "Italy")
    
    run_ai_export_bot(search_product, search_location)


