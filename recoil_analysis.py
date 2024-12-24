import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class RecoilAnalyzer:
   def __init__(self):
       self.recoil_data = {
           'AKM': {
               'vertical_coef': [595.7897, -77.6807, 19.2800],
               'horizontal_coef': [131.2847, -8.3820, -2.3566], 
               'rmse_vertical': 1713.0550,
               'rmse_horizontal': 787.9401,
               'specs': {
                   'recoil_pattern': 76,
                   'random_factor': 84,
                   'damage': 48,
                   'reload_speed': 76,
                   'jangkauan': 52
               }
           },
           'M416': {
               'vertical_coef': [397.7071, -46.5955, 3.2092],
               'horizontal_coef': [-298.5023, 34.6437, 5.5336],
               'rmse_vertical': 910.6941,
               'rmse_horizontal': 2044.6866,
               'specs': {
                   'recoil_pattern': 76,
                   'random_factor': 85,
                   'damage': 41,
                   'reload_speed': 76,
                   'jangkauan': 50
               }
           },
           'SCAR-L': {
               'vertical_coef': [-21.4130, 6.5493, 1.0589],
               'horizontal_coef': [476.4372, -92.4005, 1.3949],
               'rmse_vertical': 303.6510,
               'rmse_horizontal': 1141.6436,
               'specs': {
                   'recoil_pattern': 74,
                   'random_factor': 85,
                   'damage': 41,
                   'reload_speed': 75,
                   'jangkauan': 53
               }
           }
       }

   def plot_rmse_comparison(self):
       weapons = list(self.recoil_data.keys())
       vertical_rmse = [self.recoil_data[w]['rmse_vertical'] for w in weapons]
       horizontal_rmse = [self.recoil_data[w]['rmse_horizontal'] for w in weapons]
       x = np.arange(len(weapons))
       width = 0.35
       fig, ax = plt.subplots(figsize=(10, 6))
       rects1 = ax.bar(x - width/2, vertical_rmse, width, label='Vertical RMSE', color='skyblue')
       rects2 = ax.bar(x + width/2, horizontal_rmse, width, label='Horizontal RMSE', color='lightcoral')
       ax.set_ylabel('RMSE Value')
       ax.set_title('Perbandingan Error Recoil Pattern antar Senjata')
       ax.set_xticks(x)
       ax.set_xticklabels(weapons)
       ax.legend()

       def autolabel(rects):
           for rect in rects:
               height = rect.get_height()
               ax.annotate(f'{height:.2f}',
                         xy=(rect.get_x() + rect.get_width()/2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom')

       autolabel(rects1)
       autolabel(rects2)
       plt.tight_layout()
       plt.savefig('rmse_comparison.png', dpi=300, bbox_inches='tight')
       plt.close()

   def plot_coefficient_heatmap(self):
       coef_data = {
           'Vertical': {},
           'Horizontal': {}
       }   
       for weapon in self.recoil_data:
           coef_data['Vertical'][weapon] = self.recoil_data[weapon]['vertical_coef']
           coef_data['Horizontal'][weapon] = self.recoil_data[weapon]['horizontal_coef']
       fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
       # vertical
       sns.heatmap(pd.DataFrame(coef_data['Vertical'], 
                               index=['Time', 'Shots', 'Pattern']).T,
                  annot=True, fmt='.2f', cmap='RdYlBu', ax=ax1)
       ax1.set_title('Koefisien Recoil Vertikal')
       
       # horizontal
       sns.heatmap(pd.DataFrame(coef_data['Horizontal'], 
                               index=['Time', 'Shots', 'Random']).T,
                  annot=True, fmt='.2f', cmap='RdYlBu', ax=ax2)
       ax2.set_title('Koefisien Recoil Horizontal')
       
       plt.tight_layout()
       plt.savefig('coefficient_heatmap.png', dpi=300, bbox_inches='tight')
       plt.close()

   def generate_analysis(self):
       analysis = """Analisis Pola Recoil Senjata dalam PUBG Mobile

1. Karakteristik Recoil Vertikal:

a) AKM
- Koefisien waktu (α₁) tertinggi: 595.79, menunjukkan peningkatan recoil vertikal yang sangat signifikan seiring waktu
- Koefisien peluru (α₂) negatif: -77.68, mengindikasikan sedikit pengurangan recoil setelah beberapa tembakan
- Pattern effect (α₃) tertinggi: 19.28, menunjukkan pola recoil yang kompleks dan sulit dikontrol

b) M416
- Koefisien waktu moderat: 397.71, menunjukkan recoil vertikal yang lebih terkendali dibanding AKM
- Pattern effect moderat: 3.21, mengindikasikan pola yang lebih mudah diprediksi
- RMSE vertikal (910.69) menunjukkan variabilitas menengah

c) SCAR-L
- Koefisien waktu terendah: -21.41, menunjukkan kontrol recoil vertikal yang sangat baik
- Pattern effect minimal: 1.06, mengindikasikan pola yang sangat stabil
- RMSE vertikal terendah (303.65) menunjukkan konsistensi tinggi

2. Karakteristik Recoil Horizontal:

a) AKM
- Spread horizontal moderat dengan koefisien waktu 131.28
- RMSE horizontal terendah (787.94) menunjukkan spread yang relatif terkontrol

b) M416
- Menunjukkan tendensi spread negatif (-298.50)
- RMSE horizontal tertinggi (2044.69) mengindikasikan spread yang lebih tidak terprediksi

c) SCAR-L
- Koefisien spread horizontal tertinggi (476.44)
- RMSE horizontal moderat (1141.64)

3. Implikasi untuk Gameplay:

a) AKM
- Ideal untuk pertempuran jarak dekat hingga menengah
- Membutuhkan kontrol recoil vertikal yang aktif
- Spread horizontal yang terprediksi memungkinkan akurasi yang baik

b) M416
- Seimbang untuk berbagai jarak pertempuran
- Recoil vertikal moderat memungkinkan burst firing yang efektif
- Perlu antisipasi spread horizontal yang bervariasi

c) SCAR-L
- Sangat efektif untuk pertempuran jarak menengah
- Recoil vertikal yang minimal memungkinkan akurasi tinggi
- Pattern yang konsisten ideal untuk pemain pemula

Kesimpulan:
Hasil analisis mengkonfirmasi karakteristik yang dikenal dari ketiga senjata ini, dengan AKM menunjukkan recoil terkuat namun terprediksi, M416 menawarkan keseimbangan, dan SCAR-L unggul dalam stabilitas. Pemilihan senjata sebaiknya disesuaikan dengan gaya bermain dan kemampuan mengontrol recoil masing-masing pemain."""
       return analysis

def main():
   analyzer = RecoilAnalyzer()
   
   print("Generating RMSE comparison plot...")
   analyzer.plot_rmse_comparison()
   
   print("Generating coefficient heatmap...")
   analyzer.plot_coefficient_heatmap()
   
   print("\nGenerating analysis report...")
   analysis = analyzer.generate_analysis()
   
   with open('recoil_analysis_report.txt', 'w', encoding='utf-8') as f:
       f.write(analysis)
   
   print("\nAnalysis complete. Files generated:")
   print("1. rmse_comparison.png")
   print("2. coefficient_heatmap.png")
   print("3. recoil_analysis_report.txt")

if __name__ == "__main__":
   main()