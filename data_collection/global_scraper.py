import requests
from geopy.geocoders import Nominatim
import time

class FreeMapScraper:
    def __init__(self):
        # Küresel konum çözücü (Tüm dünya ülkelerini kapsar)
        self.geolocator = Nominatim(user_agent="global_foreign_trade_intelligence_bot_final")
        self.overpass_url = "https://overpass-api.de"

    def find_potential_customers(self, product_query, location_name):
        print(f"[+] Hedef bölge/ülke doğrulanıyor: '{location_name}'...")
        try:
            # Girdiğiniz ülke ne olursa olsun dünya haritasında sınırlarını bulur
            loc = self.geolocator.geocode(location_name)
            if not loc:
                print("[-] Girdiğiniz ülke veya bölge dünya haritasında algılanamadı.")
                return []
            
            osm_id = loc.raw.get('osm_id')
            if not osm_id:
                print("[-] Bölgeye ait harita kimliği çözülemedi.")
                return []
                
            # Overpass API için dünya genelinde geçerli Area ID hesaplama formülü
            area_id = int(osm_id) + 3600000000
            
            print(f"[+] Küresel tarama başladı! Sektör/Ürün kelimesi: '{product_query}'...")

            # Küresel Genel Sorgu: Yazılan ürün kelimesini, hedef ülkedeki 
            # tüm endüstriyel tesisler, fabrikalar, distribütörler ve ticari şirketler içinde arar.
            overpass_query = f"""
            [out:json][timeout:50];
            area({area_id})->.searchArea;
            (
              nwr["office"](area.searchArea);
              nwr["industrial"](area.searchArea);
              nwr["commercial"](area.searchArea);
              nwr["company"](area.searchArea);
              nwr["manufacturer"](area.searchArea);
            );
            out center;
            """
            
            response = requests.post(self.overpass_url, data={'data': overpass_query}, timeout=45)
            data = response.json()
            
            customers = []
            search_keywords = product_query.lower().split()
            
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                name = tags.get('name') or tags.get('operator') or tags.get('brand')
                if not name:
                    continue
                
                # Küresel kelime filtreleme algoritması
                tags_string = f"{name} " + " ".join([f"{k} {v}" for k, v in tags.items()]).lower()
                
                if not any(word in tags_string for word in search_keywords):
                    continue
                
                lat = element.get('lat') or element.get('center', {}).get('lat')
                lng = element.get('lon') or element.get('center', {}).get('lon')
                website = tags.get('website') or tags.get('contact:website') or "Bulunamadı"
                
                customer_data = {
                    "name": name,
                    "address": tags.get('addr:street', 'Adres detayları için web sitesini inceleyin'),
                    "lat": float(lat),
                    "lng": float(lng),
                    "website": website,
                    "phone": tags.get('phone') or tags.get('contact:phone') or "Bulunamadı"
                }
                
                customers.append(customer_data)
                
                # GitHub tablosunu şişirmemek için en uyumlu 15 firmada sınırla
                if len(customers) >= 15:
                    break
                    
            print(f"[+] Filtrelere uyan {len(customers)} adet küresel şirket doğrulandı.")
            return customers
            
        except Exception as e:
            print(f"[-] Küresel harita motorunda hata: {e}")
            return []
