import pandas as pd
import numpy as np

def process_recoil_data(csv_path):
    try:
        # baca data CSV
        print(f"Reading file: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"Original data shape: {df.shape}")
        # normalisasi koordinat relatif terhadap tembakan pertama
        first_x = df.iloc[0]['x_coord']
        first_y = df.iloc[0]['y_coord']
        first_time = df.iloc[0]['time']
        df['x_normalized'] = df['x_coord'] - first_x
        df['y_normalized'] = df['y_coord'] - first_y
        df['time_normalized'] = df['time'] - first_time
        # hitung delta pergerakan 
        df['delta_x'] = df['x_normalized'].diff().fillna(0)
        df['delta_y'] = df['y_normalized'].diff().fillna(0)
        df['delta_time'] = df['time_normalized'].diff().fillna(0.001) 
        # hitung V dan H
        df['V'] = (df['delta_y'] / df['delta_time']).replace([np.inf, -np.inf], np.nan)
        df['H'] = (df['delta_x'] / df['delta_time']).replace([np.inf, -np.inf], np.nan)
        # filter outliers (hanya jika ada data yang valid)
        if not df['V'].isna().all() and not df['H'].isna().all():
            Q1_v = df['V'].quantile(0.25)
            Q3_v = df['V'].quantile(0.75)
            IQR_v = Q3_v - Q1_v
            Q1_h = df['H'].quantile(0.25)
            Q3_h = df['H'].quantile(0.75)
            IQR_h = Q3_h - Q1_h
            df = df[
                (df['V'] >= Q1_v - 1.5*IQR_v) & (df['V'] <= Q3_v + 1.5*IQR_v) &
                (df['H'] >= Q1_h - 1.5*IQR_h) & (df['H'] <= Q3_h + 1.5*IQR_h)
            ]
        # simpan hasil processing
        output_path = csv_path.replace('.csv', '_processed.csv')
        df.to_csv(output_path, index=True)
        print(f"Processed data saved to {output_path}")
        print(f"Processed data shape: {df.shape}")      
        return df    
    except Exception as e:
        print(f"Error processing file {csv_path}: {str(e)}")
        return None

if __name__ == "__main__":
    # dictionary dengan path file yang udah disesuaikan
    weapon_files = {
        'AKM': "recoil_data_AKM_20241224_174856.csv",
        'M416': "recoil_data_M416_20241224_174952.csv",  
        'SCAR-L': "recoil_data_SCAR-L_20241224_175030.csv" 
    }
    # proses data untuk setiap senjata
    for weapon, csv_path in weapon_files.items():
        print(f"\nProcessing {weapon} data...")
        processed_data = process_recoil_data(csv_path)
        if processed_data is not None and not processed_data.empty:
            print(f"\nSample data for {weapon}:")
            print(processed_data[['time_normalized', 'V', 'H']].head())
        else:
            print(f"No valid data processed for {weapon}")