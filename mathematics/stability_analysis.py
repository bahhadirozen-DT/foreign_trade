import numpy as np
from scipy.linalg import eig

class MarketStabilityAnalysis:
    def __init__(self):
        pass

    def calculate_jacobian(self, supply_rate, demand_rate, competition_factor):
        """
        Dış ticaret pazarının dinamik dengesini temsil eden diferansiyel 
        sistem için anlık Jacobian matrisini (Değişim oranları matrisi) kurar.
        """
        # Örnek bir pazar dinamiği matrisi (Görselinizdeki jacobian_analysis.py mantığı)
        jacobian_matrix = np.array([
            [-supply_rate, competition_factor],
            [-competition_factor, -demand_rate]
        ])
        return jacobian_matrix

    def analyze_eigenvalues(self, jacobian_matrix):
        """
        Görselinizdeki eigenvalue_scan.py mantığı:
        Matrisin özdeğerlerini hesaplar ve pazarın kararlılık durumunu döner.
        """
        eigenvalues, _ = eig(jacobian_matrix)
        
        # Kararlılık Kontrolü: Tüm özdeğerlerin gerçel kısmı negatifse sistem kararlıdır (Asymptotically Stable)
        is_stable = all(ev.real < 0 for ev in eigenvalues)
        
        return {
            "eigenvalues": eigenvalues.tolist(),
            "is_stable": is_stable,
            "risk_score": float(np.max([ev.real for ev in eigenvalues])) # Sıfıra ne kadar yakınsa risk o kadar yüksek
        }

    def inject_stochastic_noise(self, base_value, noise_level=0.05):
        """
        Görselinizdeki stochastic_noise.py mantığı:
        Tedarik zincirindeki anlık kur dalgalanmaları veya gümrük gecikmeleri gibi 
        rastgele dış etkenleri (Gürültü) modele simüle eder.
        """
        noise = np.random.normal(0, noise_level)
        return base_value + noise

if __name__ == "__main__":
    analyzer = MarketStabilityAnalysis()
    J = analyzer.calculate_jacobian(supply_rate=0.8, demand_rate=1.2, competition_factor=0.3)
    result = analyzer.analyze_eigenvalues(J)
    print(f"[+] Kararlılık Analizi Sonucu: {result}")
