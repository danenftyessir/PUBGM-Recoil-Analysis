import cv2
import numpy as np
import pandas as pd
from datetime import datetime

class RecoilPatternExtractor:
    def __init__(self, video_path, weapon_name):
        self.video_path = video_path
        self.weapon_name = weapon_name
        self.impact_points = []
        self.timestamps = []
        
    def detect_impact_points(self, frame):
        """Deteksi bullet holes pada frame"""
        # konversi ke grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # threshold untuk isolasi bullet holes (hitam)
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
        # temukan contours untuk bullet holes
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                     cv2.CHAIN_APPROX_SIMPLE)
        # filter contours berdasarkan area
        valid_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 10 < area < 100:  # sesuaikan dengan ukuran bullet hole
                valid_contours.append(cnt)
        return valid_contours
    
    def process_video(self):
        """Proses video untuk ekstrak impact points"""
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # hitung timestamp
            timestamp = frame_count / fps
            # deteksi impact points
            contours = self.detect_impact_points(frame)
            # ekstrak koordinatnya
            for cnt in contours:
                M = cv2.moments(cnt)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    # simpan point dan timestamp jika belum ada di sekitar koordinat tersebut
                    is_new_point = True
                    for (x, y, _) in self.impact_points:
                        if abs(x - cx) < 5 and abs(y - cy) < 5:
                            is_new_point = False
                            break
                    if is_new_point:
                        self.impact_points.append((cx, cy, timestamp))
            cv2.imshow('Processing', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break     
            frame_count += 1
        cap.release()
        cv2.destroyAllWindows()
    def save_to_csv(self):
        """Simpan hasil ke CSV"""
        if not self.impact_points:
            print("No impact points detected!")
            return
        # konversikan ke DataFrame
        df = pd.DataFrame(self.impact_points, 
                         columns=['x_coord', 'y_coord', 'time'])
        # sortir berdasarkan waktu
        df = df.sort_values('time')
        # reset index jadi nomor tembakan
        df.index = range(1, len(df) + 1)
        df.index.name = 'shot_number'
        # tambah info senjata
        df['weapon'] = self.weapon_name
        # generate filename dan save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recoil_data_{self.weapon_name}_{timestamp}.csv"
        df.to_csv(filename)
        print(f"Data saved to {filename}")
        return df

def extract_recoil_pattern(video_path, weapon_name):
    extractor = RecoilPatternExtractor(video_path, weapon_name)
    print("Processing video...")
    extractor.process_video()
    print("Saving data...")
    df = extractor.save_to_csv()
    return df

if __name__ == "__main__":
    video_path = "SCAR-L.mp4"  # ganti dengan path videonya
    weapon_name = "SCAR-L"     # ganti dengan nama senjata yang ditest
    data = extract_recoil_pattern(video_path, weapon_name)
    print("\nHasil ekstraksi 5 data pertama:")
    print(data.head())