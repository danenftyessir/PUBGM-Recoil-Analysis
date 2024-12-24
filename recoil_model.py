import pandas as pd
import numpy as np
from scipy import linalg

def fit_recoil_model(processed_csv_path, weapon_params):
   """
   Fit SPL model untuk data recoil
   """
   # baca data yang udah diproses
   df = pd.read_csv(processed_csv_path)
   # setup matriks untuk SPL 
   t = df['time_normalized'].values
   n = np.arange(len(t))  # jumlah peluru
   # setup parameter spesifik senjata
   p = np.full_like(t, weapon_params['recoil_pattern'])  # nilai pola recoil 
   r = np.full_like(t, weapon_params['random_factor'])   # nilai random spread
   # matriks A untuk vertical dan horizontal
   A = np.column_stack([t, n, p])
   # vektor b untuk vertical dan horizontal
   b_v = df['V'].values
   b_h = df['H'].values
   # hasil SPL menggunakan least squares
   alpha = linalg.lstsq(A, b_v)[0]  # koefisien vertical
   beta = linalg.lstsq(A, b_h)[0]   # koefisien horizontal
   return {
       'vertical_coefficients': alpha,
       'horizontal_coefficients': beta,
       'rmse_vertical': np.sqrt(np.mean((np.dot(A, alpha) - b_v)**2)),
       'rmse_horizontal': np.sqrt(np.mean((np.dot(A, beta) - b_h)**2))
   }

if __name__ == "__main__":
   # parameter untuk tiap senjata (dari statistik resmi PUBG Mobile)
   weapon_parameters = {
       'AKM': {
           'recoil_pattern': 76, 
           'random_factor': 84,  
           'damage': 48,          
           'reload_speed': 76,     
           'jangkauan': 52        
       },
       'M416': {
           'recoil_pattern': 76, 
           'random_factor': 85,   
           'damage': 41,        
           'reload_speed': 76,     
           'jangkauan': 50        
       },
       'SCAR-L': {
           'recoil_pattern': 74,  
           'random_factor': 85,  
           'damage': 41,          
           'reload_speed': 75,    
           'jangkauan': 53        
       }
   }

   # format timestamp sesuai file yang ada
   timestamps = {
       'AKM': '20241224_174856',
       'M416': '20241224_174952', 
       'SCAR-L': '20241224_175030'
   }

   # proses tiap senjata
   for weapon, params in weapon_parameters.items():
       print(f"\nAnalyzing {weapon} recoil pattern...")
       # gunain timestamp yang sesuai untuk setiap senjata
       processed_csv = f"recoil_data_{weapon}_{timestamps[weapon]}_processed.csv"
       try:
           results = fit_recoil_model(processed_csv, params)
           print(f"\nKoefisien untuk {weapon}:")
           print(f"Spesifikasi Senjata:")
           print(f"Recoil Pattern: {params['recoil_pattern']}")
           print(f"Random Factor (Laju Tembak): {params['random_factor']}")
           print(f"Damage: {params['damage']}")
           print(f"Reload Speed: {params['reload_speed']}")
           print(f"Jangkauan: {params['jangkauan']}")
           
           print(f"\nHasil Analisis:")
           print(f"Vertical (α):")
           print(f"α₁ (time): {results['vertical_coefficients'][0]:.4f}")
           print(f"α₂ (shots): {results['vertical_coefficients'][1]:.4f}")
           print(f"α₃ (pattern): {results['vertical_coefficients'][2]:.4f}")
           
           print(f"\nHorizontal (β):")
           print(f"β₁ (time): {results['horizontal_coefficients'][0]:.4f}")
           print(f"β₂ (shots): {results['horizontal_coefficients'][1]:.4f}")
           print(f"β₃ (random): {results['horizontal_coefficients'][2]:.4f}")
           
           print(f"\nRMSE (Root Mean Square Error):")
           print(f"Vertical: {results['rmse_vertical']:.4f}")
           print(f"Horizontal: {results['rmse_horizontal']:.4f}")
           
       except Exception as e:
           print(f"Error analyzing {weapon}: {str(e)}")