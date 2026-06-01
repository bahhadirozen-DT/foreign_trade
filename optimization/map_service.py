import folium
from folium.plugins import Geocoder, LocateControl

class WorldwideB2BMapService:
    def __init__(self):
        self.map = None

    def generate_global_map(self, companies_list, route_indices=None, output_name="schekur_global_b2b_map.html"):
        """
        Eski DEAP algoritmanızdan ve veri toplama botunuzdan gelen verileri
        dünya çapında Google Maps modunda listeler.
        """
        # Haritayı tüm dünyayı görecek şekilde başlatır
        self.map = folium.Map(location=[25.0, 10.0], zoom_start=2, tiles="OpenStreetMap")
        
        # Küresel arama motoru ve konum bulucu eklentileri (Ücretsiz)
        Geocoder(placeholder="Dünya çapında ithalatçı veya şehir arayın...").add_to(self.map)
        LocateControl(auto_start=False).add_to(self.map)

        route_coordinates = []
        
        # 1. Firmaları Haritaya Ekleme
        for comp in companies_list:
            lat, lng = comp['lat'], comp['lng']
            risk = comp.get('risk_score', 0)
            route_coordinates.append([lat, lng])
            
            # Eski mathematics modülünüzdeki Jacobian eigenvalue kararlılık analizine göre renk seçimi
            color = "red" if risk > 70 else ("orange" if risk > 40 else "green")
            
            popup_html = f"""
            <div style='width:240px; font-family: Arial, sans-serif;'>
                <h4 style='margin:0 0 5px 0; color:#2c3e50;'>🏢 {comp['name']}</h4>
                <b>Hedef Sektör:</b> {comp.get('sector', 'B2B Alıcı')}<br>
                <b>Pazar Risk Skoru:</b> %{risk}<br>
                <hr style='margin:8px 0;'>
                <a href='https://godaddysites.com' target='_blank' 
                   style='display:inline-block; padding:5px 10px; background:#27ae60; color:white; text-decoration:none; border-radius:3px; font-size:12px;'>
                   Schekur Kataloğu Gönder
                </a>
            </div>
            """
            
            folium.Marker(
                location=[lat, lng],
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=comp['name'],
                icon=folium.Icon(color=color, icon="briefcase", prefix="fa")
            ).add_to(self.map)

        # 2. Eski DEAP GA Modülünden Gelen Optimum Rotayı Çizme
        if route_indices and len(route_coordinates) > 1:
            # Şehirleri algoritmanın bulduğu sıralamaya göre diziyoruz
            ordered_route = [route_coordinates[i] for i in route_indices]
            # Gezgin satıcı problemi gereği başlangıç noktasına geri bağlama
            ordered_route.append(ordered_route[0])
            
            folium.PolyLine(
                locations=ordered_route,
                color="darkblue",
                weight=3,
                opacity=0.8,
                tooltip="DEAP Genetik Algoritma Küresel Sevkiyat Hattı"
            ).add_to(self.map)

        self.map.save(output_name)
        print(f"🌍 Dünya çapında B2B müşteri haritası başarıyla listelendi: {output_name}")
